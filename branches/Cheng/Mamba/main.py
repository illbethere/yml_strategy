import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from sklearn.preprocessing import StandardScaler
import torch
import torch.nn as nn
import torch.nn.functional as F
from mamba import Mamba, MambaConfig
import argparse
import os
import pickle

parser = argparse.ArgumentParser()
parser.add_argument('--use-cuda', default=False,
                    help='CUDA training.')
parser.add_argument('--seed', type=int, default=1, help='Random seed.')
parser.add_argument('--epochs', type=int, default=300,
                    help='Number of epochs to train.')
parser.add_argument('--lr', type=float, default=0.001,
                    help='Learning rate.')
parser.add_argument('--wd', type=float, default=1e-5,
                    help='Weight decay (L2 loss on parameters).')
parser.add_argument('--hidden', type=int, default=16,
                    help='Dimension of representations')
parser.add_argument('--layer', type=int, default=2,
                    help='Num of layers')
parser.add_argument('--n-test', type=int, default=5,
                    help='Size of test set')
parser.add_argument('--ts-code', type=str, default='jd00',
                    help='Stock code')
parser.add_argument('--save-model', action='store_true',
                    help='Save trained model')
parser.add_argument('--load-model', type=str, default=None,
                    help='Load model from file path')
parser.add_argument('--model-dir', type=str, default='./models',
                    help='Directory to save/load models')                    

args = parser.parse_args()
args.cuda = args.use_cuda and torch.cuda.is_available()

def evaluation_metric(y_test,y_hat):
    MSE = mean_squared_error(y_test, y_hat)
    RMSE = MSE**0.5
    MAE = mean_absolute_error(y_test,y_hat)
    R2 = r2_score(y_test,y_hat)
    print('%.4f %.4f %.4f %.4f' % (MSE,RMSE,MAE,R2))

def set_seed(seed,cuda):
    np.random.seed(seed)
    torch.manual_seed(seed)
    if cuda:
        torch.cuda.manual_seed(seed)

def dateinf(series, n_test):
    lt = len(series)
    print('Training start',series[0])
    print('Training end',series[lt-n_test-1])
    print('Testing start',series[lt-n_test])
    print('Testing end',series[lt-1])

set_seed(args.seed,args.cuda)

class Net(nn.Module):
    def __init__(self,in_dim,out_dim):
        super().__init__()
        self.config = MambaConfig(d_model=args.hidden, n_layers=args.layer)
        self.mamba = nn.Sequential(
            nn.Linear(in_dim,args.hidden),
            Mamba(self.config),
            nn.Linear(args.hidden,out_dim),
            # nn.Tanh()
        )
    
    def forward(self,x):
        x = self.mamba(x)
        return x.flatten()

def PredictWithData(trainX, trainy, testX):
    clf = Net(len(trainX[0]),1)
    
    # 检查是否需要加载已保存的模型
    model_path = os.path.join(args.model_dir, f'{args.ts_code}_model.pth')
    scaler_path = os.path.join(args.model_dir, f'{args.ts_code}_scaler.pkl')
    
    if args.load_model and os.path.exists(model_path):
        print(f"Loading model from {model_path}")
        clf.load_state_dict(torch.load(model_path, map_location='cpu'))
        if args.cuda:
            clf = clf.cuda()
        
        # 直接进行预测
        clf.eval()
        xv = torch.from_numpy(testX).float().unsqueeze(0)
        if args.cuda:
            xv = xv.cuda()
        mat = clf(xv)
        if args.cuda: 
            mat = mat.cpu()
        yhat = mat.detach().numpy().flatten()
        return yhat
    
    # 如果不加载模型，则进行训练
    opt = torch.optim.Adam(clf.parameters(),lr=args.lr,weight_decay=args.wd)
    xt = torch.from_numpy(trainX).float().unsqueeze(0)
    xv = torch.from_numpy(testX).float().unsqueeze(0)
    yt = torch.from_numpy(trainy).float()
    if args.cuda:
        clf = clf.cuda()
        xt = xt.cuda()
        xv = xv.cuda()
        yt = yt.cuda()
    
    for e in range(args.epochs):
        clf.train()
        z = clf(xt)
        loss = F.mse_loss(z,yt)
        opt.zero_grad()
        loss.backward()
        opt.step()
        if e%10 == 0 and e!=0:
            print('Epoch %d | Lossp: %.4f' % (e, loss.item()))

    # 保存模型
    if args.save_model:
        os.makedirs(args.model_dir, exist_ok=True)
        torch.save(clf.state_dict(), model_path)
        print(f"Model saved to {model_path}")

    clf.eval()
    mat = clf(xv)
    if args.cuda: mat = mat.cpu()
    yhat = mat.detach().numpy().flatten()
    return yhat

data = pd.read_csv(args.ts_code+'.DF_1d.csv')
data.columns = data.columns.str.strip()
# 先保存第一列的数据
date_col = pd.to_datetime(data.iloc[:, 0], format='%Y%m%d')
# 删除第一列，然后设置索引
data = data.drop(data.columns[0], axis=1)
data.index = date_col
data.index.name = 'trade_date'

# --- 特征工程开始 ---
# 计算移动平均线 (MA)
data['MA5'] = data['close'].rolling(window=5).mean()
data['MA10'] = data['close'].rolling(window=10).mean()

# 计算指数移动平均线 (EMA)
data['EMA5'] = data['close'].ewm(span=5, adjust=False).mean()
data['EMA10'] = data['close'].ewm(span=10, adjust=False).mean()

# 计算相对强弱指数 (RSI)
delta = data['close'].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
rs = gain / loss
data['RSI'] = 100 - (100 / (1 + rs))

# 删除因计算指标而产生的NaN值
data.dropna(inplace=True)
# --- 特征工程结束 ---

# 计算价格变化率（在删除close列之前）
ratechg = (data['close'] - data['preClose']) / data['preClose']
ratechg = ratechg.values

# 保存close价格并移除该列
close = data.pop('close').values

# 删除不需要的列
cols_to_drop = ['preClose', 'suspendFlag']
cols_to_drop = [col for col in cols_to_drop if col in data.columns]
data.drop(columns=cols_to_drop, inplace=True)

# 选择特征列（排除价格相关列）
feature_cols = [col for col in data.columns if col not in ['close', 'open', 'high', 'low', 'time']]
dat = data[feature_cols].values
trainX, testX = dat[:-args.n_test, :], dat[-args.n_test:, :]
trainy = ratechg[:-args.n_test]

# --- 特征标准化 ---
scaler = StandardScaler()
# 在训练集上拟合scaler
scaler.fit(trainX)
# 对训练集和测试集进行转换
trainX = scaler.transform(trainX)
testX = scaler.transform(testX)

# 保存标准化器
if args.save_model:
    os.makedirs(args.model_dir, exist_ok=True)
    scaler_path = os.path.join(args.model_dir, f'{args.ts_code}_scaler.pkl')
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    print(f"Scaler saved to {scaler_path}")
# --- 特征标准化结束 ---

predictions = PredictWithData(trainX, trainy, testX)
time = data.index[-args.n_test:]
data1 = close[-args.n_test:]
finalpredicted_stock_price = []
# pred = close[-args.n_test-1]
last_price = close[-args.n_test-1]
for i in range(args.n_test):
    predicted_price = last_price * (1 + predictions[i])
    finalpredicted_stock_price.append(predicted_price)
    # pred = close[-args.n_test-1+i]*(1+predictions[i])
    # pred = pred * (1 + predictions[i])
    # finalpredicted_stock_price.append(pred)
    last_price = predicted_price

dateinf(data.index,args.n_test)
print('MSE RMSE MAE R2')
evaluation_metric(data1, finalpredicted_stock_price)
plt.figure(figsize=(10, 6))
plt.plot(time, data1, label='Stock Price')
plt.plot(time, finalpredicted_stock_price, label='Predicted Stock Price')
plt.title('Stock Price Prediction')
plt.xlabel('Time', fontsize=12, verticalalignment='top')
plt.ylabel('Close', fontsize=14, horizontalalignment='center')
plt.legend()
plt.show()