 ### 一、API简介

Java版迅投策略交易API，旨在为客户提供策略交易的Java语言开发接口，包括但不限于普通下单、算法下单、篮子交易、组合交易、委托和成交推送、行情推送、资金和持仓查询等操作，涵盖股票、期货、期权、两融等品种，
支持A股、港股通、商品期货、股指期货、贵金属等市场。


### 二、快速上手

具体代码参见test/目录下的示例程序

#### 1. 第一步

创建一个类，继承接口类XtTraderJavaApiCallback，实现回调函数

```
public class Callback extends XtTraderJavaApiCallback
{
    //连接服务器的回调函数
    public void onConnected(boolean success, String errorMsg)
    {
    ...
    }
	
    //客户端用户登录的回调函数
    public void onUserLogin(String userName, String password, int nRequestId, XtError error)
    {
    ....
    }

    //下单指令的回调
    public void onOrder(int nRequestId, int orderID, XtError  error)
    {
    ....
    }

    //撤单指令的回调
    public void onCancel(int nRequestId, XtError  error)
    {
    }

    //撤委托的回调
    public void onCancelOrder(int nRequestId, XtError  error)
    {
    }

    //获取主推的报单状态（指令）
    public void onRtnOrder(JOrderInfo data)
    {
    ....
    }

    //获得主推的委托明细（委托）
    public void onRtnOrderDetail(JOrderDetail   data)
    {
    ....
    }

    //获得主推的成交明细
    public void onRtnDealDetail(JDealDetail data)
    {
    ...
    }

    //查询产品回调
    public void onReqProductData(int nRequestId, JProductData productData,boolean isLast, XtError error) 
    {
    ...
    }

    ....
}
```

#### 2. 第二步
创建API实例并初始化

```
void init()
{
	// 创建实例
	String address = "127.0.0.1:65300"; // 交易服务地址
	XtTraderJavaApi client = XtTraderJavaApi.createXtTraderJavaApi(address);

	// 设置API回调接口
	client.setCallback(new CallBack);

	// API使用配置初始化
	client.init("../config");

	// 线程阻塞，直到实例销毁
	client->join();
}
```

#### 3. 第三步
登录交易服务

```
public void onConnected(boolean success, String errorMsg)
{
    if (success)
	{
		String machineInfo = "";
		String appId = "";
		String authCode = "";
		m_client.userLogin(m_strUserName, m_strPassWord, ++m_nRequestId, machineInfo, appId, authCode);
	}
        
}
public void onUserLogin(String userName, String password, int nRequestId, XtError error)
{
    // 登录结果处理
}
```

#### 4. 第四步

交易下单或数据查询，场景示例:

##### a. 登录成功后查询产品

```
public void onUserLogin(String userName, String password, int nRequestId, XtError error)
{
    if （error.isSuccess())
    {
        client.reqProductData();
    }
}

public void onReqProductData(int nRequestId, JProductData productData,boolean isLast, XtError error)
{
    // 处理产品相关数据
}
```

##### b. 收到资金账号信息后算法下单
```
public void onRtnLoginStatusWithActKey(String accountID, EBrokerLoginStatus status, int brokerType, String accountKey, String errorMsg)
{
    JAlgorithmOrder orderInfo = new JAlgorithmOrder();
    ...
    算法参数填写
    ...
    client.order(orderInfo, m_nRequestId++);
}

public void onOrder(int nRequestId, int orderID, XtError  error)
{
    // 下单指令反馈
}

public void onRtnOrderDetail(JOrderDetail   data)
{
    // 成交推送
}

public void onRtnOrderDetail(JOrderDetail   data)
{
    // 委托推送
}
```

##### c. 定时器下单
```
public void onUserLogin(String userName, String password, int nRequestId, XtError error)
{
    // 启动定时器，每5秒触发一次
    client.startTimer(5000);
}

// 定时器触发回调
public void onCustomTimer() {
{
     // 普通下单
	 JOrdinaryOrder orderInfo = new JOrdinaryOrder();
	 ...
	 下单参数填写
	 ...
	 client.order(&orderInfo, m_nRequestId++);
}
```
##### d. 启用指令成交统计
创建API实例时启用指令成交统计功能，在onRtnOrderStat()
回调函数中推送指令统计信息，对处于运行中的指令，按票统计，包括成交均价、已成交量、成交笔数等。
```
void init()
{
	// 创建实例
	String address = "127.0.0.1:65300"; // 交易服务地址
	XtTraderJavaApi client = XtTraderJavaApi.createXtTraderJavaApi(address);

	// 设置API回调接口
	client.setCallback(new CallBack);

	// API使用配置初始化
	client.init("../config");

	// 启用指令成交统计功能
	m_client.enableOrderStat(true);

	// 线程阻塞，直到实例销毁
	client->join();
}

//推送指令统计信息
public void onRtnOrderStat(JOrderStat data)
{
    System.out.println("[onRtnOrderStat]"
            + "\n    指令ID: " + data.m_nOrderID
            + "\n    投资备注: " + data.m_strRemark
            + "\n    交易所: " + data.m_strExchangeID
            + "\n    合约代码: " + data.m_strInstrumentID
            + "\n    成交均价: " + data.m_dAveragePrice
            + "\n    成交总量: " + data.m_nTradedVolume
            + "\n    成交笔数: " + data.m_nTradeNum);
}
```

##### e. 指令改参
支持普通算法指令和智能算法指令改参，其中：
+ 普通算法参数：支持修改价格、量、价格类型、投资备注字段，其他字段不支持
+ 智能算法参数：支持修改除资金账号、市场、股票代码、下单类型之外的所有字段

通过回调函数onModifyAlgoCommands()获取改单成功与否的通知

以智能算法为例：
```
// 资金账号登录状态通知
public void onRtnLoginStatusWithActKey(String accountID, EBrokerLoginStatus status, int brokerType, String accountKey, String errorMsg)
{
    testModifyIntelligentAlgorithmOrder(12, accountID, accountKey);
}

// 执行算法指令改单
public void testModifyIntelligentAlgorithmOrder(int nOrderId, String accountID, String accountKey)
{
    JIntelligentAlgorithmOrder orderInfo = new JIntelligentAlgorithmOrder();

    // 资金账号，必填字段。如果不填写会被api打回
   orderInfo.m_strAccountID = accountID;
   
   orderInfo.m_strOrderType = "TWAP";

   // 市场，必填字段。应该填写MarketType.h里的，股票市场有"SH"/"SZ"，如果填空或填错都会被api直接打回
   orderInfo.m_strMarket="SH";

   // 合约代码，必填字段。
   orderInfo.m_strInstrument = "600000";

   // 报单量，必填字段。不可为0，默认值为无效值。不填或填0或被api打回
   orderInfo.m_nVolume = 111000;

   // 报单委托类型。必填字段。根据相应的业务选择，默认为无效值(OPT_INVALID)。不填会被api打回
   orderInfo.m_eOperationType = EOperationType.OPT_BUY;

   // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
   orderInfo.m_dPrice = 9.57;

   // 报单价格类型，必填字段。默认为无效(PTRP_INVALID)
   orderInfo.m_ePriceType = EPriceType.PRTP_FIX;
   
   // 执行时间
   orderInfo.m_nValidTimeStart = (int)(System.currentTimeMillis() / 1000);
   orderInfo.m_nValidTimeEnd = orderInfo.m_nValidTimeStart + 1200;
   
   m_client.modifyAlgoCommands(orderInfo, nOrderId, m_nRequestId++, accountKey);
}

// 改单结果通知
public void onModifyAlgoCommands(int nRequestId, int orderID, String strRemark, XtError error) 
{
    if(error.isSuccess())
    {
        System.out.println("[onModifyAlgoCommands] success.  order id: " + orderID); 	
    }
    else
    {
        System.out.println("[onModifyAlgoCommands] failure.  order id: " + orderID + ", request id: " + nRequestId + ", error msg: " + error.errorMsg());
    }
}
```

### 三、常见问题
#### 1. onUserLogin回调里的error包含错误信息: End of file
原因：是由于API本地的配置文件traderApi.ini里的isUseSSL和一体化服务器上/home/rzrk/server/config/xtapiservice.lua里的isUseSSL的值不匹配导致的。

解决办法：把两者都修改为0，然后重启API程序和一体化服务器上的XtApiService服务即可。把两者都修改为0，然后重启API程序和一体化服务器上的XtApiService服务即可。

#### 2. onUserLogin回调里的error包含错误信息: md5不匹配禁止登录
原因：是由于一体化服务器上开启了API的md5校验导致的。

解决办法：修改一体化服务器上/home/rzrk/server/config/xtapiservice.lua里的isUseMD5Check的值修改为0，然后重启一体化服务器上的XtApiService服务即可。

#### 3. onUserLogin回调里的error包含错误信息: 客户端mac不匹配
原因：是由于一体化服务器上开启了API的mac地址校验导致的。

解决办法：修改一体化服务器上/home/rzrk/server/config/xtapiservice.lua里的isUseMacCheck的值修改为0，然后重启一体化服务器上的XtApiService服务即可。

#### 4. 周末要测试，但是账号休市
原因：周末因为股市休市，所以测试环境对于账号也是默认休市处理。

解决办法：在一体化管理端左侧菜单'系统监控->交易日设置'里，设置当天日期为交易日。如果调整之后，管理端上账号状态不是登录成功，可以在ET软件上对该账号关联的交易端执行'停用监控'操作后再'启用监控'。

#### 5. 周一到周五盘后要测试，但是账号休市
原因：目前系统默认16:00账号休市，所以通常16:00以后账号会进入休市状态。

解决办法：在一体化管理端左侧菜单'基础管理->经纪公司'里，对要测试的经纪公司，点击设置来修改日盘时间即可。如果调整之后，管理端上账号状态不是登录成功，可以在ET软件上对该账号关联的交易端执行'停用监控'操作后再'启用监控'。

#### 6. 接口中的自定义请求序号的使用
每个接口中都会要求传入一个自定义请求序号的参数，如普通下单接口 *public native void order(JOrdinaryOrder orderInfo, int nRequestId)* 中的nRequestId参数，该参数由开发者自定义，并在回调函数中返回该值，旨在让开发者可以依此管理请求和回调的匹配关系。建议该值从1开始递增，每次调用保持不重复；若该值重复，API本身不会产生任何功能和性能问题。小于0的值由系统保留使用。

#### 7. 线程模型说明
API内部使用线程池机制，下单和查询系列回调函数可能会在不同的线程中运行，所以若开发者在回调函数中的代码涉及读写全局变量，需做同步控制，防止数据错乱或者程序崩溃。

#### 8. 收到指令号为2147483647的推送是什么
带有指令号为2147483647的推送数据表示这是外部委托。

#### 9. 运行报错：Can't find dependent libraries
原因：找不到依赖的动态库。若通过-Djava.library.path设置动态库路径，则只能找到XtTraderJavaApi.dll，找不到其他动态库。

解决办法：将所有动态库放在java运行目录下（一般是代码所在的根目录），即可解决问题。

