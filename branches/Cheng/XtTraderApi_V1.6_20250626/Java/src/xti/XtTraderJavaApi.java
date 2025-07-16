/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   XtTraderJavaApi.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti;

import xti.XtStructs.*;
import xti.XtError.XtError;
import java.util.ArrayList;
    /**
    * XtTraderJavaApi类<br>
    * nRequestId：数据请求ID，是数据请求和请求结果对应的标识<br>
    * 请求成功后的回调函数会传回请求函数的 nRequestId<br>
    * 只用资金帐号登录成功后才可以请求该帐号的相应数据
    */

public class XtTraderJavaApi{
    /**
    * 加载XtTraderJavaApi模块
    */
    static {
        String os = System.getProperty("os.name");
        if (os.startsWith("Windows"))
        {
            System.loadLibrary("libeay32");
            System.loadLibrary("ssleay32");
            System.loadLibrary("HsFutuSystemInfo");
            System.loadLibrary("WinDataCollect");
        }
        else
        {
            System.loadLibrary("HsFutuSystemInfo.x64");
            System.loadLibrary("LinuxDataCollect");
        }
        System.loadLibrary("XtTraderApi");
        System.loadLibrary("XtTraderJavaApi");
    }

    /**
     * 保存c++ api 实例指针
     */
    private long apiId;
    
    /**
     * api回调实现
     */
    private XtTraderJavaApiCallback callback;

    public long getApiId() {
        return this.apiId;
    }
    public void setApiId(long Id) {
        this.apiId = Id;
    }

    public void setCallback(XtTraderJavaApiCallback pCallback) {
        this.callback = pCallback;
        pCallback.setTraderApi(this);
        setNativeCallback(callback);
    }
    
    public XtTraderJavaApiCallback getCallback() {
        return this.callback;
    }

    /**
    * 获取XtTraderApi实例
    * @param address XtApiService监听端口
    * @return API实例
    */
    public static native XtTraderJavaApi  createXtTraderJavaApi(String address);

    /**
    * 设置数据回调对象
    * @param pCallback XtTraderApiCallback类实例
    */
    private native void setNativeCallback(XtTraderJavaApiCallback pCallback) ;
    
    /**
    * 创建api实例，并进行初始化
    * @param configFilePath 配置文件夹目录
    * @return 是否初始化成功
    */
    public native boolean init(String configFilePath);

    /**
    * 启动XTTraderApi线程，等待线程结束（需要客户主动结束程序）
    * 需要调用该函数阻塞线程，否则没有请求XtTraderApi实例会退出
    */
    public native void join();

	/**
	* 启动XtTraderApi单实例线程, 多实例情况必须调用joinAll()函数
	* 需要调用该函数阻塞线程，否则没有请求XtTraderApi实例会退出
	*/
    public native void joinAsync();
	
	
		/**
	* 异步启动XtTraderApi多实例线程, 多实例情况下必须使用该函数, 同时单实例也可调用该函数
	* 需要调用该函数阻塞线程，否则没有请求XtTraderApi实例会退出
	*/
	public native void joinAllAsync() ;	
	
	/**
    * 销毁api实例
    */		
    public native void destroy();
	
	/**
	* 销毁XtTraderApi多实例线程, 所有实例停止工作, joinAll()函数解除等待状态
	*/
    public native void destroyAll();
	
    /**
    * 获取迅投交易用户名
    * @return 用户名
    */
    public native String getUserName();

    /**
    * 获取Api版本
    * @return Api版本
    */
    public native String getVersion();

    /**
    * 根据账户Key获取产品ID
    * @param accountKey 账号key
    * @return 产品ID
    */
    public native int reqProductIdByAccountKey(String accountKey);

    /**
    * 用户登陆
    * 调用此函数后，回调 onUserLogin
    * @param userName 用户名
    * @param password 用户密码
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param machineInfo 如果需要下单设置站点信息，则传入，否则可以传空
    * @param appid 如果是期货中继模式，需传入监管处申请的appid，则传入，否则可以传空
    * @param authcode 如果是期货中继模式，需传入监管处申请的authcode，则传入，否则可以传空
    */
    public native void userLogin(String userName, String password, int nRequestId, String machineInfo, String appid, String authcode);

    /**
    * 用户登出，暂时无用
    * 调用此函数后，回调 onUserLogout
    * @param userName 用户名
    * @param password 用户密码
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void userLogout(String userName, String password, int nRequestId);

    /**
    * 请求账号资金信息
    * 调用此函数后，回调 onReqAccountDetail，两融账号还会回调onReqCreditAccountDetail
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void reqAccountDetail(String accountID, int nRequestId);
    
    /**
    * 请求账号资金信息
    * 调用此函数后，回调 onReqAccountDetail，两融账号还会回调onReqCreditAccountDetail
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void reqAccountDetail(String accountID, int nRequestId, String accountKey);

    /**
     * 同步请求账号资金信息
     * @param accountID 账号ID
     * @param error 错误信息，用于接收同步请求时的错误信息
     * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
     */
    public native JAccountDetail reqAccountDetailSync(String accountID, XtError error, String accountKey);

	/**
	* 同步请求产品下所有账号资金信息
	* @param error 错误信息，用于接收同步请求时的错误信息
	* @param productId 产品id
	*/
	public native ArrayList<JAccountDetail> reqAccountDetailSyncWithProductId(XtError error, int productId);

    /**
    * 请求账号委托明细信息
    * 调用此函数后，回调 onReqOrderDetail
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void reqOrderDetail(String accountID, int nRequestId);
    
    /**
    * 请求账号委托明细信息
    * 调用此函数后，回调 onReqOrderDetail
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void reqOrderDetail(String accountID, int nRequestId, String accountKey);

    /**
    * 根据指令号请求账号委托明细信息
    * 调用此函数后，回调 onReqOrderDetail
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param nOrderID 下单的指令号，可通过onRtnOrder和onOrder获得
    */
    public native void reqOrderDetail(String accountID, int nRequestId, int nOrderID);
    
    /**
    * 根据指令号请求账号委托明细信息
    * 调用此函数后，回调 onReqOrderDetail
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param nOrderID 下单的指令号，可通过onRtnOrder和onOrder获得
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void reqOrderDetail(String accountID, int nRequestId, int nOrderID, String accountKey);

    /**
     * 同步请求账号委托明细信息
     * @param accountID 账号ID
     * @param error 错误信息，用于接收同步请求时的错误信息
     * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
     */
    public native ArrayList<JOrderDetail> reqOrderDetailSync(String accountID, XtError error, String accountKey);

    /**
    * 请求账号成交明细信息
    * 调用此函数后，回调 onReqDealDetail
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void reqDealDetail(String accountID, int nRequestId);
    
    /**
    * 请求账号成交明细信息
    * 调用此函数后，回调 onReqDealDetail
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void reqDealDetail(String accountID, int nRequestId, String accountKey);

    /**
    * 根据指令号请求账号成交明细信息
    * 调用此函数后，回调 onReqDealDetail
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param nOrderID 下单的指令号，可通过onRtnOrder和onOrder获得
    */
    public native void reqDealDetail(String accountID, int nRequestId, int nOrderID);
    
    /**
    * 根据指令号请求账号成交明细信息
    * 调用此函数后，回调 onReqDealDetail
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param nOrderID 下单的指令号，可通过onRtnOrder和onOrder获得
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void reqDealDetail(String accountID, int nRequestId, int nOrderID, String accountKey);

    /**
     * 同步请求账号成交明细信息
     * @param accountID 账号ID
     * @param error 错误信息，用于接收同步请求时的错误信息
     * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
     */
    public native ArrayList<JDealDetail> reqDealDetailSync(String accountID, XtError error, String accountKey);

    /**
     * 同步请求账号成交统计信息
     * @param accountID 账号ID
     * @param error 错误信息，用于接收同步请求时的错误信息
     * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
     */
    public native ArrayList<JDealStatics> reqDealStaticsSync(String accountID, XtError error, String accountKey);

	/**
	* 同步请求产品下所有账号成交明细信息
	* 调用此函数后，回调 map<accountkey, std::vector<xti::CDealDetail>>结构
	* error 错误信息，用于接收同步请求时的错误信息
	* productId 产品ID
	*/
	public native ArrayList<JDealDetail> reqDealDetailSyncWithProductId( XtError error, int productId);

	/**
	* 同步请求产品下所有账号成交统计信息
	* 调用此函数后，回调 map<accountkey, std::vector<xti::CDealDetail>>结构
	* error 错误信息，用于接收同步请求时的错误信息
	* productId 产品ID
	*/
	public native ArrayList<JDealStatics> reqDealStaticsSyncWithProductId( XtError error, int productId);
		
    /**
    * 请求账号持仓明细信息
    * 调用此函数后，回调 onReqPositionDetail
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void reqPositionDetail(String accountID, int nRequestId);
    
    /**
    * 请求账号持仓明细信息
    * 调用此函数后，回调 onReqPositionDetail
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void reqPositionDetail(String accountID, int nRequestId, String accountKey);

    /**
     * 同步请求账号持仓明细信息 ，供期货使用
     * @param accountID 账号ID
     * @param error 错误信息，用于接收同步请求时的错误信息
     * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
     */
    public native ArrayList<JPositionDetail> reqPositionDetailSync(String accountID, XtError error, String accountKey);

    /**
    * 请求账号持仓统计信息
    * 调用此函数后，回调 onReqPositionStatics
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void reqPositionStatics(String accountID, int nRequestId);
    
    /**
    * 请求账号持仓统计信息
    * 调用此函数后，回调 onReqPositionStatics
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void reqPositionStatics(String accountID, int nRequestId, String accountKey);

    /**
     * 同步请求账号持仓统计信息
     * @param accountID 账号ID
     * @param error 错误信息，用于接收同步请求时的错误信息
     * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
     */
    public native ArrayList<JPositionStatics> reqPositionStaticsSync(String accountID, XtError error, String accountKey);

    /**
     * @brief 请求期货账号持仓统计信息
     * @note 调用此函数后，回调 onReqFuturePositionStatics
     * @param accountID 账号ID
     * @param nRequestId 客户自己维护的请求顺序ID
     * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
     */
    public native void reqFuturePositionStatics(String accountID, int nRequestId, String accountKey) ;

    /**
     * @brief 同步期货请求账号持仓统计信息
     * @note 调用此函数后，回调 CFuturePositionStatics
     * @param accountID 账号ID
     * @param error 错误信息，用于接收同步请求时的错误信息
     * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
     */
    public native ArrayList<JFuturePositionStatics>  reqFuturePositionStaticsSync(String accountID, XtError error, String accountKey) ;

    /**
    * 请求信用账号负债合约信息
    * 调用此函数后，回调 onReqStkcompacts
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void reqStkcompacts(String accountID, int nRequestId);
    
    /**
    * 请求信用账号负债合约信息
    * 调用此函数后，回调 onReqStkcompacts
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void reqStkcompacts(String accountID, int nRequestId, String accountKey);


    /**
    * 请求期权账号备兑持仓信息
    * 调用此函数后，回调 onReqCoveredStockPosition
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void reqCoveredStockPosition(String accountID, int nRequestId);
    
    /**
    * 请求期权账号备兑持仓信息
    * 调用此函数后，回调 onReqCoveredStockPosition
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void reqCoveredStockPosition(String accountID, int nRequestId, String accountKey);

    /**
    * 请求期权账号组合持仓信息
    * 调用此函数后，回调 onReqStkOptCombPositionDetail
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    * 
    */
    public native void reqStkOptCombPositionDetail(String accountID, int nRequestId, String accountKey);

    /**
    * 请求行情数据信息
    * 调用此函数后，回调 onReqPriceData
    * @param exchangeId 市场，取值参考MarketType.h
    * @param instrumentId 合约代码
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void reqPriceData(String exchangeId, String instrumentId, int nRequestId);

    /**
     * 请求行情数据信息 同步接口
     * 调用此函数后，回调 onReqPriceData
     * @param exchangeId 市场，取值参考MarketType.h
     * @param instrumentId 合约代码
     * @param error  错误信息，用于接收同步请求时的错误信息
     */
    public native JPriceData reqPriceDataSync(String exchangeId, String instrumentId, XtError error);

    /**
    * 请求用户产品信息
    * 调用此函数后，回调 onReqProductData
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void reqProductData(int nRequestId);
	
	/**
	* 请求用户产品信息同步接口
	* 调用此函数后，返回std::vector<xti::CProductData>结构
	* error 错误信息，用于接收同步请求时的错误信息
	*/
	public native ArrayList<JProductData> reqProductDataSync(XtError error) ;

    /**
    * 普通单下单，支持股票，期货，个股期权，期货期权，沪港通，深港通
    * 普通单，回调 onOrder
    * @param orderInfo 普通单请求参数
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void order(JOrdinaryOrder orderInfo, int nRequestId);
    
    /**
    * 普通单下单，支持股票，期货，个股期权，期货期权，沪港通，深港通
    * 普通单，回调 onOrder
    * @param orderInfo 普通单请求参数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void order(JOrdinaryOrder orderInfo, int nRequestId, String accountKey);

    /**
    * 直接下单，支持股票，期货，个股期权，期货期权，沪港通，深港通，只支持指定价普通下单
    * 普通单，回调 onDirectOrder
    * @param orderInfo 普通单请求参数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void directOrder(JOrdinaryOrder orderInfo, int nRequestId, String accountKey);
    
    /**
    * 组合算法单下单，只支持股票
    * 组合算法单，回调 onOrder
    * @param orderInfo 组合算法单请求参数
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void order(JGroupOrder orderInfo, int nRequestId);
    
    /**
    * 组合算法单下单，只支持股票
    * 组合算法单，回调 onOrder
    * @param orderInfo 组合算法单请求参数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    * 
    */
    public native void order(JGroupOrder orderInfo, int nRequestId, String accountKey);

    /**
    * 算法单下单，支持股票，期货，个股期权，期货期权，沪港通，深港通
    * 算法单，回调 onOrder
    * @param orderInfo 算法单请求参数
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void order(JAlgorithmOrder orderInfo, int nRequestId);
    
    /**
    * 算法单下单，支持股票，期货，个股期权，期货期权，沪港通，深港通
    * 算法单，回调 onOrder
    * @param orderInfo 算法单请求参数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void order(JAlgorithmOrder orderInfo, int nRequestId, String accountKey);

    /**
    * 组合智能算法单下单，支持股票，期货，个股期权，期货期权，沪港通，深港通
    * 组合智能算法单，回调 onOrder
    * @param orderInfo 组合智能算法单请求参数
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void order(JAlgGroupOrder orderInfo, int nRequestId);
    
    /**
    * 组合智能算法单下单，支持股票，期货，个股期权，期货期权，沪港通，深港通
    * 组合智能算法单，回调 onOrder
    * @param orderInfo 组合智能算法单请求参数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void order(JAlgGroupOrder orderInfo, int nRequestId, String accountKey);

    /**
    * 随机量交易下单，支持股票，期货，个股期权，期货期权，沪港通，深港通
    * 随机量交易单，回调 onOrder
    * @param orderInfo 随机量交易请求参数
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void order(JRandomOrder orderInfo, int nRequestId);
    
    /**
    * 随机量交易下单，支持股票，期货，个股期权，期货期权，沪港通，深港通
    * 随机量交易单，回调 onOrder
    * @param orderInfo 随机量交易请求参数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void order(JRandomOrder orderInfo, int nRequestId, String accountKey);

    /**
    * 智能算法下单，支持股票，期货，个股期权，期货期权，沪港通，深港通
    * 智能算法单，回调 onOrder
    * @param orderInfo 智能算法交易请求参数
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void order(JIntelligentAlgorithmOrder orderInfo, int nRequestId);
    
    /**
    * 智能算法下单，支持股票，期货，个股期权，期货期权，沪港通，深港通
    * 智能算法单，回调 onOrder
    * @param orderInfo 智能算法交易请求参数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void order(JIntelligentAlgorithmOrder orderInfo, int nRequestId, String accountKey);

    /**
    * 主动算法下单，支持股票，期货，个股期权，期货期权，沪港通，深港通
    * 主动算法单，回调 onOrder
    * @param orderInfo 主动算法交易请求参数
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void order(JExternAlgorithmOrder orderInfo, int nRequestId);
    
    /**
    * 主动算法下单，支持股票，期货，个股期权，期货期权，沪港通，深港通
    * 主动算法单，回调 onOrder
    * @param orderInfo 主动算法交易请求参数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void order(JExternAlgorithmOrder orderInfo, int nRequestId, String accountKey);

    /**
    * 组合外部算法单下单，支持股票，期货，个股期权，期货期权，沪港通，深港通
    * 组合外部算法单，回调 onOrder
    * @param orderInfo 组合外部算法单请求参数
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void order(JExternAlgGroupOrder orderInfo, int nRequestId);
    
    /**
    * 组合外部算法单下单，支持股票，期货，个股期权，期货期权，沪港通，深港通
    * 组合外部算法单，回调 onOrder
    * @param orderInfo 组合外部算法单请求参数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void order(JExternAlgGroupOrder orderInfo, int nRequestId, String accountKey);

    /**
    * 按指令号撤单
    * 撤销指令，终止某个单子的运行，回调 onCancel
    * @param orderID 下单的指令号，可通过onRtnOrder和onOrder获得
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void cancel(int orderID, int nRequestId);

    /**
    * 按委托号撤单
    * 撤销委托，终止某个单子的运行，回调 onCancelOrder
    * @param accountID 账号ID
    * @param orderSyeId 委托号，可通过onReqOrderDetail或者onRtnOrderDetail返回参数COrderDetail.m_strOrderSysID获得
    * @param exchangeId 委托对应的市场，可通过onReqOrderDetail或者onRtnOrderDetail返回参数COrderDetail.m_strExchangeID获得，有些柜台撤单需要送入市场和合约代码，没有特殊要求可以送空
    * @param instrumentId 委托对应的合约代码，可通过onReqOrderDetail或者onRtnOrderDetail返回参数COrderDetail.m_strInstrumentID获得，有些柜台撤单需要送入市场和合约代码，没有特殊要求可以送空
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void cancelOrder(String accountID, String orderSyeId, String exchangeId, String instrumentId, int nRequestId);
    
    /**
    * 按委托号撤单
    * 撤销委托，终止某个单子的运行，回调 onCancelOrder
    * @param accountID 账号ID
    * @param orderSyeId 委托号，可通过onReqOrderDetail或者onRtnOrderDetail返回参数COrderDetail.m_strOrderSysID获得
    * @param exchangeId 委托对应的市场，可通过onReqOrderDetail或者onRtnOrderDetail返回参数COrderDetail.m_strExchangeID获得，有些柜台撤单需要送入市场和合约代码，没有特殊要求可以送空
    * @param instrumentId 委托对应的合约代码，可通过onReqOrderDetail或者onRtnOrderDetail返回参数COrderDetail.m_strInstrumentID获得，有些柜台撤单需要送入市场和合约代码，没有特殊要求可以送空
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void cancelOrder(String accountID, String orderSyeId, String exchangeId, String instrumentId, int nRequestId, String accountKey);

    /**
    * 上传终端ctp采集信息，用于传入ctp柜台需要留痕的终端信息
    * @param accountID 账号ID
    * @param IpPortAddr 上传终端信息机器的ip和端口信息(格式为ip:port，例如127.0.0.1:58000)
    * @param len ctp采集信息内容的长度len，即CTP_GetSystemInfo入参nLen
    * @param CTPSystemInfo ctp采集到的内容
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    * 
    */
    public native void registerUserSystemInfo(String accountID, String IpPortAddr, int len, String CTPSystemInfo, int nRequestId, String accountKey);

    /**
    * 设置用户自己的定时器
    * 调用此函数后，回调 onCustomTimer
    * @param millsec 定时器间隔，单位ms
    */
    public native void startTimer(int millsec);

    /**
    * 停止用户自己的定时器
    */
    public native void stopTimer();

    /**
		* 设置用户自己的定时器
        * 调用此函数后，回调 onNamedTimer
        * timerName 定时器名称
        * intervalInMilliSecond 定时器间隔，单位毫秒
        * time 定时器第一次触发的时间，单位毫秒，如14点25分36秒789毫秒就是142536789，输入负数表示从当前时间开始计时
        * nextDay 触发的时间是否在下一日
    */
    public native void startNamedTimer(String timerName, int intervalInMilliSecond, int time, boolean nextDay);
	
	/**
        * 停止用户自己的定时器
        * timerName 定时器名称
        */
	public native void stopNamedTimer(String timerName);
		
    /**
    * 设置用户下单指令冻结选项
    * @param nCmdFrzCheckOption 用户下单指令冻结选项，1 禁止 2 警告
    */
    public native void setCmdFrzCheckOption(int nCmdFrzCheckOption);

    /**
    * 请求账号汇率信息
    * 调用此函数后，回调 onReqReferenceRate
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void reqGGTReferenceRate(String accountID, int nRequestId);
    
    /**
    * 请求账号汇率信息
    * 调用此函数后，回调 onReqReferenceRate
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void reqGGTReferenceRate(String accountID, int nRequestId, String accountKey);

    /**
    * 请求两融账号综合资金信息
    * 调用此函数后，回调 onReqCreditDetail
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    * 
    */
    public native void reqCreditDetail(String accountID, int nRequestId, String accountKey);

    /**
    * 订阅行情数据
    * code为"allCode"时，订阅整个市场，调用此函数后，回调 onSubscribQuote
    * @param data 订阅行情参数
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void subscribQuote(JSubscribData data, int nRequestId);

    /**
    * 退订行情数据
    * code为"allCode"时，订阅整个市场，调用此函数后，回调 onUnSubscribQuote
    * @param data 订阅行情参数
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void unSubscribQuote(JSubscribData data, int nRequestId);
    
    /**
    * 启用或者禁用指令级成交统计，在回调函数onRtnOderStat中获取成交统计信息，包括均价、已成交量、成交笔数等信息，
    * @param enableOrderStat 是否启用
    */
    public native void enableOrderStat(boolean enableOrderStat);

    /**
    * 是否启用撤指令后补撤委托，默认不启用。启用后,会主动对撤销过的指令发起委托明细查询，针对发起撤指令但对应委托未了结的委托进行撤委托操作，直到委托撤销或没撤掉成交，下游只用关心指令状态即可。本函数需在登录前调用。
    */
    public native void enableCmdCancelOrder();

    /**
     * 指令暂停恢复
     * @param op 指令暂停恢复请求
     * @param accountID 账号ID
     * @param nRequestId 客户自己维护的请求顺序ID
     * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
     */
    public native void operateTask(JTaskOpRecord op, String accountID, int nRequestId, String accountKey);

    /**
    * 智能算法指令改单
    * @param orderInfo 智能算法指令改单参数，m_strAccountID，m_strMarket，m_strInstrument和m_eOperationType不能改，其他的都能改
    * @param nOrderID 需要改参的指令号
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void modifyAlgoCommands(JIntelligentAlgorithmOrder orderInfo, int nOrderID, int nRequestId, String accountKey);

    /**
    * 普通算法指令改单
    * @param orderInfo 普通算法指令改单参数，只能改m_dPrice，m_nVolume，m_ePriceType，m_strRemark
    * @param nOrderID 需要改参的指令号
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void modifyAlgoCommands(JAlgorithmOrder orderInfo, int nOrderID, int nRequestId, String accountKey);

    /**
    * 请求账号新股额度信息
    * 调用此函数后，回调 onReqSubscribeInfo
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    * 
    */
    public native void reqSubscribeInfo(String accountID, int nRequestId, String accountKey);
    
    /**
    * 请求信用账号未了结负债信息
    * 调用此函数后，回调 onReqStkUnCloseCompact
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    * 
    */
    public native void reqStkUnCloseCompacts(String accountID, int nRequestId, String accountKey);
    
    /**
    * 请求信用账号已了结负债信息
    * 调用此函数后，回调 onReqStkClosedCompact
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    * 
    */
    public native void reqStkClosedCompacts(String accountID, int nRequestId, String accountKey);

    /**
     * 刷新信用账号未了结负债信息
     * 调用此函数后，主动向柜台同步未了结负债信息
     * @param accountID 账号ID
     * @param nRequestId 客户自己维护的请求顺序ID
     * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
     *
     */
    public native void refreshStkUnCloseCompacts(String accountID, int nRequestId, String accountKey);

    /**
     * 刷新信用账号已了结负债信息
     * 调用此函数后，主动向柜台同步已了结负债信息
     * @param accountID 账号ID
     * @param nRequestId 客户自己维护的请求顺序ID
     * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
     *
     */
    public native void refreshStkClosedCompacts(String accountID, int nRequestId, String accountKey);

    /**
    * 请求账号委托明细信息
    * 调用此函数后，回调 onReqOrderDetail
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    * 
    */
    public native void reqOrderDetailNew(String accountID, int nRequestId, String accountKey);

    /**
    * 请求账号成交明细信息
    * 调用此函数后，回调 onReqDealDetail
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    * 
    */
    public native void reqDealDetailNew(String accountID, int nRequestId, String accountKey);
    
    /**
    * 获取用户下所有账号key
    * 调用此函数后，回调 onReqAccountKey
    * @param nRequestId 客户自己维护的请求顺序ID
    * 
    */
    public native void reqAccountKeys(int nRequestId);

    /**
     * 根据委托号请求账号委托明细信息
     * 调用此函数后，回调 onReqOrderDetailBySysID
     * @param accountID 账号ID
     * @param nRequestId 客户自己维护的请求顺序ID
     * @param orderSyeId 委托号
     * @param exchangeId 委托所属市场
     * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
     *
     */
    public native void reqOrderDetailBySysID(String accountID, int nRequestId, String orderSyeId, String exchangeId, String accountKey);

    /**
     * 根据委托号请求账号委托明细信息 同步接口
     * 调用此函数后，返回 JOrderDetail
     * @param accountID 账号ID
     * @param error 错误信息，用于接收同步请求时的错误信息
     * @param orderSyeId 委托号
     * @param exchangeId 委托所属市场
     * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
     *
     */
    public native JOrderDetail reqOrderDetailBySysIDSync(String accountID, XtError error, String orderSyeId, String exchangeId, String accountKey);

    /**
    * 根据委托号请求账号成交明细信息
    * 调用此函数后，回调 onReqDealDetailBySysID
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param orderSyeId 委托号
    * @param exchangeId 委托所属市场
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    * 
    */
    public native void reqDealDetailBySysID(String accountID, int nRequestId, String orderSyeId, String exchangeId, String accountKey);

    /**
    * 请求账号结算单信息
    * 调用此函数后，回调 onReqDeliveryDetail
    * @param accountID 账号ID
    * @param startDate 查询开始时间
    * @param endDate 查询结束时间
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    * 
    */
    public native void reqDeliveryDetail(String accountID, String startDate, String endDate, int nRequestId, String accountKey);


    /**
     * 请求账号结算单信息
     * 调用此函数后，回调 onReqDeliveryDetail
     * @param accountID 账号ID
     * @param startDate 查询开始时间
     * @param endDate 查询结束时间
     * @param error 错误信息，用于接收同步请求时的错误信息
     * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
     */
    public native ArrayList<JDeliveryDetail> reqDeliveryDetailSync(String accountID, String startDate, String endDate, XtError error, String accountKey) ;

    /**
    * 请求账号合约行情信息
    * 调用此函数后，回调 onReqSingleInstrumentInfo
    * @param exchangeId 市场代码
    * @param instrumentId 合约代码
    * @param nRequestId 客户自己维护的请求顺序ID
    * 
    */
    public native void reqSingleInstrumentInfo(String exchangeId, String instrumentId, int nRequestId);
    
    /**
    * 请求账号可下单量
    * 调用此函数后，回调 onReqOpVolume
    * @param opVolumeReq 可下单量请求参数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    * 
    */
    public native void reqOpVolume(JOpVolumeReq opVolumeReq, int nRequestId, String accountKey);
    
    /**
    * 请求两融账号融券可融数量信息
    * 调用此函数后，回调 onReqCreditSloCode
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    * 
    */
    public native void reqCreditSloCode(String accountID, int nRequestId, String accountKey);
    
    /**
    * 请求两融账号融资融券标的信息
    * 调用此函数后，回调 onReqCreditSubjects
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    * 
    */
    public native void reqCreditSubjects(String accountID, int nRequestId, String accountKey);
    
    /**
    * 请求两融账号担保标的信息
    * 调用此函数后，回调 onReqCreditAssure
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    * 
    */
    public native void reqCreditAssure(String accountID, int nRequestId, String accountKey);
   
    /**
    * 请求账号银证转账银行信息
    * 调用此函数后，回调 onReqTransferBank
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    * 
    */
    public native void reqTransferBank(String accountID, int nRequestId, String accountKey);
    
    /**
    * 请求账号银证转账银行流水
    * 调用此函数后，回调 onReqTransferSerial
    * @param accountID 账号ID
    * @param startDate 查询开始时间
    * @param endDate 查询结束时间
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    * 
    */
    public native void reqTransferSerial(String accountID, String startDate, String endDate, int nRequestId, String accountKey);
    
    /**
    * 请求账号银证转账银行余额
    * 调用此函数后，回调 onReqBankAmount
    * @param bankInfo 银证转账银行余额请求参数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    * 
    */
    public native void reqBankAmount(JQueryBankInfo bankInfo, int nRequestId, String accountKey);
    
    /**
    * 银证转账
    * 调用此函数后，回调 onTransfer
    * @param transferReq 银证转账请求参数
    * @param nRequestId 客户自己银证转账维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    * 
    */
    public native void transfer(JTransferReq transferReq, int nRequestId, String accountKey);
    
    /**
    * 按市场请求合约信息
    * 调用此函数后，回调 onReqInstrumentInfoByMarket
    * @param exchangeId 市场，取值参考MarketType.h
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param tradable 是否只查询可交易合约，默认0,否， 1,是
    *
    */
    public native void reqInstrumentInfoByMarket(String exchangeId, int nRequestId, int tradable);

    /**
     * 按市场请求合约信息
     * @param exchangeId 市场，取值参考MarketType.h
     * @param error 错误信息，用于接收同步请求时的错误信息
     * @param tradable 是否只查询可交易合约，默认0,否， 1,是
     *
     */
    public native ArrayList<JInstrumentInfo> reqInstrumentInfoByMarketSync(String exchangeId, XtError error, int tradable);

    /**
    * 请求账号可撤单委托明细信息
    * 调用此函数后，回调 onReqCanCancelOrderDetail
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void reqCanCancelOrderDetail(String accountID, int nRequestId, String accountKey);

    /**
    * 请求用户所有下单信息
    * 调用此函数后，回调 onReqCommandsInfo
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void reqCommandsInfo(int nRequestId);
    
    /**
    * 资金划拨
    * 调用此函数后，回调 onFundTransfer
    * @param fundTransferReq 资金划拨请求参数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    * 
    */
    public native void fundTransfer(JSecuFundTransferReq fundTransferReq, int nRequestId, String accountKey);
    
    /**
    * 股份划拨
    * 调用此函数后，回调 onSecuTransfer
    * @param secuTransferReq 股份划拨请求参数
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    * 
    */
    public native void secuTransfer(JSecuFundTransferReq secuTransferReq, int nRequestId, String accountKey);

    /**
    * 请求账号普通柜台资金
    * 调用此函数后，回调 onReqComFund
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void reqComFund(String accountID, int nRequestId, String accountKey);
    
    /**
    * 请求账号普通柜台持仓
    * 调用此函数后，回调 onReqComPosition
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void reqComPosition(String accountID, int nRequestId, String accountKey);
    
    /**
    * 获取当前交易日
    * 调用此函数后，回调 onReqTradeDay
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void reqTradeDay(int nRequestId);
    
    /**
    * 请求账号历史委托明细
    * 调用此函数后，回调 onReqHistoryOrderDetail
    * @param accountID 账号ID
    * @param startDate 查询开始时间
    * @param endDate 查询结束时间
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    * 
    */
    public native void reqHistoryOrderDetail(String accountID, String startDate, String endDate, int nRequestId, String accountKey);
     
    /**
    * 请求账号历史成交明细
    * 调用此函数后，回调 onReqHistoryDealDetail
    * @param accountID 账号ID
    * @param startDate 查询开始时间
    * @param endDate 查询结束时间
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    * 
    */
    public native void reqHistoryDealDetail(String accountID, String startDate, String endDate, int nRequestId, String accountKey);
      
    /**
    * 请求账号历史持仓统计
    * 调用此函数后，回调 onReqHistoryPositionStatics
    * @param accountID 账号ID
    * @param startDate 查询开始时间
    * @param endDate 查询结束时间
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    * 
    */
    public native void reqHistoryPositionStatics(String accountID, String startDate, String endDate, int nRequestId, String accountKey);

    /**
    * 请求期货账号的保证金率
    * 调用此函数后，回调 onReqFtAccCommissionRateDetail
    * @param accountID 账号ID
    * @param exchangeId 市场，取值参考MarketType.h
    * @param instrumentId 合约代码
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    * 
    */
    public native void reqFtAccCommissionRateDetail(String accountID, String exchangeId, String instrumentId, int nRequestId, String accountKey);

    /**
    * 请求期货账号的手续费率
    * 调用此函数后，回调 onReqFtAccMarginRateDetail
    * @param accountID 账号ID
    * @param exchangeId 市场，取值参考MarketType.h
    * @param instrumentId 合约代码
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void reqFtAccMarginRateDetail(String accountID, String exchangeId, String instrumentId, int nRequestId, String accountKey);
       
    /**
    * 获取用户下所有的产品Id
    * 调用此函数后，回调 onReqProductIds
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void reqProductIds(int nRequestId);
        
    /**
    * 创建新投资组合
    * 调用此函数后，回调 onCreatePortfolio
    * @param newPortfolioReq 创建新投资组合请求参数
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void createPortfolio(JNewPortfolioReq newPortfolioReq, int nRequestId);

    /**
    * 查询产品Id下所有的投资组合
    * 调用此函数后，回调 onReqProductPortfolio
    * @param nProductID 产品ID,可以从onReqProductIds获取
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void reqProductPortfolio(int nProductID, int nRequestId);

    /**
    * 请求投资组合委托信息
    * 调用此函数后，回调 onReqPortfolioOrder
    * @param nPortfolioID 投资组合ID
    * @param nDate 查询日期
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void reqPortfolioOrder(int nPortfolioID, int nDate, int nRequestId);
  
    /**
    * 请求投资组合一段时间内的委托信息
    * 调用此函数后，回调 onReqPortfolioMultiOrder
    * @param nPortfolioID 投资组合ID
    * @param nFromDate 查询开始日期
    * @param nToDate 查询结束日期
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void reqPortfolioMultiOrder(int nPortfolioID, int nFromDate, int nToDate, int nRequestId);

    /**
    * 请求投资组合成交信息
    * 调用此函数后，回调 onReqPortfolioDeal
    * @param nPortfolioID 投资组合ID
    * @param nDate 查询日期
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void reqPortfolioDeal(int nPortfolioID, int nDate, int nRequestId);
  
    /**
    * 请求投资组合一段时间内的成交信息
    * 调用此函数后，回调 onReqPortfolioMultiDeal
    * @param nPortfolioID 投资组合ID
    * @param nFromDate 查询开始日期
    * @param nToDate 查询结束日期
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void reqPortfolioMultiDeal(int nPortfolioID, int nFromDate, int nToDate, int nRequestId);

    /**
    * 请求投资组合持仓信息
    * 调用此函数后，回调 onReqPortfolioPosition
    * @param nPortfolioID 投资组合ID
    * @param nDate 查询日期
    * @param nRequestId 客户自己维护的请求顺序ID
    */
    public native void reqPortfolioPosition(int nPortfolioID, int nDate, int nRequestId);

    /**
    * 请求收益互换账号框架号
    * 调用此函数后，回调 onReqStrategyInfo
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void reqStrategyInfo(String accountID, int nRequestId, String accountKey);
   
    /**
    * 请求股东号，用于多股东时指定股东号
    * 调用此函数后，回调 onReqSecuAccount
    * @param accountID 账号ID
    * @param nRequestId 客户自己维护的请求顺序ID
    * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
    */
    public native void reqSecuAccount(String accountID, int nRequestId, String accountKey);
	

	/**
	* 同步请求产品下所有账号历史成交明细
	* 调用此函数后，回调 CDealDetail结构
	* startDate 查询开始时间
	* endDate 查询结束时间
	* error 错误信息，用于接收同步请求时的错误信息
	* productId 产品ID
	*/
	public native ArrayList<JDealDetail> reqHistoryDealDetailSyncWithProductId(String startDate, String endDate, XtError error, int productId);

	/**
	* 同步请求产品下所有账号历史成交统计
	* 调用此函数后，回调 CDealStatics结构
	* startDate 查询开始时间
	* endDate 查询结束时间
	* error 错误信息，用于接收同步请求时的错误信息
	* productId 产品ID
	*/
	public native ArrayList<JDealStatics> reqHistoryDealStaticsSyncWithProductId(String startDate, String endDate, XtError error, int productId);
	
	/**
	* 同步请求产品下所有账号历史成交统计
	* 调用此函数后，回调 CPositionStatics结构
	* startDate 查询开始时间
	* endDate 查询结束时间
	* error 错误信息，用于接收同步请求时的错误信息
	* productId 产品ID
	*/
	public native ArrayList<JPositionStatics> reqHistoryPositionStaticsSyncWithProductId(String startDate, String endDate, XtError error, int productId);

    /**
     * 请求市场状态信息
     * 调用此函数后，回调 onReqExchangeStatus
     * @param accountID 账号ID
     * @param nRequestId 客户自己维护的请求顺序ID
     * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
     */
    public native void reqExchangeStatus(String accountID, int nRequestId, String accountKey);

    /**
     * 请求市场状态信息 同步接口
     * @param accountID 账号ID
     * @param error 错误信息，用于接收同步请求时的错误信息
     * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
     */
    public native ArrayList<JExchangeStatus> reqExchangeStatusSync(String accountID, XtError error, String accountKey);

    /**
     * 查询用户资金流水信息
     * @param accountID 账号ID
     * @param startDate 起始日期
     * @param endDate 终止日期
     * @param nRequestId 客户自己维护的请求顺序ID
     * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
     */
    public native void reqFundFlow(String accountID, String startDate, String endDate, int nRequestId, String accountKey);

    /**
     * 查询用户资金流水信息 同步接口
     * @param accountID 账号ID
     * @param startDate 起始日期
     * @param endDate 终止日期
     * @param error 错误信息，用于接收同步请求时的错误信息
     * @param accountKey 账号Key，用于区分不同类型的账号ID相同的账号
     */
    public native ArrayList<JFundFlow> reqFundFlowSync(String accountID, String startDate, String endDate, XtError error, String accountKey);

    /**
     *  按指令号暂停指令并暂停任务
     *  暂停指令，暂停某个单子的运行，回调 onPause
     * @param orderID 下单的指令号，可通过onRtnOrder和onOrder获得
     * @param  nRequestId 客户自己维护的请求顺序ID
     */
    public native void pause(int orderID, int nRequestId);

    /**
     * 按指令号暂停指令并暂停任务
     * 暂停指令，暂停某个单子的运行，回调 onPause
     * @param  orderID 下单的指令号，可通过onRtnOrder和onOrder获得
     * @param  error 错误信息，用于接收同步请求时的错误信息
     */
    public native void pauseSync(int orderID, XtError error) ;

    /**
     * 按指令号恢复指令并恢复任务
     * 恢复指令，恢复某个单子的运行，回调 onResume
     * @param orderID 下单的指令号，可通过onRtnOrder和onOrder获得
     * @param nRequestId 客户自己维护的请求顺序ID
     */
    public native void resume(int orderID, int nRequestId) ;

    /**
     * 按指令号恢复指令并恢复任务
     * 恢复指令，恢复某个单子的运行，回调 onResume
     * @param  orderID 下单的指令号，可通过onRtnOrder和onOrder获得
     * @param  error 错误信息，用于接收同步请求时的错误信息
     */
    public native void resumeSync(int orderID, XtError error);

    }
