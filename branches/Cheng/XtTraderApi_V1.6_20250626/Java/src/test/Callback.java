package test;

import xti.*;
import xti.XtDataType.*;
import xti.XtError.*;
//import xti.XtError.XtError;
import xti.XtStructs.*;
import java.util.Date;
import java.io.UnsupportedEncodingException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;

public class Callback extends XtTraderJavaApiCallback
{
    private XtTraderJavaApi m_client;
    private String m_strUserName;
    private String m_strPassWord;
    private String m_strAddress;
    private int m_nRequestId;    
    private String m_strStockAccount;   // 股票账号
    private String m_strStockAccountKey;   // 股票账号key
    private String m_strFutureAccount;  // 期货账号
    private String m_strOptionAccount;  // 股票期权账号
    private String m_strCreditAccount;  // 信用账号


    private boolean m_bUserLogined;
    private boolean m_bAccountLogined;

    public Callback(String address, String username, String password)
    {
    	m_strAddress = address;
    	m_strUserName = username;
    	m_strPassWord = password;
    	m_nRequestId = 0;
    	m_bUserLogined = false;
    	m_bAccountLogined = false;
    }

    public boolean init()
    {   	
        System.out.println(String.format("[init] trade server: %s, username: %s", m_strAddress, m_strUserName));
        // 创建api实例
        m_client = XtTraderJavaApi.createXtTraderJavaApi(m_strAddress);
        // 设置回调接口
        m_client.setCallback((XtTraderJavaApiCallback)this);
        // 启用指令成交统计功能
		m_client.enableOrderStat(true);
        // api初始化
        return m_client.init("../config");
    }
    
    public void join()
    {
    	m_client.join();
    }

    public void joinAsync()
    {
        m_client.joinAsync();
    }


    String makeCurTimestamp()
    {
        SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        return df.format(new Date());
    }
    
    String secondsToDateTime(int seconds)
    {
        SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");  
        return format.format(new Date(seconds * 1000L));  
    }
    
    public void testOrdinaryOrder(boolean isStock, String accountId)
    {
        if (isStock)
        {
            // 参数中所有char[]数组默认值都为空。
            JOrdinaryOrder orderInfo = new JOrdinaryOrder();
            // 资金账号，必填参数。不填会被api打回，并且通过onOrder反馈失败
            orderInfo.m_strAccountID = accountId;
            // 报单合约代码，必填字段。
            orderInfo.m_strInstrument = "000001";
            // 报单市场。必填字段。股票市场有"SH"/"SZ"，如果填空或填错都会被api直接打回
            orderInfo.m_strMarket = "SZ";
            // 报单委托量，必填字段。默认int最大值，填0或不填会被api打回
            orderInfo.m_nVolume = 100;
            // 报单委托类型。必填字段。根据相应的业务选择，默认为无效值(OPT_INVALID)。不填会被api打回
            orderInfo.m_eOperationType = EOperationType.OPT_BUY;
            // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
            orderInfo.m_dPrice = 12.85;  
            // 单笔超价百分比，选填字段。默认为0
            orderInfo.m_dSuperPriceRate = 0.1;
            // 报单价格类型，必填字段。默认为无效(PTRP_INVALID)，
            orderInfo.m_ePriceType=EPriceType.PRTP_MARKET ;
            // 直接还款的金额。仅直接还款用，信用业务类型专用
            orderInfo.m_dOccurBalance = 100.0;
            
            m_client.order(orderInfo, m_nRequestId++);
        }
        else
        {
            JOrdinaryOrder orderInfo = new JOrdinaryOrder();
            // 资金账号，必填参数。不填会被api打回，并且通过onOrder反馈失败
            orderInfo.m_strAccountID = accountId;
            // 报单合约代码，必填字段。
            orderInfo.m_strInstrument = "IF2106" ;
            // 报单市场。必填字段。如果填空或填错都会被api直接打回
            orderInfo.m_strMarket = "CFFEX";
            // 报单委托类型。必填字段。根据相应的业务选择，默认为无效值(OPT_INVALID)。不填会被api打回
            orderInfo.m_eOperationType = EOperationType.OPT_OPEN_LONG ;
            // 报单价格类型，必填字段。默认为无效(PTRP_INVALID)，
            orderInfo.m_ePriceType = EPriceType.PRTP_FIX ;
            // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
            orderInfo.m_dPrice = 5290.01;  
            // 单笔超价百分比，选填字段。默认为0
            orderInfo.m_dSuperPriceRate = 0.1;
            // 报单委托量，必填字段。默认int最大值，填0或不填会被api打回
            orderInfo.m_nVolume = 1;
            // 投机套保标志，选填字段。有"投机"/"套利"/"套保"方式。除期货三个方式都可选之外都是填“投机”。默认为“投机”
            orderInfo.m_eHedgeFlag = EHedgeFlagType.HEDGE_FLAG_SPECULATION;
            
            m_client.order(orderInfo , m_nRequestId++);
        }
    }
    
    public void testGroupOrder(String accountId)
    {
        // 组合下单， 只支持股票
        JGroupOrder orderInfo = new JGroupOrder();
        // 单笔超价
        orderInfo.m_orderParam.m_dSuperPriceRate = 0.05;
        // 报价类型
        orderInfo.m_orderParam.m_ePriceType = EPriceType.PRTP_LATEST;
        // 下单类型
        orderInfo.m_orderParam.m_eOperationType = EOperationType.OPT_BUY;
        // 超价起始笔数
        orderInfo.m_orderParam.m_nSuperPriceStart = 1;
        // 下单间隔(秒）
        orderInfo.m_orderParam.m_dPlaceOrderInterval = 30;
        // 撤单间隔（秒）
        orderInfo.m_orderParam.m_dWithdrawOrderInterval = 30;
        // 单笔下单比率(1 为一次全部下单）
        orderInfo.m_orderParam.m_dSingleVolumeRate = 1; 
        // 单笔下单基准
        orderInfo.m_orderParam.m_eSingleVolumeType = EVolumeType.VOLUME_FIX;
        // 最大下单次数
        orderInfo.m_orderParam.m_nMaxOrderCount = 100;
        // 单笔下单量最大值，必须大于或等于 m_nVolume[i] * m_dSingleVolumeRate
        // 否则，以单笔下单量最大值为准
        orderInfo.m_orderParam.m_nSingleNumMax = 1000;
        // 单笔下单量最小值, 不能比100 再小了
        orderInfo.m_orderParam.m_nLastVolumeMin = 100;
        // 资金账号，必填字段。如果不填写会被api打回
        orderInfo.m_orderParam.m_strAccountID = accountId;
        // 股票只数，必填参数，默认值为0。必须大于0，小于等于500
        orderInfo.m_nOrderNum = 5;
        // 合约代码， 必填字段。不填会被api打回
        orderInfo.m_strInstrument[0] =  "000001";
        orderInfo.m_strInstrument[1] =  "000002";
        orderInfo.m_strInstrument[2] =  "000004";
        orderInfo.m_strInstrument[3] =  "600000";
        orderInfo.m_strInstrument[4] =  "600016";
         // 市场，只有"SH"/"SZ"两个市场可以填写
        orderInfo.m_strMarket[0] = "SZ";
        orderInfo.m_strMarket[1] = "SZ";
        orderInfo.m_strMarket[2] = "SZ";
        orderInfo.m_strMarket[3] = "SH";
        orderInfo.m_strMarket[4] = "SH";
        // 报单数量
        orderInfo.m_nVolume[0] = 10000;
        orderInfo.m_nVolume[1] = 30000;
        orderInfo.m_nVolume[2] = 260000;
        orderInfo.m_nVolume[3] = 80000;
        orderInfo.m_nVolume[4] = 35000;
        // 说明：m_nOrderNum、m_strInstrument、m_strMarket、m_nVolume必须统一
        m_client.order(orderInfo, m_nRequestId++);
    }
    
    public void testAlgorithmOrder(String accountId)
    {
    	JAlgorithmOrder orderInfo = new JAlgorithmOrder();
    	
        // 资金账号，必填字段。如果不填写会被api打回
       orderInfo.m_strAccountID = accountId;

        // 单笔超价比率，必填字段。
        orderInfo.m_dSuperPriceRate = 0.2;  

        // 报单下撤单间隔，股票最小为10s，期货为0.5s
        orderInfo.m_dPlaceOrderInterval = 10; 
        orderInfo.m_dWithdrawOrderInterval = 10; 

        // 超价起始笔数，默认为1
        orderInfo.m_nSuperPriceStart = 1;

        // 报单量，必填字段。不可为0，默认值为无效值。不填或填0或被api打回
        orderInfo.m_nVolume = 100000;

        // 单笔下单比率，默认值为1，委托总量m_nVolume*单笔下单比率m_dSingleVolumeRate = 单笔下单量
        // 比如，下单总量1000 * 0.005 = 5 < 最小委托量100(限于股票)， 
        orderInfo.m_dSingleVolumeRate = 1;

        // 单笔下单最小值，默认为int型最大值。股票最小为100，期货最小为1
        orderInfo.m_nSingleNumMin = 100;

        // 单笔委托最大量，默认为int型最大值。最大可报100W
        // 如果 m_nVolume*m_dSingleVolumeRate > m_nMaxOrderCount，则以m_nMaxOrderCount为准
        orderInfo.m_nSingleNumMax = 1000; 

        // 尾单最小量
        orderInfo.m_nLastVolumeMin = 100;

        // 最大下单数
        orderInfo.m_nMaxOrderCount = 100;

        // 单笔基准：目标量、买1、买1+2、买1+2+3等，默认为目标量
        orderInfo.m_eSingleVolumeType = EVolumeType.VOLUME_FIX;

        // 投机套保标志，选填字段。有"投机"/"套利"/"套保"方式。除期货三个方式都可选之外都是填“投机”。默认为“投机”
        orderInfo.m_eHedgeFlag =EHedgeFlagType.HEDGE_FLAG_SPECULATION;

        // 市场，必填字段。应该填写MarketType.h里的，股票市场有"SH"/"SZ"，如果填空或填错都会被api直接打回
        orderInfo.m_strMarket="SH";

        // 合约代码，必填字段。
        orderInfo.m_strInstrument = "600000";

        // 报单委托类型。必填字段。根据相应的业务选择，默认为无效值(OPT_INVALID)。不填会被api打回
        orderInfo.m_eOperationType = EOperationType.OPT_BUY;

        // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
        orderInfo.m_dPrice = 9.60;

        // 报单价格类型，必填字段。默认为无效(PTRP_INVALID)
        orderInfo.m_ePriceType = EPriceType.PRTP_FIX;

        // 套利标志, 支持 投机、套利、套保（不填则默认为“投机”）
        orderInfo.m_eHedgeFlag = EHedgeFlagType.HEDGE_FLAG_SPECULATION;
        
        m_client.order(orderInfo, m_nRequestId++);
    }
    
    public void testIntelligentAlgorithmOrder(String accountId)
    {
    	JIntelligentAlgorithmOrder orderInfo = new JIntelligentAlgorithmOrder();
    	
         // 资金账号，必填字段。如果不填写会被api打回
        orderInfo.m_strAccountID = accountId;
        
        orderInfo.m_strOrderType = "TWAP";

        // 市场，必填字段。应该填写MarketType.h里的，股票市场有"SH"/"SZ"，如果填空或填错都会被api直接打回
        orderInfo.m_strMarket="SH";

        // 合约代码，必填字段。
        orderInfo.m_strInstrument = "600000";

        // 报单量，必填字段。不可为0，默认值为无效值。不填或填0或被api打回
        orderInfo.m_nVolume = 1000;

        // 报单委托类型。必填字段。根据相应的业务选择，默认为无效值(OPT_INVALID)。不填会被api打回
        orderInfo.m_eOperationType = EOperationType.OPT_BUY;

        // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
        orderInfo.m_dPrice = 9.60;

        // 报单价格类型，必填字段。默认为无效(PTRP_INVALID)
        orderInfo.m_ePriceType = EPriceType.PRTP_FIX;
        
        // 执行时间
        orderInfo.m_nValidTimeStart = (int)(System.currentTimeMillis() / 1000);
        orderInfo.m_nValidTimeEnd = orderInfo.m_nValidTimeStart + 1200;
        
        orderInfo.m_dOrderRateInOpenAcution = 0.5;
        orderInfo.m_dPriceOffsetBpsForAuction = 400;
        orderInfo.m_nStopTradeForOwnHiLow = EStopTradeForOwnHiLow.STOPTRADE_NO_BUY_SELL;
        
        //仅用卖出金额  0,1
        orderInfo.m_bOnlySellAmountUsed = true;
        //买卖偏差上限3-100.00
        orderInfo.m_dBuySellAmountDeltaPct = 3.0;
        
        orderInfo.m_strRemark = "test009";
        
        m_client.order(orderInfo, m_nRequestId++);
    }
    
    public void testAlgoGroupOrder(String accountId)
    {
        JAlgGroupOrder orderInfo = new JAlgGroupOrder();
        
         // 资金账号，必填字段。如果不填写会被api打回
    	orderInfo.m_orderParam.m_strAccountID = accountId;
        
    	orderInfo.m_orderParam.m_strOrderType = "SWITCH";

        // 报单委托类型。必填字段。根据相应的业务选择，默认为无效值(OPT_INVALID)。不填会被api打回
        //orderInfo.m_orderParam.m_eOperationType = EOperationType.OPT_BUY;

        // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
    	orderInfo.m_orderParam.m_dPrice = 9.60;

        // 报单价格类型，必填字段。默认为无效(PTRP_INVALID)
    	orderInfo.m_orderParam.m_ePriceType = EPriceType.PRTP_FIX;
        
        // 执行时间
    	orderInfo.m_orderParam.m_nValidTimeStart = (int)(System.currentTimeMillis() / 1000);
    	orderInfo.m_orderParam.m_nValidTimeEnd = orderInfo.m_orderParam.m_nValidTimeStart + 1200;
        
    	orderInfo.m_orderParam.m_dOrderRateInOpenAcution = 0.5;
    	orderInfo.m_orderParam.m_dPriceOffsetBpsForAuction = 400;
    	orderInfo.m_orderParam.m_nStopTradeForOwnHiLow = EStopTradeForOwnHiLow.STOPTRADE_NO_BUY_SELL;
    	
        //仅用卖出金额  0,1
        orderInfo.m_orderParam.m_bOnlySellAmountUsed = true;
        //买卖偏差上限3-100.00
        orderInfo.m_orderParam.m_dBuySellAmountDeltaPct = 3.0;
        
        //股票只数，必填参数，默认值为0。必须大于0，小于等于500
        orderInfo.m_nOrderNum = 4;
        
        // 合约代码， 必填字段。不填会被api打回
        orderInfo.m_strInstrument[0] =  "000002";
        orderInfo.m_strInstrument[1] = "600004";
        orderInfo.m_strInstrument[2] = "600000";
        orderInfo.m_strInstrument[3] = "300356";

        orderInfo.m_strMarket[0] = "SZ";
        orderInfo.m_strMarket[1] = "SH";
        orderInfo.m_strMarket[2] = "SH";
        orderInfo.m_strMarket[3] = "SZ";

        // 报单数量
        orderInfo.m_nVolume[0] = 1000;
        orderInfo.m_nVolume[1] = 1000;
        orderInfo.m_nVolume[2] = 1000;
        orderInfo.m_nVolume[3] = 1000;

        orderInfo.m_eOperationType[0] = EOperationType.OPT_BUY.value();
        orderInfo.m_eOperationType[1] = EOperationType.OPT_BUY.value();
        orderInfo.m_eOperationType[2] = EOperationType.OPT_SELL.value();
        orderInfo.m_eOperationType[3] = EOperationType.OPT_SELL.value();

        orderInfo.m_strRemark = "test008";
        
        m_client.order(orderInfo, m_nRequestId++);
    }
      
    public void testExternAlgGroupOrder(String accountId)
    {
        JExternAlgGroupOrder orderInfo = new JExternAlgGroupOrder();
        
         // 资金账号，必填字段。如果不填写会被api打回
    	orderInfo.m_orderParam.m_strAccountID = accountId;
        
    	orderInfo.m_orderParam.m_strOrderType = "VWAPPLUS";

        // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
    	orderInfo.m_orderParam.m_dPrice = 9.60;

        // 执行时间
    	orderInfo.m_orderParam.m_nValidTimeStart = (int)(System.currentTimeMillis() / 1000);
    	orderInfo.m_orderParam.m_nValidTimeEnd = orderInfo.m_orderParam.m_nValidTimeStart + 1200;
        
    	orderInfo.m_orderParam.m_nStopTradeForOwnHiLow = EStopTradeForOwnHiLow.STOPTRADE_NO_BUY_SELL;
    	
        //股票只数，必填参数，默认值为0。必须大于0，小于等于500
        orderInfo.m_nOrderNum = 4;
        
        // 合约代码， 必填字段。不填会被api打回
        orderInfo.m_strInstrument[0] =  "000002";
        orderInfo.m_strInstrument[1] = "600004";
        orderInfo.m_strInstrument[2] = "600000";
        orderInfo.m_strInstrument[3] = "300356";

        orderInfo.m_strMarket[0] = "SZ";
        orderInfo.m_strMarket[1] = "SH";
        orderInfo.m_strMarket[2] = "SH";
        orderInfo.m_strMarket[3] = "SZ";

        // 报单数量
        orderInfo.m_nVolume[0] = 1000;
        orderInfo.m_nVolume[1] = 1000;
        orderInfo.m_nVolume[2] = 1000;
        orderInfo.m_nVolume[3] = 1000;

        orderInfo.m_eOperationType[0] = EOperationType.OPT_BUY.value();
        orderInfo.m_eOperationType[1] = EOperationType.OPT_BUY.value();
        orderInfo.m_eOperationType[2] = EOperationType.OPT_SELL.value();
        orderInfo.m_eOperationType[3] = EOperationType.OPT_SELL.value();

        orderInfo.m_strRemark = "test009";
        
        m_client.order(orderInfo, m_nRequestId++);
    }
    
    public void testModifyAlgorithmOrder(int nOrderId, String accountID, String accountKey)
    {
    	JAlgorithmOrder orderInfo = new JAlgorithmOrder();
    	
        // 单笔超价比率，必填字段。
        orderInfo.m_dSuperPriceRate = 0.2;  

        // 报单下撤单间隔，股票最小为10s，期货为0.5s
        orderInfo.m_dPlaceOrderInterval = 10; 
        orderInfo.m_dWithdrawOrderInterval = 10; 

        // 超价起始笔数，默认为1
        orderInfo.m_nSuperPriceStart = 1;

        // 报单量，必填字段。不可为0，默认值为无效值。不填或填0或被api打回
        orderInfo.m_nVolume = 150000;

        // 单笔下单比率，默认值为1，委托总量m_nVolume*单笔下单比率m_dSingleVolumeRate = 单笔下单量
        // 比如，下单总量1000 * 0.005 = 5 < 最小委托量100(限于股票)， 
        orderInfo.m_dSingleVolumeRate = 1;

        // 单笔下单最小值，默认为int型最大值。股票最小为100，期货最小为1
        orderInfo.m_nSingleNumMin = 100;

        // 单笔委托最大量，默认为int型最大值。最大可报100W
        // 如果 m_nVolume*m_dSingleVolumeRate > m_nMaxOrderCount，则以m_nMaxOrderCount为准
        orderInfo.m_nSingleNumMax = 1000; 

        // 尾单最小量
        orderInfo.m_nLastVolumeMin = 100;

        // 最大下单数
        orderInfo.m_nMaxOrderCount = 100;

        // 单笔基准：目标量、买1、买1+2、买1+2+3等，默认为目标量
        orderInfo.m_eSingleVolumeType = EVolumeType.VOLUME_FIX;

        // 投机套保标志，选填字段。有"投机"/"套利"/"套保"方式。除期货三个方式都可选之外都是填“投机”。默认为“投机”
        orderInfo.m_eHedgeFlag =EHedgeFlagType.HEDGE_FLAG_SPECULATION;

        // 市场，必填字段。应该填写MarketType.h里的，股票市场有"SH"/"SZ"，如果填空或填错都会被api直接打回
        orderInfo.m_strMarket="SH";

        // 合约代码，必填字段。
        orderInfo.m_strInstrument = "600000";

        // 报单委托类型。必填字段。根据相应的业务选择，默认为无效值(OPT_INVALID)。不填会被api打回
        orderInfo.m_eOperationType = EOperationType.OPT_BUY;

        // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
        orderInfo.m_dPrice = 9.67;

        // 报单价格类型，必填字段。默认为无效(PTRP_INVALID)
        orderInfo.m_ePriceType = EPriceType.PRTP_FIX;

        // 套利标志, 支持 投机、套利、套保（不填则默认为“投机”）
        orderInfo.m_eHedgeFlag = EHedgeFlagType.HEDGE_FLAG_SPECULATION;
        
    	m_client.modifyAlgoCommands(orderInfo, nOrderId, m_nRequestId++, accountKey);
    }
    
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
    
    public void subQuote()
    {
        // 订阅行情信息
    	JSubscribData subscribData = new JSubscribData();
        // 平台
    	subscribData.m_nPlatformID = 11172;
        // 市场代码
    	subscribData.m_strExchangeID = "SH";
        // 合约代码,当其值为allCode时，订阅整个市场
    	subscribData.m_strInstrumentID = "600000";
        // 报盘状态
    	subscribData.m_eOfferStatus = EXTOfferStatus.XT_OFFER_STATUS_SP;

        m_client.subscribQuote(subscribData, m_nRequestId++);
    }
    
    @Override
    public void onConnected(boolean success, String errorMsg) 
    {
        System.out.println(String.format("[onConnected] connect %s", success ? "success" : "failure"));
        if (success)
        {
			// machineInfo代表"IP地址|mac地址|磁盘序列号|cpu号|主机名|磁盘信息|CPUID指令的ecx参数|主板信息"，如果相关字段无关，那就直接给个空值，忽略相应字段就好，两个字段间用分隔符'|'隔开。
            // machineInfo represent:"ip|mac|diskSerialNumber|cpuid|HostName|DiskInfo|cpuIdEx|biosId", If you don't need Specific field, just ignore it.
			String machineInfo = "192.168.1.172|5C-F9-DD-73-7C-83|0682056C|BFEBFBFF000206A7|DESKTOP-84OBV5E|C,NTFS,223|6VKJD3X";
			String appId = "";
			String authCode = "";
            m_client.userLogin(m_strUserName, m_strPassWord, ++m_nRequestId, machineInfo, appId, authCode);
        }
        else
        {
            System.out.println(String.format("[onConnected] err msg: %s, exit", errorMsg));
            System.exit(-1);
        }
    }    
    
    @Override
    public void onUserLogin(String userName, String password, int nRequestId, XtError error)
    {
        String errMsg;
        try
        {
            errMsg = new String(error.errorMsg().getBytes("GBK"));
        }
        catch(UnsupportedEncodingException e)
        {
            errMsg = error.errorMsg();
        }
        System.out.println("[onUserLogin] login " +(error.isSuccess() ? "success" : ("failure, err id: " + error.errorID() + ", err msg: " + errMsg)));
        String strUserName = m_client.getUserName();
        System.out.println("[onUserLogin] login " + strUserName);
        String strVersion = m_client.getVersion();
        System.out.println("[onUserLogin] login version:" +  strVersion);
//    	m_client.reqAccountDetail(m_strAccountId, m_nRequestId++);
//    	m_client.reqDealDetail(m_strAccountId, m_nRequestId++);
//    	m_client.reqPositionDetail(m_strAccountId, m_nRequestId++);
//    	m_client.reqPositionStatics(m_strAccountId, m_nRequestId++);
        //m_client.reqProductData(m_nRequestId++);
       
        if(error.isSuccess())
        {
        	m_bUserLogined = true;
        	if(m_bUserLogined && m_bAccountLogined)
        	{
        		doRequest();
        	}
        }     
    }
    
    public void doRequest()
    {
        System.out.println("doRequest");
//        m_client.reqOrderDetail("1016894", m_nRequestId++);
        //同步查询产品信息//
//         testReqProductDataSync();
//        //查询产品下资金账号资金信息
//    	testReqAccountDetailSyncWithProductId();
//        //同步查询产品下账号成交明细hhh
//    	testReqDealDetailSyncWithProductId();
//        //同步查询产品下成交统计
//    	testReqDealStaticsSyncWithProductId();
//        //同步查询产品下历史账号成交明细
//        testReqHistoryDealDetailSyncWithProductId();
//        //同步查询产品下历史成交统计
//        testReqHistoryDealStaticsSyncWithProductId();
//        //同步查询产品下历史持仓统计
//        testReqHistoryPositionStaticsSyncWithProductId();

        //异步查询产品信息
//        m_client.reqProductData(m_nRequestId++);

        //同步功能测试
//        reqAccountDetailSync();
//        reqOrderDetailSync();
//        reqDealDetailSync();
//        reqDealStaticsSync();
//        reqPositionDetailSync();
//        reqPositionStaticsSync();
//        reqExchangeStatusSync();
//        reqStkUnCloseCompacts();
//        reqPriceDataSync();
//        m_client.reqInstrumentInfoByMarket("SH", 100, 0);
//        reqInstrumentInfoByMarketSync();
//        reqFuturePositionStaticsSync();
//        reqFundFlow();
        reqFuturePositionStatics();

    }
    public void reqAccountDetailSync()
    {
        XtError error = new XtError();
        JAccountDetail detail= new JAccountDetail();
        detail= m_client.reqAccountDetailSync("2000463", error, "2____11172____60889____49____2000463____");
        if(error.isSuccess())
        {
            System.out.println("reqAccountDetailSync seccess");
            System.out.println(String.format("[reqAccountDetailSync] m_dAvailable: %f, m_strBrokerName: %s",
                    detail.m_dAvailable, detail.m_strBrokerName));
        }
        else
        {
            System.out.println(String.format("reqAccountDetailSync failed, errno: %d, errmsg: %s",
                    error.errorID(), error.errorMsg()));
        }
    }
    public void reqOrderDetailSync()
    {
        XtError error = new XtError();
        ArrayList<JOrderDetail> list = new ArrayList<JOrderDetail>();
        list= m_client.reqOrderDetailSync("2000463", error, "2____11172____60889____49____2000463____");
        if(error.isSuccess())
        {
            System.out.println("reqOrderDetailSync seccess");
            for(int i = 0; i <list.size(); ++i)
            {
                JOrderDetail detail = list.get(i);
                System.out.println(String.format("[reqOrderDetailSync] m_nOrderID: %d, m_strOrderSysID: %s ,m_nOrderPriceType: %s, m_eOffsetFlag: %s ",
                        detail.m_nOrderID, detail.m_strOrderSysID, detail.m_nOrderPriceType, detail.m_eOffsetFlag));
            }
        }
        else
        {
            System.out.println(String.format("reqOrderDetailSync failed, errno: %d, errmsg: %s",
                    error.errorID(), error.errorMsg()));
        }
    }

    public void reqDealDetailSync()
    {
        XtError error = new XtError();
        ArrayList<JDealDetail> list = new ArrayList<JDealDetail>();
        list= m_client.reqDealDetailSync("2000463", error, "2____11172____60889____49____2000463____");
        if(error.isSuccess())
        {
            System.out.println("reqDealDetailSync seccess");
            for(int i = 0; i <list.size(); ++i)
            {
                JDealDetail detail = list.get(i);
                System.out.println(String.format("[reqDealDetailSync] m_nOrderID: %d, m_strOrderSysID: %s, m_strTradeID: %s, m_nDirection: %s, m_nOffsetFlag: %s, m_nHedgeFlag: %s, m_nOrderPriceType: %s, m_eEntrustType: %s, m_eCoveredFlag: %s",
                        detail.m_nOrderID, detail.m_strOrderSysID, detail.m_strTradeID, detail.m_nDirection, detail.m_nOffsetFlag, detail.m_nHedgeFlag, detail.m_nOrderPriceType, detail.m_eEntrustType, detail.m_eCoveredFlag));
            }
        }
        else
        {
            System.out.println(String.format("reqDealDetailSync failed, errno: %d, errmsg: %s",
                    error.errorID(), error.errorMsg()));
        }
    }
    public void reqDealStaticsSync()
    {
        XtError error = new XtError();
        ArrayList<JDealStatics> list = new ArrayList<JDealStatics>();
        list= m_client.reqDealStaticsSync("2000463", error, "2____11172____60889____49____2000463____");
        if(error.isSuccess())
        {
            System.out.println("reqDealDetailSync seccess");
            for(int i = 0; i <list.size(); ++i)
            {
                JDealStatics detail = list.get(i);
                System.out.println(String.format("[reqDealDetailSync] m_nDirection: %s, m_nOffsetFlag: %s, m_nHedgeFlag: %s",
                        detail.m_nDirection, detail.m_nOffsetFlag, detail.m_nHedgeFlag));
            }
        }
        else
        {
            System.out.println(String.format("reqDealDetailSync failed, errno: %d, errmsg: %s",
                    error.errorID(), error.errorMsg()));
        }
    }



    public void reqPositionDetailSync()
    {
        XtError error = new XtError();
        ArrayList<JPositionDetail> list = new ArrayList<JPositionDetail>();
        list= m_client.reqPositionDetailSync("2000463", error, "2____11172____60889____49____2000463____");
        if(error.isSuccess())
        {
            System.out.println("reqPositionDetailSync seccess");
            for(int i = 0; i <list.size(); ++i)
            {
                JPositionDetail detail = list.get(i);
                System.out.println(String.format("[reqPositionDetailSync] m_nOrderID: %d, m_strInstrumentID: %s",
                        detail.m_nOrderID, detail.m_strInstrumentID));
            }
        }
        else
        {
            System.out.println(String.format("reqPositionDetailSync failed, errno: %d, errmsg: %s",
                    error.errorID(), error.errorMsg()));
        }
    }
    public void reqPositionStaticsSync()
    {
        XtError error = new XtError();
        ArrayList<JPositionStatics> list = new ArrayList<JPositionStatics>();
        list= m_client.reqPositionStaticsSync("2000463", error, "2____11172____60889____49____2000463____");
        if(error.isSuccess())
        {
            System.out.println("reqPositionStaticsSync seccess");
            for(int i = 0; i <list.size(); ++i)
            {
                JPositionStatics detail = list.get(i);
                System.out.println(String.format("[reqPositionStaticsSync] m_nPosition: %d, m_strInstrumentID: %s",
                        detail.m_nPosition, detail.m_strInstrumentID));
            }
        }
        else
        {
            System.out.println(String.format("reqPositionStaticsSync failed, errno: %d, errmsg: %s",
                    error.errorID(), error.errorMsg()));
        }
    }


    public void reqFuturePositionStatics() {
        m_client.reqFuturePositionStatics("1016894", 0, "1____21026____60066_1327____-1____1016894____");
        System.out.println("reqFuturePositionStatics ");
    }

    public void reqFuturePositionStaticsSync()
    {
        XtError error = new XtError();
        ArrayList<JFuturePositionStatics> list = new ArrayList<JFuturePositionStatics>();
        list= m_client.reqFuturePositionStaticsSync("1016894", error, "1____21026____60066_1327____-1____1016894____");
        if(error.isSuccess())
        {
            System.out.println("reqFuturePositionStaticsSync success");
            for(int i = 0; i <list.size(); ++i)
            {
                JFuturePositionStatics detail = list.get(i);
                System.out.println(String.format("[reqFuturePositionStaticsSync] m_nPosition: %d, m_strInstrumentID: %s",
                        detail.m_nPosition, detail.m_strInstrumentID));
            }
        }
        else
        {
            System.out.println(String.format("reqFuturePositionStaticsSync failed, errno: %d, errmsg: %s",
                    error.errorID(), error.errorMsg()));
        }
    }
    public void reqPriceDataSync()
    {
        XtError error = new XtError();
        JPriceData detail = new JPriceData();
        detail= m_client.reqPriceDataSync("SH", "600000", error);
        if(error.isSuccess())
        {
            System.out.println("reqPriceDataSync seccess");
            System.out.println(String.format("[reqPriceDataSync] , m_strInstrumentID: %s, m_dLastPrice: %f", detail.m_strInstrumentID,
                    detail.m_dLastPrice));
        }
        else
        {
            System.out.println(String.format("reqPriceDataSync failed, errno: %d, errmsg: %s",
                    error.errorID(), error.errorMsg()));
        }
    }

    public void reqInstrumentInfoByMarketSync()
    {
        XtError error = new XtError();
        ArrayList<JInstrumentInfo> list = new ArrayList<JInstrumentInfo>();
        int tradable = 1;
        list= m_client.reqInstrumentInfoByMarketSync("SH", error, 1 );
        if(error.isSuccess())
        {
            int size = list.size();
            System.out.println(String.format("reqInstrumentInfoByMarketSync seccess records: %d",  size));
            for(int i = 0; i <list.size(); ++i)
            {
                JInstrumentInfo detail = list.get(i);
//                if (detail.m_eExDivdendType == EXtExDivdendType.XT_EXD_RIGHT)
//                if (detail.m_eExDivdendType == EXtExDivdendType.XT_EXD_NORMAL)
                {
                    System.out.println(String.format("[reqInstrumentInfoByMarketSync] , m_strInstrumentID: %s, m_eSuspendedType：%s， m_eExDivdendType：%s， m_eStockType：%s",
                            detail.m_strInstrumentID,  detail.m_eSuspendedType, detail.m_eExDivdendType, detail.m_eStockType));
                }
            }
        }
        else
        {
            System.out.println(String.format("reqInstrumentInfoByMarketSync failed, errno: %d, errmsg: %s",
                    error.errorID(), error.errorMsg()));
        }
    }

    public void reqExchangeStatusSync()
    {
        XtError error = new XtError();
        ArrayList<JExchangeStatus> list = new ArrayList<JExchangeStatus>();
        list= m_client.reqExchangeStatusSync("2000463", error, "2____11172____60889____49____2000463____" );
        if(error.isSuccess())
        {
            System.out.println("reqExchangeStatusSync seccess");
            for(int i = 0; i <list.size(); ++i)
            {
                JExchangeStatus detail = list.get(i);
                System.out.println(String.format("[reqExchangeStatusSync] , m_strExchangeId: %s, m_eInstrumentStatus: %s", detail.m_strExchangeId,
                        detail.m_eInstrumentStatus));
            }
        }
        else
        {
            System.out.println(String.format("reqExchangeStatusSync failed, errno: %d, errmsg: %s",
                    error.errorID(), error.errorMsg()));
        }
    }
	public void testStartNamedTimer()
	{
		String timerName = "dealStaticsTimer";
		int intervalInMilliSecond = 10000;
		int time = -1;
		boolean nextDay = false;
		m_client.startNamedTimer(timerName,intervalInMilliSecond,time,nextDay);
	}
    @Override
    public void onNamedTimer(String timerName)
    {
        testReqDealStaticsSyncWithProductId();
    }
    public void testReqAccountDetailSyncWithProductId()
    {
    	XtError error = new XtError();
    	int produceId = 1333;
    	ArrayList<JAccountDetail> list = new ArrayList<JAccountDetail>();
    	list= m_client.reqAccountDetailSyncWithProductId(error, produceId);
    	if(error.isSuccess())
    	{
    		System.out.println("reqAccountDetailSyncWithProductId seccess");
    		for(int i = 0; i<list.size(); ++i)
    		{
    			JAccountDetail detail = list.get(i);
    			System.out.println(String.format("[JAccountDetail] m_nProductId: %d, m_strProductName: %s", 
    					detail.m_nProductId, detail.m_strProductName));
    		}
    	}
    	else
    	{
    		System.out.println(String.format("reqAccountDetailSyncWithProductId failed, errno: %d, errmsg: %s", 
					error.errorID(), error.errorMsg()));
    	}
    }
    public void testReqDealDetailSyncWithProductId()
    {
    	XtError error = new XtError();
    	int produceId = 1265;
    	ArrayList<JDealDetail> dealDetailList = new ArrayList<JDealDetail>();
    	dealDetailList= m_client.reqDealDetailSyncWithProductId(error, produceId);
    	if(error.isSuccess())
    	{
    		System.out.println("reqDealDetailSyncWithProductId seccess");
    		for(int i = 0; i<dealDetailList.size(); ++i)
    		{
    			JDealDetail dealDetail = dealDetailList.get(i);
    			System.out.println(String.format("[JDealDetail] m_strAccountID: %s, m_strInstrumentID: %s, m_nVolume: %d, m_strTradeID: %s, m_nDirection: %s",
    					dealDetail.m_strAccountID, dealDetail.m_strInstrumentID, dealDetail.m_nVolume, dealDetail.m_strTradeID, dealDetail.m_nDirection));
    		}
    	}
    	else
    	{
    		System.out.println(String.format("reqDealDetailSyncWithProductId failed, errno: %d, errmsg: %s", 
					error.errorID(), error.errorMsg()));
    	}
    }
    public void testReqDealStaticsSyncWithProductId()
    {
    	XtError error = new XtError();
    	int produceId = 1265;
    	ArrayList<JDealStatics> dealStaticList = new ArrayList<JDealStatics>();
    	dealStaticList= m_client.reqDealStaticsSyncWithProductId(error, produceId);
    	if(error.isSuccess())
    	{
    		System.out.println("reqDealStaticsSyncWithProductId seccess");
    		for(int i = 0; i<dealStaticList.size(); ++i)
    		{
    			JDealStatics dealStatics = dealStaticList.get(i);
    			System.out.println(String.format("[JDealStatics] m_strProductID: %s, m_strInstrumentID: %s, m_nVolume: %d, m_nDirection: %s",
    					dealStatics.m_strProductID, dealStatics.m_strInstrumentID, dealStatics.m_nVolume, dealStatics.m_nDirection));
    		}
    	}
    	else
    	{
    		System.out.println(String.format("reqDealStaticsSyncWithProductId failed, errno: %d, errmsg: %s", 
					error.errorID(), error.errorMsg()));
    	}
    }

    public void testReqHistoryDealDetailSyncWithProductId()
    {
        System.out.println("reqHistoryDealDetailSyncWithProductId started");
        XtError error = new XtError();
        int produceId = 1265;
        String startDate = "20231013";
        String endDate = "20231013";
        ArrayList<JDealDetail> dealDetailList = new ArrayList<JDealDetail>();
        dealDetailList= m_client.reqHistoryDealDetailSyncWithProductId(startDate, endDate, error, produceId);
        if(error.isSuccess())
        {
            System.out.println("reqHistoryDealDetailSyncWithProductId seccess");
            for(int i = 0; i<dealDetailList.size(); ++i)
            {
                JDealDetail dealDetail = dealDetailList.get(i);
                System.out.println(String.format("[JDealDetail] m_strTradeDate: %s, m_strAccountID: %s, m_strInstrumentID: %s, m_nVolume: %d, m_strTradeID: %s, m_nOffsetFlag: %s",
                        dealDetail.m_strTradeDate, dealDetail.m_strAccountID, dealDetail.m_strInstrumentID, dealDetail.m_nVolume, dealDetail.m_strTradeID, dealDetail.m_nOffsetFlag));
            }
        }
        else
        {
            System.out.println(String.format("reqHistoryDealDetailSyncWithProductId failed, errno: %d, errmsg: %s",
                    error.errorID(), error.errorMsg()));
        }
    }
    public void testReqHistoryDealStaticsSyncWithProductId()
    {
        XtError error = new XtError();
        int produceId = 1265;
        String startDate = "20231013";
        String endDate = "20231013";
        ArrayList<JDealStatics> dealStaticList = new ArrayList<JDealStatics>();
        dealStaticList= m_client.reqHistoryDealStaticsSyncWithProductId(startDate, endDate, error, produceId);
        if(error.isSuccess())
        {
            System.out.println("reqHistoryDealStaticsSyncWithProductId seccess");
            for(int i = 0; i<dealStaticList.size(); ++i)
            {
                JDealStatics dealStatics = dealStaticList.get(i);
                System.out.println(String.format("[JDealStatics] m_strProductID: %s, m_strInstrumentID: %s, m_nVolume: %d, m_nOffsetFlag: %s",
                         dealStatics.m_strProductID, dealStatics.m_strInstrumentID, dealStatics.m_nVolume, dealStatics.m_nOffsetFlag));
            }
        }
        else
        {
            System.out.println(String.format("reqHistoryDealStaticsSyncWithProductId failed, errno: %d, errmsg: %s",
                    error.errorID(), error.errorMsg()));
        }
    }

    public void testReqHistoryPositionStaticsSyncWithProductId()
    {
        XtError error = new XtError();
        int produceId = 1265;
        String startDate = "20231013";
        String endDate = "20231013";
        ArrayList<JPositionStatics> positionStaticList = new ArrayList<JPositionStatics>();
        positionStaticList= m_client.reqHistoryPositionStaticsSyncWithProductId(startDate, endDate, error, produceId);
        if(error.isSuccess())
        {
            System.out.println("reqHistoryPositionStaticsSyncWithProductId seccess");
            for(int i = 0; i<positionStaticList.size(); ++i)
            {
                JPositionStatics positionStatics = positionStaticList.get(i);
                System.out.println(String.format("[JPositionStatics] 账号m_strAccountID: %s, 合约m_strInstrumentID: %s, 持仓成本m_dPositionCost: %f, 持仓盈亏m_dPositionProfit:%f",
                         positionStatics.m_strAccountID, positionStatics.m_strInstrumentID, positionStatics.m_dPositionCost, positionStatics.m_dPositionProfit));
            }
        }
        else
        {
            System.out.println(String.format("reqHistoryPositionStaticsSyncWithProductId failed, errno: %d, errmsg: %s",
                    error.errorID(), error.errorMsg()));
        }
    }

    public void testReqProductDataSync()
    {
        XtError error = new XtError();
        ArrayList<JProductData> productDataList = new ArrayList<JProductData>();
        productDataList = m_client.reqProductDataSync(error);
        for(int i = 0; i<productDataList.size(); ++i)
        {
            JProductData productData = productDataList.get(i);
            System.out.println("[reqProductDataSync]"
                    + "\n    m_nProductId: " + productData.m_nProductId
                    + "\n    m_nProductName: " + productData.m_strProductName
                    + "\n    m_strProductCode:  "+ productData.m_strProductCode
                    + "\n    m_strCreateDate:  "+ productData.m_strCreateDate
                    + "\n    m_dBalance:  "+ productData.m_dBalance
                    + "\n    m_dStockValue:  "+ productData.m_dStockValue
                    + "\n    m_dLoanValue:  "+ productData.m_dLoanValue
                    + "\n    m_dFundValue:  "+ productData.m_dFundValue
                    + "\n    m_dTotalDebt: " + productData.m_dTotalDebt );
        }
        //可能有产品某些账号没有登录成功，这儿直接打印错误信息，里面有所有未登录成功的账号
        System.out.println("[reqProductDataSync]"
                    + "\n    errmsg: " + error.errorMsg());

    }
    @Override
    public void onRtnLoginStatus(String accountID, EBrokerLoginStatus status, int brokerType, String errorMsg)
    {
        String errMsg;
        try
        {
            errMsg = new String(errorMsg.getBytes("GBK"));
        }
        catch(UnsupportedEncodingException e)
        {
            errMsg = "";
        }
        //System.out.println(String.format("[onRtnLoginStatus] account: %s, type: %s, status: %s", 
        //        accountID, getAccountType(brokerType), (status == EBrokerLoginStatus.BROKER_LOGIN_STATUS_OK ? "success" : "failure, err: " + errMsg)));
                
//        switch (brokerType)
//        {
//            case 1:
//                m_strFutureAccount = accountID;
//                //testOrdinaryOrder(false, accountID);
//                break;
//            case 2:
//            	if (status == EBrokerLoginStatus.BROKER_LOGIN_STATUS_OK)
//                	m_strStockAccount = accountID;
//                //subQuote();
//                //testOrdinaryOrder(true, accountID);
//                //testGroupOrder(accountID);
//                //testAlgorithmOrder(accountID);
//                	//testIntelligentAlgorithmOrder(accountID);
//                break;
//            case 3:
//                m_strCreditAccount = accountID;
//                break;
//            case 6:
//                m_strOptionAccount = accountID;
//                break;
//            default:
//                break;
//        }
    }
    
    public String getAccountType(int brokerType)
    {
        switch (brokerType)
        {
            case 1:
                return "future";
            case 2:
                return "stock";
            case 3:
                return "credit";
            case 6:
                return "option";
            default:
                break;
        }
        return "unknown";
    }
    
    @Override
    public void onRtnLoginStatusWithActKey(String accountID, EBrokerLoginStatus status, int brokerType, String accountKey, String errorMsg)
    {
//        System.out.println(String.format("[onRtnLoginStatusWithActKey] account: %s, type: %s, status: %s",
//                accountID, getAccountType(brokerType), (status == EBrokerLoginStatus.BROKER_LOGIN_STATUS_OK ? "success" : "failure, err: " + errorMsg)));
        
    	switch (brokerType)
        {
        	case 1:
        		if (status == EBrokerLoginStatus.BROKER_LOGIN_STATUS_OK && accountID.equals("1016894") )
                    doRequest();
        			break;
            case 3:
//            	if (status == EBrokerLoginStatus.BROKER_LOGIN_STATUS_OK )
//            	{
//            		m_bAccountLogined = true;
//            		m_strStockAccount = accountID;
//            		m_strStockAccountKey = accountKey;
//                	if(m_bUserLogined && m_bAccountLogined)
//                	{
//                        doRequest();
//                	}
//            	}
            		
            		//m_client.reqAccountKeys(0);
                //testModifyAlgorithmOrder(11, accountID, accountKey);
            	//testModifyIntelligentAlgorithmOrder(12, accountID, accountKey);
                break;
            default:
            	break;
        }
    }

    @Override
    public void onRtnLoginStatusCustom(String accountID, EBrokerLoginStatus status, int brokerType, String accountKey, String userName, String errorMsg)
    {
    }
    
    @Override
    public void onUserLogout(String userName, String password, int nRequestId, XtError  error)  
    {
        System.out.println( "onUserLogout: " + (error.isSuccess()?" rtn success":(" ERR ID" + error.errorID() + " msg: " +error.errorMsg())));
    }
    
    @Override
    public void onReqAccountDetail(String accountID, int nRequestId, JAccountDetail   data, boolean isLast, XtError   error)
    {
        System.out.println("onReqAccountDetail:" + " isLast "+ isLast + (error.isSuccess()?" rtn  success":(" ERR ID" + error.errorID() + " msg: " +error.errorMsg())));
    }
    
    @Override
    public void onReqOrderDetail(String accountID, int nRequestId, JOrderDetail   data, boolean isLast, XtError   error)
    {
        System.out.println("onReqOrderDetail:" + " isLast "+ isLast + (error.isSuccess()?" rtn success":(" ERR ID" + error.errorID() + " msg: " +error.errorMsg())));
    }
    
    @Override
    public void onReqDealDetail(String accountID, int nRequestId, JDealDetail   data, boolean isLast, XtError   error)
    {
        System.out.println(String.format("[onReqDealDetail] m_nOrderID: %d, m_strOrderSysID: %s, m_strTradeID: %s",
                data.m_nOrderID, data.m_strOrderSysID, data.m_strTradeID));
//        System.out.println("onReqDealDetail:" + " isLast "+ isLast + (error.isSuccess()?" rtn success":(" ERR ID" + error.errorID() + " msg: " +error.errorMsg())));
    }
    
    @Override
    public void onReqPositionDetail(String accountID, int nRequestId, JPositionDetail   data, boolean isLast, XtError   error)
    {
        System.out.println("onReqPositionDetail:" + " isLast "+ isLast + (error.isSuccess()?" rtn success":(" ERR ID" + error.errorID() + " msg: " +error.errorMsg())));
    }
    
    @Override
    public void onReqPositionStatics(String accountID, int nRequestId, JPositionStatics  data, boolean isLast, XtError  error) 
    {
        System.out.println("onReqPositionStatics:" +  " isToday "+ data.m_bIsToday + " isLast "+ isLast + (error.isSuccess()?" rtn success":(" ERR ID" + error.errorID() + " msg: " +error.errorMsg())));
    }
    
    @Override
    public void onReqStksubjects(String accountID, int nRequestId, JStkSubjects data, boolean isLast, XtError error)
    {
        System.out.println("onReqStksubjects:" + " isLast "+ isLast + (error.isSuccess()?" rtn success":(" ERR ID" + error.errorID() + " msg: " +error.errorMsg())));
    }

    @Override
    public void onReqStkcompacts(String accountID, int nRequestId, JStkCompacts data, boolean isLast, XtError error)
    {
        System.out.println("onReqStkcompacts:" + " isLast "+ isLast + (error.isSuccess()?" rtn success":(" ERR ID" + error.errorID() + " msg: " +error.errorMsg())));
    }
    
    @Override
	public void onReqCreditAccountDetail(String accountID,int nRequestId, JCreditAccountDetail data,boolean isLast,XtError  error)
    {
    	 System.out.println("onReqCreditAccountDetail:" + " isLast "+ isLast + (error.isSuccess()?" rtn success":(" ERR ID" + error.errorID() + " msg: " +error.errorMsg())));
    }

	@Override
    public void onReqPriceData(int nRequestId, JPriceData data, XtError   error)
    {
        System.out.println("[onReqPriceData] OpenPrice: " + data.m_dOpenPrice );
    }
    
	@Override
	public void onRtnOrder(JOrderInfo data) {
		System.out.println("[onRtnOrder]"
				+ "\n    m_nOrderId: " + data.m_nOrderID
				+ "\n    m_startTime: " + secondsToDateTime(data.m_startTime)
				+ "\n    m_eOrderStatus: " + data.m_eStatus
				+ "\n    m_strMsg: " + data.m_strMsg);
	}
	
    /**
    * 指令成交统计信息（指令）
    */
	@Override
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
	
	@Override
    public void onRtnOrderDetail(JOrderDetail   data)
    {
        if (data.m_nErrorID  == 0)
        {
            System.out.println("[onRtnOrderDetail]"
                    + "\n    instrumentID: "+ data.m_strInstrumentID
                    + "\n    m_nOrderStatus:  " + data.m_eOrderStatus 
                    + "\n    m_nOrderID: " + data.m_nOrderID 
                    + "\n    time: " + data.m_strInsertDate + " " + data.m_strInsertTime
                    + "\n    m_nVolumeTraded: " + data.m_nTradedVolume 
                    + "\n    m_dTradeAmount: "  + data.m_dTradeAmount  
                    + "\n    m_nTotalVolume: " + data.m_nTotalVolume);
        }
        else
        {
            System.out.println("[onRtnOrderDetail] Failure, 涓嬪崟ID锟� "+ data.m_nOrderID  
                    + "\n        , ErrorID: " + data.m_nErrorID  
                    + "\n        , ErrorMsg: " + data.m_strErrorMsg  );
        }
    }
    
    @Override
    public void onRtnDealDetail(JDealDetail data)
    {
        System.out.println("[onRtnDealDetail] "
            + "\n  指令ID: " + data.m_nOrderID 
            + "\n  成交编号: " + data.m_strTradeID  
            + "\n  市场: " + data.m_strExchangeID
            + "\n  代码: " + data.m_strInstrumentID 
            + "\n  成交量: " + data.m_nVolume
            + "\n  成交均价: " + data.m_dAveragePrice
            + "\n  资金账号: " + data.m_strAccountID 
            + "\n  time: " + makeCurTimestamp());
    }
    
    @Override
    public void onRtnOrderError(JOrderError data)
    {
        String errMsg;
        try
        {
            errMsg = new String(data.m_strErrorMsg.getBytes("gbk"));
        }
        catch(UnsupportedEncodingException e)
        {
            errMsg = data.m_strErrorMsg;
        }
        
        System.out.println("[onRtnOrderError]"
            + "\n    errorId: " + data.m_nErrorID 
            + "\n    errorMsg: " + errMsg 
            + "\n    m_nOrderID:" + data.m_nOrderID );
    }
    
    @Override
    public void onRtnCancelError(JCancelError data)
    {
        System.out.println("[onRtnCancelError] OrderId: " + data.m_nOrderID  + ", ErrorId: " + data.m_nErrorID  + ", errorMsg: " + data.m_strErrorMsg );
    }
    
    @Override
    public void onRtnAccountDetail(String accountID, JAccountDetail  accountDetail)
    {
//        System.out.println("[onRtnAccountDetail]"); 
//                + "\n    m_strOpenDate: " + accountDetail.m_strStatus 
//                + "\n    m_strOpenDate:  "+ accountDetail.m_strOpenDate  
//                + "\n    m_dFrozenMargin: " + accountDetail.m_dFrozenMargin );
    }
    
    @Override
    public void onRtnCreditAccountDetail(String accountID, JCreditAccountDetail creditAccountDetail)
    {
//      System.out.println("[onRtnCreditAccountDetail]"); 
//      		+ "\n    m_dPerAssurescaleValue: " + creditAccountDetail.m_dPerAssurescaleValue 
//      		+ "\n    m_dEnableBailBalance:  "+ creditAccountDetail.m_dEnableBailBalance  
//      		+ "\n    m_dUsedBailBalance: " + creditAccountDetail.m_dUsedBailBalance );
    }
	@Override
	public void onReqProductData(int nRequestId, JProductData productData,boolean isLast, XtError error)
	{
        if (error.isSuccess())
        {
            System.out.println("[onReqProductData]"
            + "\n    m_nProductId: " + productData.m_nProductId
            + "\n    m_nProductName: " + productData.m_strProductName
            + "\n    m_dLoanValue:  "+ productData.m_dLoanValue
            + "\n    m_dFundValue: " + productData.m_dFundValue );
        }
        else
        {
            System.out.println("[onReqProductData]"
                    + "\n    errmsg: " + error.errorMsg());
        }
	}
    
	@Override
	public void onRtnNetValue(JNetValue data) {
	}
	
	@Override
    public void onOrder(int nRequestId, int orderID, String strRemark, XtError  error)
    {
    	if(error.isSuccess())
    	{
    		System.out.println("[onOrder] success.  order id: " + orderID); 	
    	}
    	else
    	{
            System.out.println("[onOrder] failure.  order id: " + orderID + ", request id: " + nRequestId + ", error msg: " + error.errorMsg());
    	}
    }
    
    @Override
    public void onCancel(int nRequestId, XtError  error)
    {
        System.out.println("[ onCancel ] isSuccess: " + (error.isSuccess()?"true":"false")+
                 "\ntime: " + makeCurTimestamp()
            + "\nRequestId: " + nRequestId + ", ErrorId: " + error.errorID() + ", errorMsg: " + error.errorMsg());
    }

    @Override
    public void onCancelWithRemark(int nRequestId, String strRemark, XtError  error)
    {
        System.out.println("[ onCancelWithRemark ] isSuccess: " + (error.isSuccess()?"true":"false")+
                 "\ntime: " + makeCurTimestamp()
            + "\nRequestId: " + nRequestId + ", ErrorId: " + error.errorID() + ", errorMsg: " + error.errorMsg());
    }

    @Override
    public void onCancelOrder(int nRequestId, XtError  error)
    {
        System.out.println("[ onCancelOrder ] isSuccess: " + (error.isSuccess()?"true":"false")+
                 "\ntime: " + makeCurTimestamp()
            + "\nRequestId: " + nRequestId + ", ErrorId: " + error.errorID() + ", errorMsg: " + error.errorMsg());
    }
    
	@Override
	public void onReqCoveredStockPosition(String accountID, int nRequestId,
			JCoveredStockPosition data, boolean isLast, XtError error) {
		System.out.println("[onReqCoveredStockPosition]"
		+ "\n    m_dPerAssurescaleValue: " + data.m_strAccountID 
		+ "\n    m_dEnableBailBalance:  "+ data.m_strExchangeName  
		+ "\n    m_dUsedBailBalance: " + data.m_strInstrumentID );
		
	}

	

    @Override
    public void onCustomTimer() {
        // TODO Auto-generated method stub
        
    }

    
    public void onReqReferenceRate(String accountID,int nRequestId, JReferenceRate data,boolean isLast,XtError  error)
    {
         System.out.println("onReqReferenceRate:" + " isLast "+ isLast + (error.isSuccess()?" rtn success":(" ERR ID" + error.errorID() + " msg: " +error.errorMsg())));
    }

    public void onReqCreditDetail(String accountID,int nRequestId, JCreditDetail data,boolean isLast,XtError  error)
    {
         System.out.println("onReqCreditDetail:" + " isLast "+ isLast + (error.isSuccess()?" rtn success":(" ERR ID" + error.errorID() + " msg: " +error.errorMsg())));
    }

	@Override
	public void onReqStkOptCombPositionDetail(String accountID, int nRequestId, JStockOptionCombPositionDetail data,
			boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onSubscribQuote(int nRequestId, JSubscribData data, XtError error) {
		// TODO Auto-generated method stub
        System.out.println("onSubscribQuote:" + " mkt: " + data.m_strExchangeID + " code: " +data.m_strInstrumentID);
	}

	@Override
	public void onUnSubscribQuote(int nRequestId, JSubscribData data, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onRtnPriceData(JPriceData data) {
		// TODO Auto-generated method stub
        System.out.println("onRtnPriceData:" + " mkt: " + data.m_strExchangeID + " code: " +data.m_strInstrumentID + " price: " +data.m_dLastPrice);	
	}

	@Override
	public void onOperateTask(String accountID, int nRequestId, String accountKey, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onModifyAlgoCommands(int nRequestId, int orderID, String strRemark, XtError error) {
		if(error.isSuccess())
    	{
    		System.out.println("[onModifyAlgoCommands] success.  order id: " + orderID); 	
    	}
    	else
    	{
            System.out.println("[onModifyAlgoCommands] failure.  order id: " + orderID + ", request id: " + nRequestId + ", error msg: " + error.errorMsg());
    	}
	}

	@Override
	public void onReqSubscribeInfo(String accountID, int nRequestId, JSubscribeInfo data, boolean isLast,
			XtError error) {
		System.out.println("onReqSubscribeInfo:" + " isLast "+ isLast + (error.isSuccess()?" rtn success":(" ERR ID" + error.errorID() + " msg: " +error.errorMsg())));
	}

    public void reqStkUnCloseCompacts()
    {
        System.out.println("reqStkUnCloseCompacts" );
        m_client.reqStkUnCloseCompacts("3000084",100, "");
    }

	@Override
	public void onReqStkUnCloseCompact(String accountID, int nRequestId, JStkUnClosedCompacts data, boolean isLast,
			XtError error) {
		// TODO Auto-generated method stub
        System.out.println("onReqStkUnCloseCompact" );
	}

	@Override
	public void onReqStkClosedCompact(String accountID, int nRequestId, JStkClosedCompacts data, boolean isLast,
			XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqAccountKey(int nRequestId, JAccountKey data, boolean isLast, XtError error) {
		System.out.println("onReqAccountKey:" + " accountId "+ data.m_strAccountID  + " isLast "+ isLast + (error.isSuccess()?" rtn success":(" ERR ID" + error.errorID() + " msg: " +error.errorMsg())));
	}

	@Override
	public void onReqDealDetailBySysID(String accountID, int nRequestId, String orderSyeId, String exchangeId,
			JDealDetail data, boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqDeliveryDetail(String accountID, int nRequestId, JDeliveryDetail data, boolean isLast,
			XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqSingleInstrumentInfo(int nRequestId, JInstrumentInfo data, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onRtnExchangeStatus(JExchangeStatus data) {
		// TODO Auto-generated method stub
		
	}
	@Override
	public void onRtnCreditDetail(JCreditDetail data) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqOpVolume(String accountID,int nRequestId, String dataKey,int nVolume, boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqCreditSloCode(String accountID, int nRequestId, JCreditSloCode data, boolean isLast,
			XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqCreditSubjects(String accountID, int nRequestId, JCreditSubjects data, boolean isLast,
			XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqCreditAssure(String accountID, int nRequestId, JCreditAssure data, boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqTransferBank(String accountID, int nRequestId, JQueryBankInfo data, boolean isLast,
			XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqTransferSerial(String accountID, int nRequestId, JTransferSerial data, boolean isLast,
			XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqBankAmount(String accountID, int nRequestId, JQueryBankAmount data, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onTransfer(int nRequestId, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqInstrumentInfoByMarket(int nRequestId, JInstrumentInfo data, boolean isLast, XtError error) {
		// TODO Auto-generated method stub
        System.out.println(String.format("[reqInstrumentInfoByMarketSync] , m_strInstrumentID: %s, m_strInstrumentName: %s， m_eProductClass：%s， m_eMaxMarginSideAlgorithm：%s， m_eSuspendedType：%s， m_eExDivdendType：%s， m_eStockType：%s",
                data.m_strInstrumentID, data.m_strInstrumentName, data.m_eProductClass, data.m_eMaxMarginSideAlgorithm, data.m_eSuspendedType, data.m_eExDivdendType, data.m_eStockType));

	}

	@Override
	public void onReqCanCancelOrderDetail(String accountID, int nRequestId, JOrderDetail data, boolean isLast,
			XtError error) {
		// TODO Auto-generated method stub
		
	}

    @Override
    public void onReqCommandsInfo(int nRequestId,JOrderInfo data,boolean isLast ,XtError error)
    {
        // TODO Auto-generated method stub
        System.out.println("[onReqCommandsInfo] enter");
    }

	@Override
	public void onFundTransfer(int nRequestId, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onSecuTransfer(int nRequestId, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqComFund(String accountID, int nRequestId, JStockComFund data, boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqComPosition(String accountID, int nRequestId, JStockComPosition data, boolean isLast,
			XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onRtnAlgoError(int nOrderID, String strRemark, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqTradeDay(String tradeDay, int nRequestId, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqHistoryOrderDetail(String accountID, int nRequestId, JOrderDetail data, boolean isLast,
			XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqHistoryDealDetail(String accountID, int nRequestId, JDealDetail data, boolean isLast,
			XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqHistoryPositionStatics(String accountID, int nRequestId, JPositionStatics data, boolean isLast,
			XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqInstrumentInfoByMarketWithMkt(int nRequestId, String exchangeId, JInstrumentInfo data,
			boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqAccountDetailWithAccKey(String accountID, int nRequestId, String accountKey, JAccountDetail data,
			boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqOrderDetailWithAccKey(String accountID, int nRequestId, String accountKey, JOrderDetail data,
			boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqDealDetailWithAccKey(String accountID, int nRequestId, String accountKey, JDealDetail data,
			boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqPositionDetailWithAccKey(String accountID, int nRequestId, String accountKey, JPositionDetail data,
			boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqPositionStaticsWithAccKey(String accountID, int nRequestId, String accountKey,
			JPositionStatics data, boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqStksubjectsWithAccKey(String accountID, int nRequestId, String accountKey, JStkSubjects data,
			boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqStkcompactsWithAccKey(String accountID, int nRequestId, String accountKey, JStkCompacts data,
			boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqCoveredStockPositionWithAccKey(String accountID, int nRequestId, String accountKey,
			JCoveredStockPosition data, boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqStkOptCombPositionDetailWithAccKey(String accountID, int nRequestId, String accountKey,
			JStockOptionCombPositionDetail data, boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqCreditAccountDetailWithAccKey(String accountID, int nRequestId, String accountKey,
			JCreditAccountDetail data, boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}


	@Override
	public void onReqReferenceRateWithAccKey(String accountID, int nRequestId, String accountKey, JReferenceRate data,
			boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqCreditDetailWithAccKey(String accountID, int nRequestId, String accountKey, JCreditDetail data,
			boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqSubscribeInfoWithAccKey(String accountID, int nRequestId, String accountKey, JSubscribeInfo data,
			boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqStkUnCloseCompactWithAccKey(String accountID, int nRequestId, String accountKey,
			JStkUnClosedCompacts data, boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqStkClosedCompactWithAccKey(String accountID, int nRequestId, String accountKey,
			JStkClosedCompacts data, boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqDealDetailBySysIDWithAccKey(String accountID, int nRequestId, String accountKey, String orderSyeId,
			String exchangeId, JDealDetail data, boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqDeliveryDetailWithAccKey(String accountID, int nRequestId, String accountKey, JDeliveryDetail data,
			boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqOpVolumeWithAccKey(String accountID, int nRequestId, String accountKey, String dataKey,
			int nVolume, boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqCreditSloCodeWithAccKey(String accountID, int nRequestId, String accountKey, JCreditSloCode data,
			boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqCreditSubjectsWithAccKey(String accountID, int nRequestId, String accountKey, JCreditSubjects data,
			boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqCreditAssureWithAccKey(String accountID, int nRequestId, String accountKey, JCreditAssure data,
			boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqTransferBankWithAccKey(String accountID, int nRequestId, String accountKey, JQueryBankInfo data,
			boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqTransferSerialWithAccKey(String accountID, int nRequestId, String accountKey, JTransferSerial data,
			boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqBankAmountWithAccKey(String accountID, int nRequestId, String accountKey, JQueryBankAmount data,
			XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqCanCancelOrderDetailWithAccKey(String accountID, int nRequestId, String accountKey,
			JOrderDetail data, boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqComFundWithAccKey(String accountID, int nRequestId, String accountKey, JStockComFund data,
			boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqComPositionWithAccKey(String accountID, int nRequestId, String accountKey, JStockComPosition data,
			boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqHistoryOrderDetailWithAccKey(String accountID, int nRequestId, String accountKey,
			JOrderDetail data, boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqHistoryDealDetailWithAccKey(String accountID, int nRequestId, String accountKey, JDealDetail data,
			boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqHistoryPositionStaticsWithAccKey(String accountID, int nRequestId, String accountKey,
			JPositionStatics data, boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqFtAccCommissionRateDetail(String accountID, int nRequestId, String accountKey,
			JCommissionRateDetail data, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqFtAccMarginRateDetail(String accountID, int nRequestId, String accountKey, JMarginRateDetail data,
			boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqProductIds(int nRequestId, int nProductID, String accountKey, boolean isLast) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onCreatePortfolio(int nRequestId, int nPortfolioID, String strRemark, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqProductPortfolio(int nProductID, int nRequestId, JPortfolioInfo data, boolean isLast,
			XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqPortfolioOrder(int nPortfolioID, int nRequestId, JOrderDetail data, boolean isLast,
			XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqPortfolioMultiOrder(int nPortfolioID, int nRequestId, JOrderDetail data, boolean isLast,
			XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqPortfolioDeal(int nPortfolioID, int nRequestId, JDealDetail data, boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqPortfolioMultiDeal(int nPortfolioID, int nRequestId, JDealDetail data, boolean isLast,
			XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqPortfolioPos(int nPortfolioID, int nRequestId, JPositionStatics data, boolean isLast,
			XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqStrategyInfo(String accountID, int nRequestId, String accountKey, JStrategyInfo data,
			boolean isLast, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onDirectOrder(int nRequestId, String strOrderSysID, String strRemark, XtError error) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onReqSecuAccount(String accountID, int nRequestId, String accountKey, JSecuAccount data, boolean isLast,
			XtError error) {
		// TODO Auto-generated method stub
		
	}

    @Override
    public void onReqExchangeStatus(String accountID, int nRequestId, String accountKey, ArrayList<JExchangeStatus> data, XtError error) {

    }

    public void reqFundFlow() {
        m_client.reqFundFlow("1016894", "20241201", "20241211",0, "1____21026____60066_1327____-1____1016894____");
        System.out.println("reqFundFlow ");
    }
    @Override
//    public void onReqFundFlow(String accountID, int nRequestId, String accountKey, ArrayList<JFundFlow> data, XtError error) {
    public void onReqFundFlow(String accountID, int nRequestId, String accountKey, ArrayList<JFundFlow>data, XtError error)
    {
        System.out.println("onReqFundFlow ");
    }

    @Override
    public void onReqOrderDetailBySysID(String accountID, int nRequestId, String accountKey, String orderSyeId, String exchangeId, JOrderDetail data, XtError error) {

    }

    @Override
    public void onPause(int nRequestId, String strRemark, XtError error) {

    }

    @Override
    public void onResume(int nRequestId, String strRemark, XtError error) {

    }

    @Override
    public void onReqFuturePositionStatics(String accountID, int nRequestId, String accountKey, ArrayList<JFuturePositionStatics> data, boolean isLast,XtError error) {
        for(int i = 0; i <data.size(); ++i)
        {
            JFuturePositionStatics detail = data.get(i);
            System.out.println(String.format("[onReqFuturePositionStatics] m_nPosition: %d, m_strInstrumentID: %s",
                    detail.m_nPosition, detail.m_strInstrumentID));
        }
    }
}
