using System;
using System.Threading;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using NetApi;

namespace test4csharp
{
    class Callback:XtTraderApiCallback
    {
        public int m_nRequestId;
        public String m_strAddress;
        public String m_strUserName;
        public String m_strPassWord;
        public String m_strAccountId;

        public int m_nOrderNumPerSec;
        public int m_nOrderTimeSecs;

        public XtTraderApi m_client;


        public Callback(String address, String username, String password, String accountid, int orderNum, int timeSec)
        {
            m_strAddress = address;
            m_strUserName = username;
            m_strPassWord = password;
            m_strAccountId = accountid;
            m_nOrderNumPerSec = orderNum;
            m_nOrderTimeSecs = timeSec;
        }

        public bool init()
        {
            if (m_strAddress.Length == 0)
            {
                System.Console.WriteLine("server address is empty, exit");
                return false;
            }

            m_client = XtTraderApi.createXtTraderApi(m_strAddress);
            if (null == m_client)
            {
                System.Console.WriteLine("create traderapi client fails, exit");
                return false;
            }
            m_client.setCallback(this);
            return m_client.init("../config");
        }

        public void join()
        {
            m_client.join();
        }

        public void timeExpireSendOrder()
        {
            while(m_nOrderTimeSecs>0)
            {
                Thread.Sleep(1000);
                if (m_strAccountId.StartsWith("3700"))
                {
                    testOrdinaryOrder(true, m_strAccountId, m_nOrderNumPerSec);
                    //testAlgorithmOrder(true, m_strAccountId, m_nOrderNumPerSec);
                    //testGroupOrder(m_strAccountId);  // 组合单只支持算法单
                }
                else
                    //testOrdinaryOrder(true, m_strAccountId, m_nOrderNumPerSec);
                testCAlgGroupOrder("");
                System.Console.WriteLine("Current Thread Id: {0}, time left (s): {1}", Thread.CurrentThread.ManagedThreadId, m_nOrderTimeSecs);
                m_nOrderTimeSecs--;
            }
        }

        public override void onRtnOrder(COrderInfo data)
        {
            // 处理逻辑：
            // 1. 如果 OrderStatus为 结束状态（>=EOrderCommandStatus.OCS_FINISHED)
            // 则 可以获取 成交量和成交额
            String orderStatus = "";
            switch (data.m_eStatus)
            {
                case EOrderCommandStatus.OCS_CHECKING: orderStatus = "风控检查中"; break;
                case EOrderCommandStatus.OCS_APPROVING: orderStatus = "审批中"; break;
                case EOrderCommandStatus.OCS_REJECTED: orderStatus = "已驳回"; break;
                case EOrderCommandStatus.OCS_RUNNING: orderStatus = "运行中"; break;
                case EOrderCommandStatus.OCS_CANCELING: orderStatus = "撤销中"; break;
                case EOrderCommandStatus.OCS_FINISHED: orderStatus = "已完成"; break;
                case EOrderCommandStatus.OCS_STOPPED: orderStatus = "已停止"; break;
                case EOrderCommandStatus.OCS_FROCE_COMPLETED: orderStatus = "强制撤销"; break;
                case EOrderCommandStatus.OCS_CHECKFAILED: orderStatus = "风控驳回"; break;
            }

            //string utf8String = "鍢夊拰缇庡悍";

            // Create two different encodings.
            Encoding utf8 = Encoding.UTF8;
            Encoding defaultCode = Encoding.Default;

            // Convert the string into a byte[].
            byte[] utf8Bytes = defaultCode.GetBytes(data.m_strMsg);

            // Perform the conversion from one encoding to the other.
            byte[] defaultBytes = Encoding.Convert(utf8, defaultCode, utf8Bytes);

            // Convert the new byte[] into a char[] and then into a string.
            // This is a slightly different approach to converting to illustrate
            // the use of GetCharCount/GetChars.
            char[] defaultChars = new char[defaultCode.GetCharCount(defaultBytes, 0, defaultBytes.Length)];
            defaultCode.GetChars(defaultBytes, 0, defaultBytes.Length, defaultChars, 0);
            string defaultString = new string(defaultChars);

            // Display the strings created before and after the conversion.
            Console.WriteLine("Original string: {0}", data.m_strMsg);
            Console.WriteLine("Ascii converted string: {0}", defaultString);
            data.m_strMsg = defaultString;

            System.Console.WriteLine("[onRtnOrder] order id: {0}, status: {1}, 成交量: {2}, 执行信息: {3}", data.m_nOrderID, orderStatus, data.m_dTradedVolume, data.m_strMsg);
        }


        void testOrdinaryOrder(bool isStock, String accountId, int times)
        {
            if (isStock)
            {
                for (int i = 0; i < times; ++i)
                {
                    // 股票
                    COrdinaryOrder orderInfo = new COrdinaryOrder();
                    // 资金账号，必填参数。不填会被api打回，并且通过onOrder反馈失败
                    orderInfo.m_strAccountID = accountId;

                    // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
                    orderInfo.m_dPrice = 12.2;

                    // 单笔超价百分比，选填字段。默认为0
                    orderInfo.m_dSuperPriceRate = 0.5;

                    // 报单委托量，必填字段。默认int最大值，填0或不填会被api打回
                    orderInfo.m_nVolume = 1;

                    // 报单市场。必填字段。股票市场有"SH"/"SZ"，如果填空或填错都会被api直接打回
                    orderInfo.m_strMarket = "SH";

                    // 直接还款的金额。仅直接还款用，信用业务类型专用
                    orderInfo.m_dOccurBalance = 1000;

                    // 报单合约代码，必填字段。
                    orderInfo.m_strInstrument = "601018";

                    // 报单价格类型，必填字段。默认为无效(PTRP_INVALID)。
                    orderInfo.m_ePriceType = EPriceType.PRTP_FIX;

                    // 报单委托类型。必填字段。根据相应的业务选择，默认为无效值(OPT_INVALID)。不填会被api打回
                    orderInfo.m_eOperationType = EOperationType.OPT_BUY;

                    // 投机套保标志，选填字段。有"投机"/"套利"/"套保"方式。除期货三个方式都可选之外都是填“投机”。默认为“投机”
                    orderInfo.m_eHedgeFlag = EHedgeFlagType.HEDGE_FLAG_SPECULATION;

                    orderInfo.m_strRemark = "testOrder";

                    m_client.order(orderInfo, m_nRequestId++);
                }
            }
            else
            {
                for (int i = 0; i < times; ++i)
                {
                    COrdinaryOrder orderInfo = new COrdinaryOrder();
                    // 资金账号，必填参数。不填会被api打回，并且通过onOrder反馈失败
                    orderInfo.m_strAccountID = accountId;

                    // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
                    orderInfo.m_dPrice = 16.10;

                    // 单笔超价百分比，选填字段。默认为0
                    orderInfo.m_dSuperPriceRate = 0.5;

                    // 报单委托量，必填字段。默认int最大值，填0或不填会被api打回
                    orderInfo.m_nVolume = 1;

                    // 报单市场。必填字段。如果填空或填错都会被api直接打回
                    orderInfo.m_strMarket = "CZCE";

                    // 报单合约代码，必填字段。
                    orderInfo.m_strInstrument = "CF509";

                    // 报单价格类型，必填字段。默认为无效(PTRP_INVALID)。
                    orderInfo.m_ePriceType = EPriceType.PRTP_BUY1;

                    // 报单委托类型。必填字段。根据相应的业务选择，默认为无效值(OPT_INVALID)。不填会被api打回
                    orderInfo.m_eOperationType = EOperationType.OPT_DIRECT_CASH_REPAY;

                    // 投机套保标志，选填字段。有"投机"/"套利"/"套保"方式。除期货三个方式都可选之外都是填“投机”。默认为“投机”
                    orderInfo.m_eHedgeFlag = EHedgeFlagType.HEDGE_FLAG_SPECULATION;

                    m_client.order(orderInfo, m_nRequestId++);
                }
            }
        }

        void testAlgorithmOrder(bool isStock, String accoundId, int times)
        {
            //算法单
            if (isStock)
            {
                for (int i = 0; i < times; ++i)
                {
                    CAlgorithmOrder orderInfo = new CAlgorithmOrder();
                    orderInfo.m_strAccountID = accoundId;  // 股票 账号
                    orderInfo.m_strInstrument = "000002";  // 股票代码
                    orderInfo.m_strMarket = "SZ";  // 市场：股票有 SZ, SH

                    //orderInfo.m_dPrice = 13.10;
                    //// 单笔超价
                    orderInfo.m_dSuperPriceRate = 0.1;  

                    orderInfo.m_nVolume = 100;   // 委托量

                    // 单笔下单比率，委托总量*单笔下单比率 = 单笔下单量
                    // m_nVolume * m_dSingleVolumeRate = 单笔下单量
                    // 比如，下单总量1000 * 0.005 = 5 < 最小委托量100(限于股票)， 
                    // 1000拆分成10笔委托
                    orderInfo.m_dSingleVolumeRate = 0.005;

                    orderInfo.m_dPlaceOrderInterval = 30;  // 下单间隔， 1秒(最小0.5s)
                    orderInfo.m_dWithdrawOrderInterval = 15;  // 撤单间隔：15秒（最小0.5s)

                    // 单笔下单比率最小/大值 如果不填写，会按照每笔 100只来下委托
                    //orderInfo.m_nSingleNumMin = 100;
                    //// 单笔委托最大量
                    //// 如果 m_nVolume*m_dSingleVolumeRate > m_nMaxOrderCount，则以m_nMaxOrderCount为准
                    //orderInfo.m_nSingleNumMax = 1000; 

                    //orderInfo.m_nMaxOrderCount = 100;  // 最大下单次数， 与下单间隔对应

                    // 有效开始时间和有效结束时间不用填

                    orderInfo.m_eOperationType = EOperationType.OPT_BUY;  // 股票 只有OPT_BUY、OPT_SELL

                    // 单笔基准：目标量、买1、买1+2、买1+2+3等
                    orderInfo.m_eSingleVolumeType = EVolumeType.VOLUME_FIX;

                    // 最新价、对手加、指定价、买1-5等
                    orderInfo.m_ePriceType = EPriceType.PRTP_LATEST;

                    // 套利标志, 支持 投机、套利、套保（不填则默认为“投机”）
                    orderInfo.m_eHedgeFlag = EHedgeFlagType.HEDGE_FLAG_SPECULATION;
                    //requestID，本地用于确定服务器返回的 OrderID
                    m_client.order(orderInfo, m_nRequestId++);
                }

            }
            else
            {
                for (int i = 0; i < times; ++i)
                {
                    CAlgorithmOrder orderInfo = new CAlgorithmOrder();
                    //strcpy(orderInfo.m_strAccountID, accoundId.c_str());  // 期货 账号
                    //orderInfo.m_strAccountID[accoundId.length()] = '\0';
                    orderInfo.m_strAccountID = accoundId;

                    orderInfo.m_strMarket = "CZCE";  // 市场：SZ, SH, CZCE等
                    orderInfo.m_strInstrument = "CF509";  // 期货代码

                    //orderInfo.m_dPrice = 68900.4; // 基准价（指定价报单时需要填）

                    //单笔超价百分比
                    orderInfo.m_dSuperPriceRate = 0.005;

                    orderInfo.m_nVolume = 1;   // 委托量

                    // 单笔下单比率，委托总量*单笔下单比率 = 单笔下单量
                    // m_nVolume * m_dSingleVolumeRate = 单笔下单量
                    orderInfo.m_dSingleVolumeRate = 0.005;

                    orderInfo.m_dPlaceOrderInterval = 1;  // 下单间隔， 1秒(最小0.5s)
                    orderInfo.m_dWithdrawOrderInterval = 15;  // 撤单间隔：15秒（最小0.5s)

                    // 单笔下单比率最小/大值 如果不填写，会按照每笔 100只来下委托
                    orderInfo.m_nSingleNumMin = 1;
                    // 单笔委托最大量
                    // 如果 m_nVolume*m_dSingleVolumeRate > m_nMaxOrderCount，则以m_nMaxOrderCount为准
                    orderInfo.m_nSingleNumMax = 100;

                    orderInfo.m_nMaxOrderCount = 1;  // 最大下单次数， 与下单间隔对应

                    // 有效开始时间和有效结束时间不用填

                    orderInfo.m_eOperationType = EOperationType.OPT_OPEN_LONG;  // 期货 有开多、平左多等10个选项

                    // 单笔基准：目标量、买1、买1+2、买1+2+3等
                    orderInfo.m_eSingleVolumeType = EVolumeType.VOLUME_FIX;

                    // 最新价、对手加、指定价、买1-5等
                    orderInfo.m_ePriceType = EPriceType.PRTP_LATEST;

                    // 套利标志, 支持 投机、套利、套保（不填则默认为“投机”）
                    orderInfo.m_eHedgeFlag = EHedgeFlagType.HEDGE_FLAG_SPECULATION;
                    //requestID，本地用于确定服务器返回的 OrderID
                    m_client.order(orderInfo, m_nRequestId++);
                }

            }
        }

        void testGroupOrder(String accoundId)
        {
            // 组合下单， 只支持股票
            CGroupOrder orderInfo = new CGroupOrder();
            // 单笔超价 百分比
            orderInfo.m_orderParam.m_dSuperPriceRate = 0.02;
            // 报价类型
            orderInfo.m_orderParam.m_ePriceType = EPriceType.PRTP_LATEST;
            // 下单类型
            orderInfo.m_orderParam.m_eOperationType = EOperationType.OPT_BUY;
            // 超价起始笔数, 从这一笔开始使用超价设置
            orderInfo.m_orderParam.m_nSuperPriceStart = 1;
            // 下单间隔(秒）
            orderInfo.m_orderParam.m_dPlaceOrderInterval = 30;
            // 撤单间隔（秒）
            orderInfo.m_orderParam.m_dWithdrawOrderInterval = 30;
            // 单比下单比率(1 为一次全部下单）
            orderInfo.m_orderParam.m_dSingleVolumeRate = 1;
            // 单笔下单基准
            orderInfo.m_orderParam.m_eSingleVolumeType = EVolumeType.VOLUME_FIX;
            // 最大下单次数
            orderInfo.m_orderParam.m_nMaxOrderCount = 100;
            // 单笔下单量最大值，必须大于或等于 m_nVolume[i] * m_dSingleVolumeRate
            // 否则，以单笔下单量最大值为准
            orderInfo.m_orderParam.m_nSingleNumMax = 200;
            // 单笔下单量最小值, 不能比100 再小了
            orderInfo.m_orderParam.m_nLastVolumeMin = 100;
            orderInfo.m_orderParam.m_strAccountID = accoundId;
            // 股票只数，必填参数，默认值为0。必须大于0，小于等于500
            orderInfo.m_nOrderNum = 2;
            // 合约代码， 必填字段。不填会被api打回
            orderInfo.m_strInstrument[0] = "000002";
            orderInfo.m_strInstrument[1] = "000004";
            // 市场，只有"SH"/"SZ"两个市场可以填写
            orderInfo.m_strMarket[0] = "SZ";
            orderInfo.m_strMarket[1] = "SZ";
            // 报单数量
            orderInfo.m_nVolume[0] = 100;
            orderInfo.m_nVolume[1] = 200;
            m_client.order(orderInfo, m_nRequestId++);
        }


        void testCAlgGroupOrder(String accoundId)
        {
            // 组合下单， 只支持股票
            CAlgGroupOrder orderInfo = new CAlgGroupOrder();
            // 单笔超价 百分比
            orderInfo.m_orderParam.m_strAccountID = "2000463";
            orderInfo.m_orderParam.m_strMarket = "";
            orderInfo.m_orderParam.m_strInstrument = "";
            orderInfo.m_orderParam.m_strOrderType = "TWAP";
            orderInfo.m_orderParam.m_dPrice = 0.0;
            orderInfo.m_orderParam.m_nVolume = 0;
            orderInfo.m_orderParam.m_nValidTimeStart = 1729562717;
            orderInfo.m_orderParam.m_nValidTimeEnd = 1729564537;
            orderInfo.m_orderParam.m_dMaxPartRate = 0.2;
            orderInfo.m_orderParam.m_dMinAmountPerOrder = 0;
            orderInfo.m_orderParam.m_ePriceType = EPriceType.PRTP_MARKET;
            orderInfo.m_orderParam.m_eOperationType = EOperationType.OPT_BUY;

            orderInfo.m_orderParam.m_dPriceOffsetBpsForAuction = 200;
            orderInfo.m_orderParam.m_dOrderRateInOpenAcution = 0.2;
            orderInfo.m_orderParam.m_bOnlySellAmountUsed = true;
            orderInfo.m_orderParam.m_dBuySellAmountDeltaPct = 0.03;
            orderInfo.m_orderParam.m_nMaxTradeDurationAfterET = 0;
            orderInfo.m_orderParam.m_eOrderStrategyType = EOrderStrategyType.E_ORDER_STRATEGY_TYPE_NORMAL;

            // 市场，只有"SH"/"SZ"两个市场可以填写
            orderInfo.m_strMarket[0] = "SZ";
            orderInfo.m_strMarket[1] = "SZ";

            // 合约代码， 必填字段。不填会被api打回
            orderInfo.m_strInstrument[0] = "000002";
            orderInfo.m_strInstrument[1] = "000004";

            // 报单数量
            orderInfo.m_nVolume[0] = 100;
            orderInfo.m_nVolume[1] = 200;

            orderInfo.m_eOperationType[0] = EOperationType.OPT_BUY;
            orderInfo.m_eOperationType[1] = EOperationType.OPT_BUY;

            // 股票只数，必填参数，默认值为0。必须大于0，小于等于500
            orderInfo.m_nOrderNum = 2;

            m_client.order(orderInfo, m_nRequestId++, "");
        }
        public override void onConnected(bool success, String errorMsg)
        {
            System.Console.WriteLine("connect {0}", success);
            if (success)
            {
                m_client.userLogin(m_strUserName, m_strPassWord, m_nRequestId++, "","","");
            }else {
                System.Console.WriteLine("connect failed! errorMsg: {0}", errorMsg);
            }
        }

        public override void onUserLogin(String userName, String password, int nRequestId, XtError error)
        {
            if (error.isSuccess())
            {
                //testOrdinaryOrder(true, m_strAccountId, m_nOrderNumPerSec);
                //m_client.reqAccountDetail(m_strAccountId, m_nRequestId++);
                //m_client.reqOrderDetail(m_strAccountId, m_nRequestId++);
                //m_client.reqOrderDetail(m_strAccountId, m_nRequestId++, 312);
                //m_client.reqDealDetail(m_strAccountId, m_nRequestId++);
                //m_client.reqPositionDetail(m_strAccountId, m_nRequestId++);
                //m_client.reqPriceData("SZ", "000002", m_nRequestId++);
                System.Console.WriteLine("UserLogin Success username: {0}, password: {1}", userName, password);
            }
            else
            {
                System.Console.WriteLine("UserLogin fails, username: {0}, password: {1}, errorMsg: {2}", userName, password, error.errorMsg());
            }
        }
        
        public override void onUserLogout(String userName, String password, int nRequestId, XtError error)
        {
            if (error.isSuccess())
            {
                System.Console.WriteLine("[onUserLogout] success");
            }
            else
            {
                System.Console.WriteLine("[onUserLogout] fails, errorId:{0},errorMsg:{1}", error.errorID(), error.errorMsg());
            }
            
        }

        public override void onReqPositionDetail(String accountID, int nRequestId, CPositionDetail data, bool isLast, XtError error)
        {
            if (error.isSuccess() )
            {
                System.Console.WriteLine("[onReqPositionDetail] accountid: {0}, m_strExchangeID: {1}, error id: {2}, error msg: {3}", data.m_strAccountID, data.m_strExchangeID, error.errorID(), error.errorMsg());
            } 
            else
            {
                System.Console.WriteLine("[onReqPositionDetail] data is null. accountid: {0}, error id: {1}, error msg: {2}", accountID, error.errorID(), error.errorMsg());
            }
        }

        public override void onReqPositionStatics(String accountID, int nRequestId, CPositionStatics data, bool isLast, XtError error)
        {
            if (error.isSuccess())
            {
                System.Console.WriteLine("[onReqPositionStatics] accountid: {0}, m_strExchangeID: {1}, error id: {2}, error msg: {3}", data.m_strAccountID, data.m_strExchangeID, error.errorID(), error.errorMsg());
            }
            else
            {
                System.Console.WriteLine("[onReqPositionStatics] data is null. accountid: {0}, error id: {1}, error msg: {2}", accountID, error.errorID(), error.errorMsg());
            }
        }

        public override void onReqAccountDetail(String accountID, int nRequestId, CAccountDetail data, bool isLast, XtError error)
        {
            if (error.isSuccess() )
            {
                System.Console.WriteLine("[onReqAccountDetail] accountid: {0}, m_dBalance: {1}, error id: {2}, error msg: {3}", data.m_strAccountID, data.m_dBalance, error.errorID(), error.errorMsg());
            } 
            else
            {
                System.Console.WriteLine("[onReqAccountDetail] data is null. accountid: {0}, error id: {1}, error msg: {2}", accountID, error.errorID(), error.errorMsg());
            }
        }

        public override void onReqOrderDetail(String accountID, int nRequestId, COrderDetail data, bool isLast, XtError error)
        {
            if (error.isSuccess())
            {
                System.Console.WriteLine("[onReqOrderDetail] accountid: {0}, ExchangeId: {1}, error id: {2}, error msg: {3}", data.m_strAccountID, data.m_strExchangeID, error.errorID(), error.errorMsg());
            }
            else
            {
                System.Console.WriteLine("[onReqOrderDetail] data is null. accountid: {0}, error id: {1}, error msg: {2}", accountID, error.errorID(), error.errorMsg());
            }
        }     
   
        public override void onReqDealDetail(String accountID, int nRequestId, CDealDetail data, bool isLast, XtError error)
        {
            if (error.isSuccess())
            {
                System.Console.WriteLine("[onReqDealDetail] accountid: {0}, OrderSysID: {1}, error id: {2}, error msg: {3}", accountID, data.m_strOrderSysID, error.errorID(), error.errorMsg());
            }
            else
            {
                System.Console.WriteLine("[onReqDealDetail] data is null. accountid: {0}, error id: {1}, error msg: {2}", accountID, error.errorID(), error.errorMsg());
            }
        }
        public override void onReqCreditAccountDetail(String accountID, int nRequestId, CCreditAccountDetail data, bool isLast, XtError error)
        {
            if (error.isSuccess())
            {
                System.Console.WriteLine("[onReqCreditAccountDetail] accountid: {0}, SloIncome: {1}, error id: {2}, error msg: {3}", accountID, data.m_dSloIncome, error.errorID(), error.errorMsg());
            }
            else
            {
                System.Console.WriteLine("[onReqCreditAccountDetail] data is null. accountid: {0}, error id: {1}, error msg: {2}", accountID, error.errorID(), error.errorMsg());
            }
        }
        public override void onRtnCreditAccountDetail(String accountID, CCreditAccountDetail data)
        {
            System.Console.WriteLine("[onRtnCreditAccountDetail] m_dPerAssurescaleValue:{0}", data.m_dPerAssurescaleValue);
        }

        public override void onReqStkcompacts(string accountID, int nRequestId, CStkCompacts data, bool isLast, XtError error) {
            System.Console.WriteLine("[onReqStkcompacts] m_dBusinessFare:{0}", data.m_dBusinessFare);
        }

        public override void onReqStksubjects(string accountID, int nRequestId, CStkSubjects data, bool isLast, XtError error)
        {
            System.Console.WriteLine("[onReqStksubjects] m_dAssureRatio:{0}", data.m_dAssureRatio);
        }

        public override void onReqCoveredStockPosition(string accountID, int nRequestId, CCoveredStockPosition data, bool isLast, XtError error)
        {
            System.Console.WriteLine("[onReqCoveredStockPosition] m_nTotalAmount:{0}", data.m_nTotalAmount);
        }

        public override void onReqStkOptCombPositionDetail(string accountID, int nRequestId, CStockOptionCombPositionDetail data, bool isLast, XtError error)
        {
            System.Console.WriteLine("[onReqStkOptCombPositionDetail] m_strCombID:{0}", data.m_strCombID);
        }

        public override void onReqPriceData(int nRequestId, CPriceData data, XtError error)
        {
            if (error.isSuccess())
            {
                System.Console.WriteLine("[onReqPriceData] nRequestId: {0}, m_dLastPrice: {1}, m_dAveragePrice: {2}, error id: {3}, error msg: {4}", nRequestId, data.m_dLastPrice, data.m_dAveragePrice, error.errorID(), error.errorMsg());
            }
            else
            {
                System.Console.WriteLine("[onReqPriceData] data is null. nRequestId: {0}, error id: {1}, error msg: {2}", nRequestId, error.errorID(), error.errorMsg());
            }
        }

        public override void onReqCInstrumentDetail(string accountID, int nRequestId, CInstrumentDetail data, bool isLast, XtError error)
        {
            if (error.isSuccess())
            {
                System.Console.WriteLine("[onReqCInstrumentDetail] nRequestId: {0}, m_strInstrumentID: {1}, m_dOptExercisePrice: {2}, m_strInstrumentName: {3}", nRequestId, data.m_strInstrumentID, data.m_dOptExercisePrice, data.m_strInstrumentName);
            }
            else
            {
                System.Console.WriteLine("[onReqCInstrumentDetail] data is null. nRequestId: {0}, error id: {1}, error msg: {2}", nRequestId, error.errorID(), error.errorMsg());
            }
        }
       
        public override void onRtnOrderDetail(COrderDetail data)
        {
            if (data.m_nErrorID == 0 )
            {
                System.Console.WriteLine("[onRtnOrderDetail] OrderId: {0}, 委托状态:{1}, instrumentId:{2}", data.m_nOrderID, data.m_eOrderStatus, data.m_strInstrumentID);
            }
            else
            {
                System.Console.WriteLine("[onRtnOrderDetai] Failure. {0} ErrorID: {1}, ErrorMsg:{2}", data.m_nOrderID, data.m_nErrorID, data.m_strErrorMsg);
            }
        }

        public override void onRtnDealDetail(CDealDetail data)
        {
            System.Console.WriteLine("[onRtnDealDetail] orderId: {0}, orderSysId:{1}, m_nVolume:{2}, m_dAmount:{3}", data.m_nOrderID, data.m_strOrderSysID, data.m_nVolume, data.m_dAmount);
        }

        public override void onRtnOrderError(COrderError data)
        {
            System.Console.WriteLine("[onRtnOrderError] orderId:{0}", data.m_nOrderID);
        }

        public override void onRtnCancelError(CCancelError data)
        {
            System.Console.WriteLine("[onRtnCancelError] orderId:{0} ", data.m_nOrderID);
        }

        public override void onRtnLoginStatus(String accountID, EBrokerLoginStatus status, int brokerType, String errorMsg)
        {

            String loginStatus = "";
            switch (status)
            {
                case EBrokerLoginStatus.BROKER_LOGIN_STATUS_INALID: loginStatus = "无效状态"; break;
                case EBrokerLoginStatus.BROKER_LOGIN_STATUS_OK: loginStatus = "可用，初始化完成"; break;
                case EBrokerLoginStatus.BROKER_LOGIN_STATUS_WAITING_LOGIN: loginStatus = "连接中"; break;
                case EBrokerLoginStatus.BROKER_LOGIN_STATUS_LOGINING: loginStatus = "登录中"; break;
                case EBrokerLoginStatus.BROKER_LOGIN_STATUS_FAIL: loginStatus = "失败"; break;
                case EBrokerLoginStatus.BROKER_LOGIN_STATUS_INITING: loginStatus = "在初始化中 "; break;
                case EBrokerLoginStatus.BROKER_LOGIN_STATUS_CORRECTING: loginStatus = "数据刷新校正中"; break;
                case EBrokerLoginStatus.BROKER_LOGIN_STATUS_CLOSED: loginStatus = "收盘后（休市中）"; break;
            }

            System.Console.WriteLine("[onRtnLoginStatus] {0} status: {1} ", accountID, loginStatus);
            if (status == EBrokerLoginStatus.BROKER_LOGIN_STATUS_OK && m_strAccountId == accountID)
            {
                System.Console.WriteLine("Main thread id is: {0}, start order thread", Thread.CurrentThread.ManagedThreadId);
                m_client.reqInstrumentDetail(accountID, ++m_nRequestId);
                Thread orderThread = new Thread(new ThreadStart(timeExpireSendOrder));
                orderThread.Start();
            }
            if (status == EBrokerLoginStatus.BROKER_LOGIN_STATUS_OK)
            {
                //System.Console.WriteLine("Main thread id is: {0}, start order thread", Thread.CurrentThread.ManagedThreadId);
            }
        }

        public override void onRtnLoginStatusWithActKey(String accountID, EBrokerLoginStatus status, int brokerType, String accountKey, String errorMsg)
        {
            if (status == EBrokerLoginStatus.BROKER_LOGIN_STATUS_OK && m_strAccountId == accountID)
            {
                //testOrdinaryOrder(true, m_strAccountId, 1);
            }
        }

        public override void onRtnAccountDetail(String accountID, CAccountDetail accountDetail)
        {
            //System.Console.WriteLine("onRtnAccountDetail 账号ID:" + accountID + " with detail " + accountDetail.ToString());
        }

        public override void onRtnNetValue(CNetValue data)
        {
            //System.Console.WriteLine("onRtnNetValue, productid: " + data.m_nProductId);
        }

        public override void onRtnDeliveryStatus(String accountID, bool status, String errorMsg)
        {
            //System.Console.WriteLine("onRtnDeliveryStatus ID:" + accountID + (status? "OK" : " with Msg " + errorMsg));
        }

        public override void onOrder(int nRequestId, int orderID, String strRemark, XtError error)
        {
            if (error.isSuccess())
            {
                //m_client.cancel(orderID, nRequestId++);
                System.Console.WriteLine("[onOrder] success, orderId: {0}, requestId: {1}", orderID, nRequestId);
            }
            else
            {
                System.Console.WriteLine("[onOrder] failure, orderId: {0}, requestId: {1}, error id: {2}, error msg: {3}", orderID, nRequestId, error.errorID(), error.errorMsg());
            }
        }

        public override void onCancel(int nRequestId, XtError error)
        {
            System.Console.WriteLine("onCancel " + (error.isSuccess() ? " success" : (" ERR ID" + error.errorID() + " msg: " + error.errorMsg())));
        }

        public override void onCancelOrder(int nRequestId, XtError error)
        {
            System.Console.WriteLine("onCancel " + (error.isSuccess() ? " success" : (" ERR ID" + error.errorID() + " msg: " + error.errorMsg())));
        }

        public override void onReqReferenceRate(String accountID, int nRequestId, CReferenceRate data, bool isLast, XtError error)
        {
        }

        public override void onRtnPriceData(CPriceData data)
        {
        }

        public override void onCancelWithRemark(int nRequestId, String strRemark, XtError error)
        {
        }

        public override void onReqCreditDetail(String accountID, int nRequestId, CCreditDetail data, bool isLast, XtError error)
        {
        }

        public override void onOperateTask(String accountID, int nRequestId, String accountKey, XtError error)
        {
        }

        public override void onModifyAlgoCommands(int nRequestId, int orderID, String strRemark, XtError error)
        {
        }

        public override void onReqSubscribeInfo(String accountID, int nRequestId, CSubscribeInfo data, bool isLast, XtError error)
        {
        }

        public override void onReqStkUnCloseCompact(String accountID, int nRequestId, CStkUnClosedCompacts data, bool isLast, XtError error)
        {
        }

        public override void onReqStkClosedCompact(String accountID, int nRequestId, CStkClosedCompacts data, bool isLast, XtError error)
        {
        }

        public override void onCustomTimer()
        {
            System.Console.WriteLine("onCustomTimer");
        }
    }
}
