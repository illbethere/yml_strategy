/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   XtTraderJavaApiCallback.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti;

import xti.XtDataType.*;
import xti.XtError.XtError;
import xti.XtStructs.*;

import java.util.ArrayList;

/**
* XtTraderJavaApi回调接口
* 相应请求的回调函数
* nRequestId 和请求函数中 nRequestId 想对应
* error 请求函数的返回是否成功，如果失败有错误信息
* 函数名组成：以 on 为前缀，加上相应请求函数的函数名称（请求函数首字母大写）
*/

public abstract class XtTraderJavaApiCallback {
        
    public XtTraderJavaApi traderApi;
    private long ApiId;
    
    public XtTraderJavaApi getTraderApi() {
        return this.traderApi;
    }
    public void setTraderApi(XtTraderJavaApi traderApi) {
        this.traderApi = traderApi;
    }    
    public long getApiId() {
        return this.ApiId;
    }
    public void setApiId(long apiId) {
        this.ApiId = apiId;
    }    
    
    /**
    * 连接服务器的回调函数
    * @param success 服务器连接是否成
    * @param errorMsg 如果服务器连接失败，存储错误信息
    */
    public abstract void onConnected(boolean success, String errorMsg);

    /**
    * 用户登录的回调函数
    * @param userName 用户名
    * @param password 用户密码
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param error 错误信息
    * 当error返回报错时，error.errorMsg()包含登陆失败原因
    */
    public abstract void onUserLogin(String userName, String password, int nRequestId, XtError error);

    /**
    * 用户登出的回调函数
    * @param userName 用户名
    * @param password 用户密码
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param error 错误信息
    * 当error返回报错时，error.errorMsg()包含登陆失败原因
    */
    public abstract void onUserLogout(String userName, String password, int nRequestId, XtError error);
    
    /**
    * 请求账号资金的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 账号资金数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqAccountDetail(String accountID, int nRequestId, JAccountDetail data, boolean isLast, XtError error);

    /**
    * 请求账号资金的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账户key
    * @param data 账号资金数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqAccountDetailWithAccKey(String accountID, int nRequestId, String accountKey, JAccountDetail data, boolean isLast, XtError error);

    /**
    * 请求账号委托明细的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 账号委托明细数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqOrderDetail(String accountID, int nRequestId, JOrderDetail data, boolean isLast, XtError error);

    /**
    * 请求账号委托明细的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账户key
    * @param data 账号委托明细数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqOrderDetailWithAccKey(String accountID, int nRequestId, String accountKey, JOrderDetail data, boolean isLast, XtError error);

    /**
    * 请求账号成交明细的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 账号成交明细数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqDealDetail(String accountID, int nRequestId, JDealDetail data, boolean isLast, XtError error);

    /**
    * 请求账号成交明细的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账户key
    * @param data 账号成交明细数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqDealDetailWithAccKey(String accountID, int nRequestId, String accountKey, JDealDetail data, boolean isLast, XtError error);

    /**
    * 请求账号持仓明细的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 账号持仓明细数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqPositionDetail(String accountID, int nRequestId, JPositionDetail data, boolean isLast, XtError error);

    /**
    * 请求账号持仓明细的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账户key
    * @param data 账号持仓明细数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqPositionDetailWithAccKey(String accountID, int nRequestId, String accountKey, JPositionDetail data, boolean isLast, XtError error);

    /**
    * 请求账号持仓统计的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 账号持仓统计数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqPositionStatics(String accountID, int nRequestId, JPositionStatics data, boolean isLast, XtError error);

    /**
    * 请求账号持仓统计的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账户key
    * @param data 账号持仓统计数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqPositionStaticsWithAccKey(String accountID, int nRequestId, String accountKey, JPositionStatics data, boolean isLast, XtError error);

    /**
     * @brief 请求期货账号持仓统计的回调函数
     * @param  accountID 账号ID
     * @param  nRequestId 客户自己维护的请求顺序ID
     * @param  accountKey 账户key
     * @param  data 期货账号持仓统计数据，一次最大返回设置返回条数，数据超过设置数量多次返回
     * @param  isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
     * @param  error 错误信息
     * @attention 当error返回报错时，data内容不可用
     */
    public abstract void onReqFuturePositionStatics(String accountID, int nRequestId, String accountKey, ArrayList<JFuturePositionStatics> data, boolean isLast, XtError error) ;

    /**
    * 请求两融账号负债的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 两融账号负债数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqStkcompacts(String accountID, int nRequestId, JStkCompacts data, boolean isLast, XtError error);

    /**
    * 请求两融账号负债的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账户key
    * @param data 两融账号负债数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqStkcompactsWithAccKey(String accountID, int nRequestId, String accountKey, JStkCompacts data, boolean isLast, XtError error);

    /**
    * 请求期权账号备兑持仓的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 期权账号备兑持仓数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqCoveredStockPosition(String accountID, int nRequestId,  JCoveredStockPosition data, boolean isLast, XtError error);

    /**
    * 请求期权账号备兑持仓的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账户key
    * @param data 期权账号备兑持仓数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqCoveredStockPositionWithAccKey(String accountID, int nRequestId, String accountKey, JCoveredStockPosition data, boolean isLast, XtError error);

    /**
    * 请求期权账号组合持仓数据的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 期权账号组合持仓数据数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqStkOptCombPositionDetail(String accountID, int nRequestId,  JStockOptionCombPositionDetail data, boolean isLast, XtError error);

    /**
    * 请求期权账号组合持仓数据的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账户key
    * @param data 期权账号组合持仓数据数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqStkOptCombPositionDetailWithAccKey(String accountID, int nRequestId, String accountKey, JStockOptionCombPositionDetail data, boolean isLast, XtError error);

    /**
    * 请求账号两融资金的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 账号两融资金数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqCreditAccountDetail(String accountID,int nRequestId, JCreditAccountDetail data, boolean isLast,XtError  error);

    /**
    * 请求账号两融资金的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账户key
    * @param data 账号两融资金数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqCreditAccountDetailWithAccKey(String accountID,int nRequestId, String accountKey, JCreditAccountDetail data, boolean isLast,XtError  error);

    /**
    * 请求行情数据的回调函数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 行情数据数据
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqPriceData(int nRequestId, JPriceData data, XtError error);

    /**
    * 主推的报单状态（指令）
    * @param data 下单指令信息
    */
    public abstract void onRtnOrder(JOrderInfo data);
    
    /**
    * 指令成交统计信息（指令）
    * @param data 指令统计信息
    */
    public abstract void onRtnOrderStat(JOrderStat data);

    /**
    * 主推的委托明细（委托）
    * @param data 委托明细信息
    */
    public abstract void onRtnOrderDetail(JOrderDetail data);

    /**
    * 主推的成交明细
    * @param data 成交明细信息
    */
    public abstract void onRtnDealDetail(JDealDetail data);

    /**
    * 主推的委托错误信息
    * @param data 下单失败的错误信息
    */
    public abstract void onRtnOrderError(JOrderError data);

    /**
    * 主推的撤销信息
    * @param data 撤单失败的错误信息
    */
    public abstract void onRtnCancelError(JCancelError data);

    /**
    * 主推的用户登录状态
    * @param accountID 账号ID
    * @param status 主推资金账号的登录状态
    * @param brokerType 主推资金账号的类型
    * @param errorMsg 错误信息
    * brokerType取值1:期货账号, 2:股票账号, 3:信用账号, 4:贵金属账号, 5:期货期权账号, 6:股票期权账号, 7:沪港通账号, 10:全国股转账号
    */
    public abstract void onRtnLoginStatus(String accountID, EBrokerLoginStatus status, int brokerType, String errorMsg);
    
    /**
    * 主推的用户登录状态
    * @param accountID 账号ID
    * @param status 主推资金账号的登录状态
    * @param brokerType 主推资金账号的类型
    * @param accountKey 账号 key，用于区分不同类型的相同账号ID的账号
    * @param errorMsg 错误信息
    * brokerType取值1:期货账号, 2:股票账号, 3:信用账号, 4:贵金属账号, 5:期货期权账号, 6:股票期权账号, 7:沪港通账号, 10:全国股转账号
    */
    public abstract void onRtnLoginStatusWithActKey(String accountID, EBrokerLoginStatus status, int brokerType, String accountKey, String errorMsg);

    /**
    * 主推的用户登录状态
    * @param accountID 账号ID
    * @param status 主推资金账号的登录状态
    * @param brokerType 主推资金账号的类型
    * @param accountKey 账号 key，用于区分不同类型的相同账号ID的账号
    * @param userName 用户名
    * @param errorMsg 错误信息
    * brokerType取值1:期货账号, 2:股票账号, 3:信用账号, 4:贵金属账号, 5:期货期权账号, 6:股票期权账号, 7:沪港通账号, 10:全国股转账号
    */
    public abstract void onRtnLoginStatusCustom(String accountID, EBrokerLoginStatus status, int brokerType, String accountKey, String userName, String errorMsg);

    /**
    * 主推的资金账号信息
    * @param accountID 账号ID
    * @param data 账号资金信息
    */
    public abstract void onRtnAccountDetail(String accountID, JAccountDetail data);

    /**
    * 主推的两融资金账号信息
    * @param accountID 账号ID
    * @param data 账号两融资金信息
    */
    public abstract void onRtnCreditAccountDetail(String accountID, JCreditAccountDetail data);

    /**
    * 主推的产品净值信息
    * @param data 产品净值信息
    */
    public abstract void onRtnNetValue(JNetValue data);

    /**
    * 下单的回调函数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param orderID 指令号
    * @param strRemark 下单时填写的投资备注
    * @param error 错误信息
    * 当error返回报错时，error.errorMsg()包含下单失败原因
    */
    public abstract void onOrder(int nRequestId, int orderID, String strRemark, XtError error);
    
    /**
    * 直接下单的回调函数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param strOrderSysID 委托号
    * @param strRemark 下单时填写的投资备注
    * @param error 错误信息
    * 当error返回报错时，error.errorMsg()包含下单失败原因
    */
    public abstract void onDirectOrder(int nRequestId, String strOrderSysID, String strRemark, XtError error);
    
    /**
    * 撤指令的回调函数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param error 错误信息
    * 当error返回报错时，error.errorMsg()包含撤单失败原因，建议用下面带投资备注的onCancelWithRemark，该接口逐渐废弃
    */
    public abstract void onCancel(int nRequestId, XtError error);

    /**
    * 撤指令的回调函数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param strRemark 下单时填写的投资备注
    * @param error 错误信息
    * 当error返回报错时，error.errorMsg()包含撤单失败原因
    */
    public abstract void onCancelWithRemark(int nRequestId, String strRemark, XtError error);
	
    /**
    * 撤委托的回调函数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param error 错误信息
    * 当error返回报错时，error.errorMsg()包含撤单失败原因
    */
    public abstract void onCancelOrder(int nRequestId, XtError error);
    
    /**
    * 请求产品信息的回调函数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 产品信息数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqProductData(int nRequestId,JProductData data,boolean isLast ,XtError error);

    /**
    * 用户自己的定时器回调
    */
    public abstract void onCustomTimer();

    /**
    * 用户自己的定时器回调
	* @param timerName 定时器名称
    */
    public abstract void onNamedTimer(String timerName);
	
    /**
    * 请求港股账号汇率数据的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 港股账号汇率数据数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqReferenceRate(String accountID,int nRequestId, JReferenceRate data, boolean isLast,XtError error);

    /**
    * 请求港股账号汇率数据的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账户key
    * @param data 港股账号汇率数据数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqReferenceRateWithAccKey(String accountID,int nRequestId, String accountKey, JReferenceRate data, boolean isLast,XtError error);

    /**
    * 请求两融账号两融综合资金数据的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 两融账号两融综合资金数据数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqCreditDetail(String accountID,int nRequestId, JCreditDetail data, boolean isLast,XtError error);

    /**
    * 请求两融账号两融综合资金数据的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账户key
    * @param data 两融账号两融综合资金数据数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqCreditDetailWithAccKey(String accountID,int nRequestId, String accountKey, JCreditDetail data, boolean isLast,XtError error);

    /**
    * 行情订阅的回调函数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 行情订阅数据
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onSubscribQuote(int nRequestId, JSubscribData data, XtError error);

    /**
    * 行情退订的回调函数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 行情订阅数据
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onUnSubscribQuote(int nRequestId, JSubscribData data, XtError error);
    
    /**
    * 主推行情数据
    * @param data 行情数据
    */
    public abstract void onRtnPriceData(JPriceData data);

    /**
    * 暂停恢复任务回调
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号 key，用于区分不同类型的相同账号ID的账号
    * @param error 错误信息，暂停恢复失败时包含错误信息
    * 当error返回报错时，包含错误信息
    */
    public abstract void onOperateTask(String accountID, int nRequestId, String accountKey, XtError error);

    /**
    * 指令改参的回调函数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param orderID 指令号
    * @param strRemark 下单时填写的投资备注
    * @param error 错误信息
    * 当error返回报错时，error.errorMsg()包含下单失败原因
    */
    public abstract void onModifyAlgoCommands(int nRequestId, int orderID, String strRemark, XtError error);

    /**
    * 请求新股额度数据的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 新股信息数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqSubscribeInfo(String accountID,int nRequestId, JSubscribeInfo data, boolean isLast,XtError error);

    /**
    * 请求新股额度数据的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账户key
    * @param data 新股信息数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqSubscribeInfoWithAccKey(String accountID,int nRequestId, String accountKey, JSubscribeInfo data, boolean isLast,XtError error);
    
    /**
    * 请求未了结负债信息的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 未了结负债信息数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqStkUnCloseCompact(String accountID,int nRequestId, JStkUnClosedCompacts data, boolean isLast,XtError error);

    /**
    * 请求未了结负债信息的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账户key
    * @param data 未了结负债信息数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqStkUnCloseCompactWithAccKey(String accountID,int nRequestId, String accountKey, JStkUnClosedCompacts data, boolean isLast,XtError error);

    
    /**
    * 请求已了结负债信息的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 已了结负债信息数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqStkClosedCompact(String accountID,int nRequestId, JStkClosedCompacts data, boolean isLast,XtError error);

    /**
    * 请求已了结负债信息的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账户key
    * @param data 已了结负债信息数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqStkClosedCompactWithAccKey(String accountID,int nRequestId, String accountKey,JStkClosedCompacts data, boolean isLast,XtError error);

    
    /**
    * 获取用户下所有账号key的回调函数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 已了结负债信息数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqAccountKey(int nRequestId, JAccountKey data, boolean isLast,XtError error);

    /**
     * 根据委托号请求账号委托明细信息的回调函数
     * @param accountID 账号ID
     * @param nRequestId 客户自己维护的请求顺序ID
     * @param accountKey 账号key
     * @param orderSyeId 委托号
     * @param exchangeId 委托所属市场
     * @param data 账号委托明细数据
     * @param error 错误信息
     * 当error返回报错时，data内容不可用
     */
    public abstract void onReqOrderDetailBySysID(String accountID,int nRequestId, String accountKey, String orderSyeId, String exchangeId, JOrderDetail data, XtError error);


    /**
    * 根据委托号请求账号成交明细信息的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param orderSyeId 委托号
    * @param exchangeId 委托所属市场
    * @param data 账号成交明细数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqDealDetailBySysID(String accountID,int nRequestId, String orderSyeId, String exchangeId, JDealDetail data, boolean isLast,XtError error);

    /**
    * 根据委托号请求账号成交明细信息的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号key
    * @param orderSyeId 委托号
    * @param exchangeId 委托所属市场
    * @param data 账号成交明细数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqDealDetailBySysIDWithAccKey(String accountID,int nRequestId, String accountKey, String orderSyeId, String exchangeId, JDealDetail data, boolean isLast,XtError error);

    /**
    * 请求账号结算单信息的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 账号结算单数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqDeliveryDetail(String accountID, int nRequestId, JDeliveryDetail data, boolean isLast, XtError error);

    /**
    * 请求账号结算单信息的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key
    * @param data 账号结算单数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqDeliveryDetailWithAccKey(String accountID, int nRequestId, String accountKey, JDeliveryDetail data, boolean isLast, XtError error);
    
    /**
    * 请求账号合约行情信息的回调函数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 合约数据数据
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqSingleInstrumentInfo(int nRequestId, JInstrumentInfo data, XtError error);
    
    /**
    * 主推市场状态信息
    * @param data 市场状态信息
    */
    public abstract void onRtnExchangeStatus(JExchangeStatus data);

    /**
    * 主推两融综合资金
    * @param data 两融综合资金
    */
    public abstract void onRtnCreditDetail(JCreditDetail data);
    
    /**
    * 请求账号可下单量的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param dataKey 数据标识，市场加合约
    * @param nVolume 可下单量
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqOpVolume(String accountID,int nRequestId, String dataKey,int nVolume, boolean isLast, XtError error);

    /**
    * 请求账号可下单量的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号key
    * @param dataKey 数据标识，市场加合约
    * @param nVolume 可下单量
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqOpVolumeWithAccKey(String accountID,int nRequestId, String accountKey, String dataKey,int nVolume, boolean isLast, XtError error);
    
    /**
    * 请求两融账号融券可融数量的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 融券可融数量数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqCreditSloCode(String accountID,int nRequestId, JCreditSloCode data, boolean isLast,XtError error);

    /**
    * 请求两融账号融券可融数量的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号key
    * @param data 融券可融数量数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqCreditSloCodeWithAccKey(String accountID,int nRequestId, String accountKey, JCreditSloCode data, boolean isLast,XtError error);
    
    /**
    * 请求两融账号融资融券标的的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 融资融券标的数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqCreditSubjects(String accountID,int nRequestId, JCreditSubjects data, boolean isLast,XtError error);

    /**
    * 请求两融账号融资融券标的的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key
    * @param data 融资融券标的数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqCreditSubjectsWithAccKey(String accountID,int nRequestId, String accountKey, JCreditSubjects data, boolean isLast,XtError error);
    
    /**
    * 请求两融账号担保标的的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 担保标的数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqCreditAssure(String accountID,int nRequestId, JCreditAssure data, boolean isLast,XtError error);

    /**
    * 请求两融账号担保标的的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号key
    * @param data 担保标的数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqCreditAssureWithAccKey(String accountID,int nRequestId, String accountKey,JCreditAssure data, boolean isLast,XtError error);
    
    /**
    * 请求账号银证转账银行信息的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 账号银证转账银行信息数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqTransferBank(String accountID,int nRequestId, JQueryBankInfo data, boolean isLast,XtError error);

    /**
    * 请求账号银证转账银行信息的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key
    * @param data 账号银证转账银行信息数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqTransferBankWithAccKey(String accountID,int nRequestId, String accountKey,JQueryBankInfo data, boolean isLast,XtError error);
    
    /**
    * 请求账号银证转账银行流水的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 账号银证转账银行信息数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqTransferSerial(String accountID,int nRequestId, JTransferSerial data, boolean isLast,XtError error);

    /**
    * 请求账号银证转账银行流水的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key
    * @param data 账号银证转账银行信息数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqTransferSerialWithAccKey(String accountID,int nRequestId, String accountKey, JTransferSerial data, boolean isLast,XtError error);
    
    /**
    * 请求账号银证转账银行余额的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 账号银证转账银行余额数据
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqBankAmount(String accountID,int nRequestId, JQueryBankAmount data,XtError error);  

    /**
    * 请求账号银证转账银行余额的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key
    * @param data 账号银证转账银行余额数据
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqBankAmountWithAccKey(String accountID,int nRequestId, String accountKey,JQueryBankAmount data,XtError error);  
    
    /**
    * 银证转账的回调函数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param error 错误信息
    * 当error返回报错时，error.errorMsg()包含转账失败原因
    */
    public abstract void onTransfer(int nRequestId,XtError error);
    
    /**
    * 按市场请求合约信息的回调函数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 合约信息数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqInstrumentInfoByMarket(int nRequestId, JInstrumentInfo data, boolean isLast, XtError error);
    
    /**
    * 按市场请求合约信息的回调函数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param exchangeId 委托所属市场
    * @param data 合约信息数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqInstrumentInfoByMarketWithMkt(int nRequestId, String exchangeId, JInstrumentInfo data, boolean isLast, XtError error);
    
    /**
    * 请求账号可撤单委托明细的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 账号委托明细数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqCanCancelOrderDetail(String accountID, int nRequestId, JOrderDetail data, boolean isLast, XtError error);

    /**
    * 请求账号可撤单委托明细的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号key
    * @param data 账号委托明细数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqCanCancelOrderDetailWithAccKey(String accountID, int nRequestId, String accountKey, JOrderDetail data, boolean isLast, XtError error);

    /**
    * 请求所有下单命令信息的回调函数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 命令信息
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqCommandsInfo(int nRequestId,JOrderInfo data,boolean isLast ,XtError error);
    
    /**
    * 资金划拨的回调函数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param error 错误信息
    * 当error返回报错时，error.errorMsg()包含转账失败原因
    */
    public abstract void onFundTransfer(int nRequestId, XtError error);
    
    /**
    * 股份划拨的回调函数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param error 错误信息
    * 当error返回报错时，error.errorMsg()包含转账失败原因
    */
    public abstract void onSecuTransfer(int nRequestId, XtError error);
    
    /**
    * 请求账号账号普通柜台资金的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 账号资金划拨普通柜台资金数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqComFund(String accountID, int nRequestId, JStockComFund data, boolean isLast, XtError error);

    /**
    * 请求账号账号普通柜台资金的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key
    * @param data 账号资金划拨普通柜台资金数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqComFundWithAccKey(String accountID, int nRequestId, String accountKey, JStockComFund data, boolean isLast, XtError error);
    
    /**
    * 请求账号普通柜台持仓的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 账号股份划拨普通柜台持仓数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqComPosition(String accountID, int nRequestId, JStockComPosition data, boolean isLast, XtError error);

    /**
    * 请求账号普通柜台持仓的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key
    * @param data 账号股份划拨普通柜台持仓数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqComPositionWithAccKey(String accountID, int nRequestId, String accountKey, JStockComPosition data, boolean isLast, XtError error);

    /**
    * 主推的算法母单错误信息
    * @param nOrderID 指令ID
    * @param strRemark 下单时填写的投资备注
    * @param error 错误信息
    */
    public abstract void onRtnAlgoError(int nOrderID, String strRemark, XtError error);
    
    /**
    * 请求当前交易日的回调函数
    * @param tradeDay 当前交易日
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param error 错误信息
    */
    public abstract void onReqTradeDay(String tradeDay, int nRequestId, XtError error);
    
    /**
    * 请求账号历史委托明细的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 账号委托明细数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqHistoryOrderDetail(String accountID, int nRequestId, JOrderDetail data, boolean isLast, XtError error);

    /**
    * 请求账号历史委托明细的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号key
    * @param data 账号委托明细数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqHistoryOrderDetailWithAccKey(String accountID, int nRequestId, String accountKey, JOrderDetail data, boolean isLast, XtError error);

    /**
    * 请求账号历史成交明细的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 账号成交明细数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqHistoryDealDetail(String accountID, int nRequestId, JDealDetail data, boolean isLast, XtError error);

    /**
    * 请求账号历史成交明细的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号key
    * @param data 账号成交明细数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqHistoryDealDetailWithAccKey(String accountID, int nRequestId, String accountKey, JDealDetail data, boolean isLast, XtError error);

    /**
    * 请求账号历史持仓统计的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 账号持仓统计数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqHistoryPositionStatics(String accountID, int nRequestId, JPositionStatics data, boolean isLast, XtError error);

    /**
    * 请求账号历史持仓统计的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号key
    * @param data 账号持仓统计数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqHistoryPositionStaticsWithAccKey(String accountID, int nRequestId, String accountKey, JPositionStatics data, boolean isLast, XtError error);

    /**
    * 请求期货账号保证金率的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号key
    * @param data 保证金率
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqFtAccCommissionRateDetail(String accountID, int nRequestId, String accountKey, JCommissionRateDetail data, XtError error);

    /**
    * 请求期货账号手续费率的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号key
    * @param data 手续费率
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqFtAccMarginRateDetail(String accountID, int nRequestId, String accountKey, JMarginRateDetail data, boolean isLast, XtError error);

    /**
    * 获取用户下所有的产品Id的回调函数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param nProductID 产品Id
    * @param accountKey 账号key
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    */
    public abstract void onReqProductIds(int nRequestId, int nProductID, String accountKey, boolean isLast);

    /**
    * 创建新投资组合的回调函数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param nPortfolioID 投资组合编号
    * @param strRemark 下单时填写的投资备注
    * @param error 错误信息
    * 当error返回报错时，error.errorMsg()包含下单失败原因
    */
    public abstract void onCreatePortfolio(int nRequestId, int nPortfolioID, String strRemark, XtError error);
    
    /**
    * 查询产品Id下所有的投资组合的回调函数
    * @param nProductID 产品ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 投资组合数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqProductPortfolio(int nProductID, int nRequestId, JPortfolioInfo data, boolean isLast, XtError error);
    
    /**
    * 请求投资组合委托信息的回调函数
    * @param nPortfolioID 投资组合ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 账号委托明细数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqPortfolioOrder(int nPortfolioID, int nRequestId, JOrderDetail data, boolean isLast, XtError error);

    /**
    * 请求投资组合一段时间内的委托信息的回调函数
    * @param nPortfolioID 投资组合ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 账号委托明细数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqPortfolioMultiOrder(int nPortfolioID, int nRequestId, JOrderDetail data, boolean isLast, XtError error);
    
    /**
    * 请求账号成交明细的回调函数
    * @param nPortfolioID 投资组合ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 账号成交明细数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqPortfolioDeal(int nPortfolioID, int nRequestId, JDealDetail data, boolean isLast, XtError error);

    /**
    * 请求投资组合一段时间内的成交信息的回调函数
    * @param nPortfolioID 投资组合ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 账号成交明细数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqPortfolioMultiDeal(int nPortfolioID, int nRequestId, JDealDetail data, boolean isLast, XtError error);
    
    /**
    * 请求投资组合持仓信息的回调函数
    * @param nPortfolioID 投资组合ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param data 账号持仓统计数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqPortfolioPos(int nPortfolioID, int nRequestId, JPositionStatics data, boolean isLast, XtError error);
    
    /**
    * 请求收益互换账号框架号的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号key
    * @param data 收益互换账号框架号数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqStrategyInfo(String accountID, int nRequestId, String accountKey, JStrategyInfo data, boolean isLast, XtError error);
  
    /**
    * 请求股东号的回调函数
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号key
    * @param data 股东号数据
    * @param isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
    * @param error 错误信息
    * 当error返回报错时，data内容不可用
    */
    public abstract void onReqSecuAccount(String accountID, int nRequestId, String accountKey, JSecuAccount data, boolean isLast, XtError error);

    /**
     * 市场状态信息回调
     * @param accountID 账号ID
     * @param nRequestId 客户自己维护的请求顺序ID
     * @param accountKey 账号key
     * @param data 市场状态信息
     * @param error 错误信息
     * 当error返回报错时，data内容不可用
     */
    public abstract void onReqExchangeStatus(String accountID, int nRequestId, String accountKey, ArrayList<JExchangeStatus>data, XtError error);

    /**
     * 请求用户资金流水的回调函数
     * @param accountID 账号ID
     * @param nRequestId 客户自己维护的请求顺序ID
     * @param accountKey 账号key
     * @param data 用户资金流水数据
     * @param error 错误信息
     * 当error返回报错时，data内容不可用
     */
    public abstract void onReqFundFlow(String accountID, int nRequestId, String accountKey, ArrayList<JFundFlow>data, XtError error);

    /**
     * 暂停指令的回调函数
     * @param  nRequestId 客户自己维护的请求顺序ID
     * @param  strRemark 下单时填写的投资备注，如果暂停的指令号不存在返回空
     * @param  error 错误信息
     * 当error返回报错时，error.errorMsg()包含撤单失败原因
     */
    public abstract void onPause(int nRequestId, String strRemark,  XtError error) ;

    /**
     *  恢复指令的回调函数
     * @param nRequestId 客户自己维护的请求顺序ID
     * @param strRemark 下单时填写的投资备注，如果恢复的指令号不存在返回空
     * @param error 错误信息
     *  error返回报错时，error.errorMsg()包含撤单失败原因
     */
    public abstract void onResume(int nRequestId, String strRemark,  XtError error) ;
}
