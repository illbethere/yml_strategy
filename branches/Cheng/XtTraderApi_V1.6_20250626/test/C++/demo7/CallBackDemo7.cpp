#include "time.h"
#include <string.h>
#include <demo7/CallBackDemo7.h>
#include <windows.h>
const int INDEX = 10;

namespace demo7
{
    Callback::Callback(const string& address, const string& username, const string& password):
        m_nRequestId(1),
        m_strAddress(address),
        m_strUserName(username),
        m_strPassWord(password),
        m_client(NULL),
        m_blogin(false),
        m_bloginStatus(false),
        m_bDoRequest(true),
        m_nRespCnt(0)
    {
    }

    Callback::~Callback()
    {
        if (m_client != NULL)
        {
            m_client->destroy();
            delete m_client;
        }
    }

    int Callback::init()
    {
        cout << endl;
        cout << "[init] server: " << m_strAddress << ", username: " << m_strUserName << endl;
        m_client = XtTraderApi::createXtTraderApi(m_strAddress.c_str());
        if (NULL == m_client)
        {
            cout << "[init] create api failure" << endl;
            return -1;
        }

        m_client->setCallback(this);
        return m_client->init("../config");
    }

    //获取资金账号对应key值，为了区分相同资金账号
    string Callback::getAccountKey(const char* accountId, EXTBrokerType brokerType)
    {
        CAccountKey arrAccountKey[INDEX];
        XtError xtError = m_client->getKey(accountId, arrAccountKey, INDEX);
        if (xtError.isSuccess())
        {
            for (int i = 0; i < INDEX; ++i)
            {
                if (arrAccountKey[i].m_eBrokerType == brokerType)
                    return arrAccountKey[i].m_strAccountKey;
            }
        }
        return "";
    }

    long long Callback::genRequestId()
    {
        return ++m_nRequestId;
    }

    string Callback::getAccountTypeDesc(int brokerType)
    {
        switch (brokerType)
        {
        case AT_FUTURE:
            return "期货账号";
        case AT_STOCK:
            return "股票账号";
        case AT_CREDIT:
            return "信用账号";
        case AT_GOLD:
            return "贵金属账号";
        case AT_FUTURE_OPTION:
            return "期货期权账号";
        case AT_STOCK_OPTION:
            return "个股期权账号";
        case AT_HUGANGTONG:
            return "沪港通账号";
        case AT_SHENGANGTONG:
            return "深港通账号";
        case AT_NEW3BOARD:
            return "新三板账号";
        default:
            break;
        }
        return "未知账号";
    }

    std::string Callback::getAccountStatusDesc(int status)
    {
        switch (status)
        {
        case BROKER_LOGIN_STATUS_INALID:    return "登录无效";
        case BROKER_LOGIN_STATUS_OK:        return "可用，初始化完成";
        case BROKER_LOGIN_STATUS_WAITING_LOGIN:  return "连接中";
        case BROKER_LOGIN_STATUS_LOGINING:  return "登录中";
        case BROKER_LOGIN_STATUS_FAIL:      return "失败";
        case BROKER_LOGIN_STATUS_INITING:   return "在初始化中";
        case BROKER_LOGIN_STATUS_CORRECTING:return "数据刷新校正中";
        case BROKER_LOGIN_STATUS_CLOSED:    return "收盘后（休市中）";
        default: return "未知";
        }
    }

    void Callback::join()
    {
        m_client->join();
    }

    void Callback::joinAll()
    {
        m_client->XtTraderApi::joinAll();
    }

    void Callback::doRequest()
    {
        //testReqProductData();
        testReqProductDataSync();

        //testReqAccountDetailSyncWithProductId();
        //testReqDealDetailSyncWithProductId();
        //testReqDealStaticsSyncWithProductId();
        //testReqHistoryDealDetailSyncWithProductID();
        //testReqHistoryDealStaticsSyncWithProductID();
        //testReqHistoryPositionStaticsSyncWithProductID();

        //cout << "start send request" << endl;
        // 这里可进行账号、资金、持仓等基础信息查询
        //CAccountDetailSync accdata = m_client->reqAccountDetailSync(userName, m_strAccountKey.c_str());
        //查询账号资金信息
        //m_client->reqAccountDetail(m_strStockAccount.c_str(), genRequestId());
        //testReqAccountKeySync();
        //m_client->reqOrderDetail(m_strStockAccount.c_str(), genRequestId());
        //m_client->reqOrderDetailNew(m_strStockAccount.c_str(), genRequestId(), m_strAccountKey.c_str());
        //m_client->reqDealDetail(m_strStockAccount.c_str(), genRequestId());
        //m_client->reqPositionDetail(m_strStockAccount.c_str(), genRequestId());
        //查询账号持仓统计
        //m_client->reqPositionStatics(m_strStockAccount.c_str(), genRequestId(), m_strAccountKey.c_str());

        // 报单类参数
       // m_client->cancel(472, genRequestId());
        //testCancelSync(int(472),  m_strAccountKey.c_str());
        //testStockOrdinaryOrder(m_strStockAccount.c_str(), 1);// 普通单，股票
        //testOrdinaryOrder(CB_AT_STOCK, m_strStockAccount.c_str(), 1);  // 普通单，股票
        // testAlgorithmOrder(AT_STOCK, m_strStockAccount.c_str()); // 算法单，股票
        //testIntelligentAlgorithmOrder(m_strStockAccount.c_str(), m_strAccountKey.c_str()); //智能算法单
        //testAlgoGroupOrder(m_strStockAccount.c_str(), m_strAccountKey.c_str()); //智能算法单
        //testStockOrdinaryGroupOrder(m_strStockAccount.c_str(), m_strAccountKey.c_str());

        // 订阅行情
        //CSubscribData subInfo1;
        //strcpy(subInfo1.m_strExchangeID, "SH");
        //strcpy(subInfo1.m_strInstrumentID, "600000");
        //subInfo1.m_eOfferStatus = XT_OFFER_STATUS_SP;
        //cout << "[REQ] [subscribQuote]" << endl;
        //m_client->subscribQuote(&subInfo1, genRequestId());
        //Sleep(1);
        //cout << "[REQ] [subscribQuote]" << endl;
        //m_client->subscribQuote(&subInfo1, genRequestId());

        //CSubscribData subInfo2;
        //strcpy(subInfo2.m_strExchangeID, "SZ");
        //strcpy(subInfo2.m_strInstrumentID, "000001");
        //subInfo2.m_eOfferStatus = XT_OFFER_STATUS_SP;
        //m_client->subscribQuote(&subInfo2, genRequestId());
        //vector<CSubscribData> v_subData;
        //v_subData.push_back(subInfo1);
        //v_subData.push_back(subInfo2);
        //m_client->batchSubscribQuote(&v_subData, genRequestId());
        //m_client->batchUnSubscribQuote(&v_subData, genRequestId());

        //testReqProductData();


    }

    void Callback::onConnected(bool success, const char* errorMsg)
    {
        cout << "[onConnected] server connect " << (success ? string("success") : string("failure, err: ") + errorMsg) << endl;
        if (success)
        {
            m_client->userLogin(m_strUserName.c_str(), m_strPassWord.c_str(), m_nRequestId++);
            //XtError logindata = m_client->userLoginSync(m_strUserName.c_str(), m_strPassWord.c_str());
            //if (logindata.isSuccess())
            //{
            //    m_bloginStatus = true;
            //    //if (m_blogin && m_bloginStatus)
            //    {
            //        //if (m_bDoRequest)
            //        {
            //            doRequest();
            //            m_bDoRequest = false;
            //        }
            //    }
            //}
        }
    }

    void Callback::onUserLogin(const char* userName, const char* password, int nRequestId, const XtError& error)
    {

        if (error.isSuccess())
        {
            m_bloginStatus = true;
        }
        cout << "[onUserLogin] login " << (error.isSuccess() ? "success" : string("failure, err: ") + error.errorMsg()) << endl;
        if ( m_blogin && m_bloginStatus)
        {
            if (m_bDoRequest)
            {
                doRequest();
                m_bDoRequest = false;
            }
        }
    }

    void Callback::onRtnLoginStatus(const char* accountId, EBrokerLoginStatus status, int brokerType, const char* errorMsg)
    {
        if (status == BROKER_LOGIN_STATUS_OK)
        {
            m_blogin = true;
        }
        cout << "[onRtnLoginStatus] account id: " << accountId << ", type: " << getAccountTypeDesc(brokerType) << ", status: " << getAccountStatusDesc(status) << endl;

        if (brokerType == AT_STOCK)
        {
            m_strStockAccount = accountId;
        }
        if (m_blogin && m_bloginStatus)
        {
            if (m_bDoRequest && brokerType == AT_STOCK)
            {
                doRequest();
                m_bDoRequest = false;
            }
        }
    }

    void Callback::onRtnLoginStatusWithActKey(const char* accountId, EBrokerLoginStatus status, int brokerType, const char* accountKey, const char* errorMsg)
    {
        m_strAccountKey = accountKey;
        cout << "[onRtnLoginStatusWithActKey] account id: " << accountId << ", account key: " << accountKey <<", type: " << getAccountTypeDesc(brokerType) << ", status: " << getAccountStatusDesc(status) << endl;
    }

    // ----------------------普通单----------------------------------------------


    void Callback::testFutureOrdinaryOrder(const string& accountId,  int times)
    {
        for (int i = 0; i < times; ++i)
        {
            // 参数中所有char[]数组默认值都为空。
             COrdinaryOrder orderInfo;

            // 资金账号，必填参数。不填会被api打回，并且通过onOrder反馈失败
            strcpy(orderInfo.m_strAccountID, accountId.c_str());

            // 单笔超价百分比，选填字段。默认为0
            orderInfo.m_dSuperPriceRate = 0;

            // 报单市场。必填字段。股票市场有"CFFEX"/"SHFE"/"DCE"/"CZCE"，如果填空或填错都会被api直接打回
            strcpy(orderInfo.m_strMarket, "CZCE");

            // 报单合约代码，必填字段。
            strcpy(orderInfo.m_strInstrument, "CF503");

            // 报单委托量，必填字段。默认int最大值，填0或不填会被api打回
            orderInfo.m_nVolume = 1;

            // 报单委托类型。必填字段。根据相应的业务选择，具体请参考XtDataType.h，默认为无效值(OPT_INVALID)。不填会被api打回
            orderInfo.m_eOperationType = OPT_OPEN_LONG;

            // 报单价格类型，必填字段。默认为无效(PTRP_INVALID)，具体可参考XtDataType.h
            orderInfo.m_ePriceType = PRTP_LATEST;

            // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
            orderInfo.m_dPrice = 12895;

            // 投机套保标志，选填字段。有"投机"/"套利"/"套保"方式。除期货三个方式都可选之外都是填“投机”。默认为“投机”
            orderInfo.m_eHedgeFlag = HEDGE_FLAG_SPECULATION;

            // 直接还款的金额。仅直接还款用，信用业务类型专用
            orderInfo.m_dOccurBalance = 100;

            orderInfo.m_eTimeCondition = TIME_CONDITION_IOC;
            orderInfo.m_eVolumeCondition = VOLUME_CONDITION_MIN;

            m_client->order(&orderInfo, genRequestId());
        }
    }

    void Callback::testFutureOrdinaryGroupOrder(const string& accountId, string accountKey)
    {
        // 参数中所有char[]数组默认值都为空。
        COrdinaryGroupOrder orderInfo;

        // 资金账号，必填参数。不填会被api打回，并且通过onOrder反馈失败
        strcpy(orderInfo.m_strAccountID, accountId.c_str());

        // 单笔超价百分比，选填字段。默认为0
        orderInfo.m_dSuperPriceRate = 0;

        orderInfo.m_nOrderNum = 3;

        // 合约代码， 必填字段。不填会被api打回
        strcpy(orderInfo.m_strInstrument[0], "IC2106");
        strcpy(orderInfo.m_strInstrument[1], "IF2106");
        strcpy(orderInfo.m_strInstrument[2], "a2103");

        // 市场，只有"SH"/"SZ"两个市场可以填写
        strcpy(orderInfo.m_strMarket[0], "CFFEX");
        strcpy(orderInfo.m_strMarket[1], "CFFEX");
        strcpy(orderInfo.m_strMarket[2], "DCE");

        // 报单数量
        orderInfo.m_nVolume[0] = 1;
        orderInfo.m_nVolume[1] = 2;
        orderInfo.m_nVolume[2] = 1;

        // 报单委托类型。必填字段。根据相应的业务选择，具体请参考XtDataType.h，默认为无效值(OPT_INVALID)。不填会被api打回
        orderInfo.m_eOperationType[0] = OPT_OPEN_LONG;
        orderInfo.m_eOperationType[1] = OPT_CLOSE_LONG_HISTORY;
        orderInfo.m_eOperationType[2] = OPT_OPEN_LONG;

        // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
        orderInfo.m_dPrice[0] = 12;
        orderInfo.m_dPrice[1] = 13;
        orderInfo.m_dPrice[2] = 14;

        // 报单价格类型，必填字段。默认为无效(PTRP_INVALID)，具体可参考XtDataType.h
        orderInfo.m_ePriceType = PRTP_SALE1;

        // 投机套保标志，选填字段。有"投机"/"套利"/"套保"方式。除期货三个方式都可选之外都是填“投机”。默认为“投机”
        orderInfo.m_eHedgeFlag = HEDGE_FLAG_SPECULATION;

        orderInfo.m_eTimeCondition = TIME_CONDITION_IOC;
        orderInfo.m_eVolumeCondition = VOLUME_CONDITION_MIN;

        // 投资备注
        strcpy(orderInfo.m_strRemark, "test002");

        m_client->order(&orderInfo, genRequestId());
    }


    void Callback::testFutureOrdinaryOrder(const string& accountId, const std::string& accountKey,  int times)
    {
        for (int i = 0; i < times; ++i)
        {
            // 参数中所有char[]数组默认值都为空。
            COrdinaryOrder orderInfo;

            // 资金账号，必填参数。不填会被api打回，并且通过onOrder反馈失败
            strcpy(orderInfo.m_strAccountID, accountId.c_str());

            // 单笔超价百分比，选填字段。默认为0
            orderInfo.m_dSuperPriceRate = 0;

            // 报单市场。必填字段。股票市场有"CFFEX"/"SHFE"/"DCE"/"CZCE"，如果填空或填错都会被api直接打回
            strcpy(orderInfo.m_strMarket, "CFFEX");

            // 报单合约代码，必填字段。
            strcpy(orderInfo.m_strInstrument, "IF2009");

            // 报单委托量，必填字段。默认int最大值，填0或不填会被api打回
            orderInfo.m_nVolume = 1;

            // 报单委托类型。必填字段。根据相应的业务选择，具体请参考XtDataType.h，默认为无效值(OPT_INVALID)。不填会被api打回
            orderInfo.m_eOperationType = OPT_OPEN_LONG;

            // 报单价格类型，必填字段。默认为无效(PTRP_INVALID)，具体可参考XtDataType.h
            orderInfo.m_ePriceType = PRTP_FIX;

            // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
            orderInfo.m_dPrice = 222;

            // 投机套保标志，选填字段。有"投机"/"套利"/"套保"方式。除期货三个方式都可选之外都是填“投机”。默认为“投机”
            orderInfo.m_eHedgeFlag = HEDGE_FLAG_SPECULATION;

            // 直接还款的金额。仅直接还款用，信用业务类型专用
            orderInfo.m_dOccurBalance = 100;

            orderInfo.m_eTimeCondition = TIME_CONDITION_IOC;
            orderInfo.m_eVolumeCondition = VOLUME_CONDITION_MIN;

            m_client->order(&orderInfo, genRequestId(), accountKey.c_str());
        }
    }
    
    void Callback::testFutureOptionOrdinaryOrder(const string& accountId,  int times)
    {
        for (int i = 0; i < times; ++i)
        {
            // 参数中所有char[]数组默认值都为空。
            COrdinaryOrder orderInfo;

            // 资金账号，必填参数。不填会被api打回，并且通过onOrder反馈失败
            strcpy(orderInfo.m_strAccountID, accountId.c_str());

            // 单笔超价百分比，选填字段。默认为0
            orderInfo.m_dSuperPriceRate = 0;

            // 报单市场。必填字段。股票市场有"CFFEX"/"SHFE"/"DCE"/"CZCE"，如果填空或填错都会被api直接打回
            strcpy(orderInfo.m_strMarket, "DCE");

            // 报单合约代码，必填字段。
            strcpy(orderInfo.m_strInstrument, "m1812-C-3300");

            // 报单委托量，必填字段。默认int最大值，填0或不填会被api打回
            orderInfo.m_nVolume = 1;

            // 报单委托类型。必填字段。根据相应的业务选择，具体请参考XtDataType.h，默认为无效值(OPT_INVALID)。不填会被api打回
            orderInfo.m_eOperationType = OPT_OPEN_LONG;

            // 报单价格类型，必填字段。默认为无效(PTRP_INVALID)，具体可参考XtDataType.h
            orderInfo.m_ePriceType = PRTP_FIX;

            // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
            orderInfo.m_dPrice = 158;

            // 投机套保标志，选填字段。有"投机"/"套利"/"套保"方式。除期货三个方式都可选之外都是填“投机”。默认为“投机”
            orderInfo.m_eHedgeFlag = HEDGE_FLAG_SPECULATION;

            // 直接还款的金额。仅直接还款用，信用业务类型专用
            orderInfo.m_dOccurBalance = 100;

            m_client->order(&orderInfo, genRequestId());
        }
    }


    void Callback::testReqAccountKeySync()
    {
        XtError m_error = XtError();
        vector<CAccountKey> accountData = m_client->reqAccountKeysSync(m_error);
        if (m_error.isSuccess())
        {
            cout << "accountKey size:" << accountData.size() << endl;
            for (int i = 0; i< accountData.size(); ++i)
            {
                cout << "accountKey :" << accountData[i].m_strAccountKey << endl;
            }
        }
    }


    void Callback::testReqAccountDetailSyncWithProductId()
    {
        XtError xterror = XtError();
        vector<xti::CAccountDetail> accontMap;
        accontMap = m_client->reqAccountDetailSyncWithProductId(xterror, 1265);
    }


    void Callback::testReqDealDetailSyncWithProductId()
    {
        XtError xterror = XtError();
        vector<xti::CDealDetail> dealDetailMap;
        dealDetailMap = m_client->reqDealDetailSyncWithProductId(xterror, 1265);
        if (xterror.isSuccess())
        {
            cout << "reqDealDetailSyncWithProductId success" << endl;
        }
        else
        {
            cout << "reqDealDetailSyncWithProductId failed, errmsg:" << xterror.errorMsg() << endl;
        }
    }


    void Callback::testReqDealStaticsSyncWithProductId()
    {
        XtError xterror = XtError();
        vector<xti::CDealStatics> dealStaticsMap;
        dealStaticsMap = m_client->reqDealStaticsSyncWithProductId(xterror, 1265);
        for (int i = 0; i < dealStaticsMap.size(); ++i)
        {
            cout << "DealStatics  "
                << " m_strInstrumentID: " << dealStaticsMap[i].m_strInstrumentID
                << " m_nOffsetFlag: " << dealStaticsMap[i].m_nOffsetFlag
                << " m_nCount: " << dealStaticsMap[i].m_nCount
                << " m_nVolume: " << dealStaticsMap[i].m_nVolume << endl;
        }
    }


    void Callback::testReqHistoryDealDetailSyncWithProductID()
    {
        XtError xterror = XtError();
        vector<xti::CDealDetail> dealDetailMap;
        dealDetailMap = m_client->reqHistoryDealDetailSyncWithProductId("20231013","20231013",xterror, 1265);
        if (xterror.isSuccess())
        {
            cout << "reqDealDetailSyncWithProductId success" << endl;
        }
        else
        {
            cout << "reqDealDetailSyncWithProductId failed, errmsg:" << xterror.errorMsg() << endl;
        }
    }


    void Callback::testReqHistoryDealStaticsSyncWithProductID()
    {
        for (int j = 0; j < 5; ++j)
        {
            XtError xterror = XtError();
            vector<xti::CDealStatics> dealStaticsMap;
            dealStaticsMap = m_client->reqHistoryDealStaticsSyncWithProductId("20231013", "20231013", xterror, 1265);
            for (int i = 0; i < dealStaticsMap.size(); ++i)
            {
                cout << "DealStatics  "
                    << " m_strInstrumentID: " << dealStaticsMap[i].m_strInstrumentID
                    << " m_nOffsetFlag: " << dealStaticsMap[i].m_nOffsetFlag
                    << " m_nCount: " << dealStaticsMap[i].m_nCount
                    << " m_nVolume: " << dealStaticsMap[i].m_nVolume << endl;
            }
        }
    }


    void Callback::testReqHistoryPositionStaticsSyncWithProductID()
    {
        XtError xterror = XtError();
        vector<xti::CPositionStatics>positionStaticsMap;
        positionStaticsMap = m_client->reqHistoryPositionStaticsSyncWithProductId("20231013", "20231013", xterror, 1265);
        for (int i = 0; i < positionStaticsMap.size(); ++i)
        {
            cout << "DealStatics  "
                << " m_strInstrumentID: " << positionStaticsMap[i].m_strInstrumentID
                << " m_strInstrumentName: " << positionStaticsMap[i].m_strInstrumentName
                << " m_strInstrumentName: " << positionStaticsMap[i].m_strInstrumentName
                << " m_dPositionCost: " << positionStaticsMap[i].m_dPositionCost << endl;
        }
    }

    void Callback::testReqProductData()
    {
        m_client->reqProductData(genRequestId());
    }


    void Callback::testReqProductDataSync()
    {
        XtError xterror = XtError();
        vector<xti::CProductData> data;
        data = m_client->reqProductDataSync(xterror);

        for (int i = 0; i < data.size(); ++i)
        {
            cout << "[onReqProductData]  产品净值 :" << data[i].m_dTotalNetValue
                << "\n    产品ID:" << data[i].m_nProductId
                << "\n    当前资金余额:" << data[i].m_dBalance
                << "\n    期初资金余额:" << data[i].m_dPreBalance
                << "\n    期货帐号的可用资金之和:" << data[i].m_dAvaliableFuture
                << "\n    期货账号占用保证金:" << data[i].m_dCurrMargin
                << "\n    期货动态权益之和:" << data[i].m_dBalancefuture
                << "\n    股票总市值:" << data[i].m_dStockValue
                << "\n    债券总市值:" << data[i].m_dLoanValue
                << "\n    基金总市值:" << data[i].m_dFundValue
                << "\n    回购总市值:" << data[i].m_dRepurchaseValue << endl;
        }
        if (xterror.isSuccess())
        {
            cout << "[reqProductDataSync] success errmsg :" << xterror.errorMsg() << endl;
        }
        else
        {
            cout << "[reqProductDataSync] error errmsg :" << xterror.errorMsg() << endl;
        }
    }

    void Callback::testStockOrdinaryOrder(const string& accountId, int times, string accountKey)
    {
        for (int i = 0; i < times; ++i)
        {
            // 参数中所有char[]数组默认值都为空。
            COrdinaryOrder orderInfo;

            // 资金账号，必填参数。不填会被api打回，并且通过onOrder反馈失败
            strcpy(orderInfo.m_strAccountID, accountId.c_str());

            // 单笔超价百分比，选填字段。默认为0
            orderInfo.m_dSuperPriceRate = 0;

            // 报单市场。必填字段。股票市场有"SH"/"SZ"，如果填空或填错都会被api直接打回
            strcpy(orderInfo.m_strMarket, "SZ");

            // 报单合约代码，必填字段。
            strcpy(orderInfo.m_strInstrument, "000001");

            // 报单委托量，必填字段。默认int最大值，填0或不填会被api打回
            orderInfo.m_nVolume = 1000;

            // 报单委托类型。必填字段。根据相应的业务选择，具体请参考XtDataType.h，默认为无效值(OPT_INVALID)。不填会被api打回
            orderInfo.m_eOperationType = OPT_BUY;

            // 报单价格类型，必填字段。默认为无效(PTRP_INVALID)，具体可参考XtDataType.h
            orderInfo.m_ePriceType = PRTP_FIX;

            // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
            orderInfo.m_dPrice = 12.03;

            // 投机套保标志，选填字段。有"投机"/"套利"/"套保"方式。除期货三个方式都可选之外都是填“投机”。默认为“投机”
            orderInfo.m_eHedgeFlag = HEDGE_FLAG_SPECULATION;

            // 直接还款的金额。仅直接还款用，信用业务类型专用
            orderInfo.m_dOccurBalance = 100;

            // 投资备注
            strcpy(orderInfo.m_strRemark, "test004");

            m_client->order(&orderInfo, genRequestId());
            //m_client->directOrder(&orderInfo, genRequestId());
        }
    }

    void Callback::testStockOrdinaryGroupOrder(const string& accountId, string accountKey)
    {
            // 参数中所有char[]数组默认值都为空。
            COrdinaryGroupOrder orderInfo;

            // 资金账号，必填参数。不填会被api打回，并且通过onOrder反馈失败
            strcpy(orderInfo.m_strAccountID, accountId.c_str());

            // 单笔超价百分比，选填字段。默认为0
            orderInfo.m_dSuperPriceRate = 0;

            orderInfo.m_nOrderNum = 3;

            // 合约代码， 必填字段。不填会被api打回
            strcpy(orderInfo.m_strInstrument[0], "000002");
            strcpy(orderInfo.m_strInstrument[1], "600004");
            strcpy(orderInfo.m_strInstrument[2], "600006");

            // 市场，只有"SH"/"SZ"两个市场可以填写
            strcpy(orderInfo.m_strMarket[0], "SZ");
            strcpy(orderInfo.m_strMarket[1], "SH");
            strcpy(orderInfo.m_strMarket[2], "SH");

            // 报单数量
            orderInfo.m_nVolume[0] = 100;
            orderInfo.m_nVolume[1] = 200;
            orderInfo.m_nVolume[2] = 300;

            // 报单委托类型。必填字段。根据相应的业务选择，具体请参考XtDataType.h，默认为无效值(OPT_INVALID)。不填会被api打回
            orderInfo.m_eOperationType[0] = OPT_BUY;
            orderInfo.m_eOperationType[1] = OPT_BUY;
            orderInfo.m_eOperationType[2] = OPT_BUY;

            // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
            orderInfo.m_dPrice[0] = 12;
            orderInfo.m_dPrice[1] = 13;
            orderInfo.m_dPrice[2] = 14;

            // 报单价格类型，必填字段。默认为无效(PTRP_INVALID)，具体可参考XtDataType.h
            orderInfo.m_ePriceType = PRTP_LATEST;

            // 投机套保标志，选填字段。有"投机"/"套利"/"套保"方式。除期货三个方式都可选之外都是填“投机”。默认为“投机”
            orderInfo.m_eHedgeFlag = HEDGE_FLAG_SPECULATION;

            // 投资备注
            strcpy(orderInfo.m_strRemark, "test001");

            m_client->order(&orderInfo, genRequestId());
    }

    void Callback::testHGTOrdinaryOrder(const string& accountId, int times, string accountKey)
    {
        for (int i = 0; i < times; ++i)
        {
            // 参数中所有char[]数组默认值都为空。
            COrdinaryOrder orderInfo;

            // 资金账号，必填参数。不填会被api打回，并且通过onOrder反馈失败
            strcpy(orderInfo.m_strAccountID, accountId.c_str());

            // 单笔超价百分比，选填字段。默认为0
            orderInfo.m_dSuperPriceRate = 0;

            // 报单市场。必填字段。股票市场有"HGT"，如果填空或填错都会被api直接打回
            strcpy(orderInfo.m_strMarket, "HGT");

            // 报单合约代码，必填字段。
            strcpy(orderInfo.m_strInstrument, "00004");

            // 报单委托量，必填字段。默认int最大值，填0或不填会被api打回
            orderInfo.m_nVolume = 1000;

            // 报单委托类型。必填字段。根据相应的业务选择，具体请参考XtDataType.h，默认为无效值(OPT_INVALID)。不填会被api打回
            orderInfo.m_eOperationType = OPT_BUY;

            // 报单价格类型，必填字段。默认为无效(PTRP_INVALID)，具体可参考XtDataType.h
            orderInfo.m_ePriceType = PRTP_LATEST;

            // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
            orderInfo.m_dPrice = 12.3;

            // 投机套保标志，选填字段。有"投机"/"套利"/"套保"方式。除期货三个方式都可选之外都是填“投机”。默认为“投机”
            orderInfo.m_eHedgeFlag = HEDGE_FLAG_SPECULATION;

            // 直接还款的金额。仅直接还款用，信用业务类型专用
            orderInfo.m_dOccurBalance = 100;

            // 投资备注
            strcpy(orderInfo.m_strRemark, "test001");

            m_client->order(&orderInfo, genRequestId());

        }
    }

    void Callback::testSGTOrdinaryOrder(const string& accountId, int times, string accountKey)
    {
        for (int i = 0; i < times; ++i)
        {
            // 参数中所有char[]数组默认值都为空。
            COrdinaryOrder orderInfo;

            // 资金账号，必填参数。不填会被api打回，并且通过onOrder反馈失败
            strcpy(orderInfo.m_strAccountID, accountId.c_str());

            // 单笔超价百分比，选填字段。默认为0
            orderInfo.m_dSuperPriceRate = 0;

            // 报单市场。必填字段。股票市场有"SGT"，如果填空或填错都会被api直接打回
            strcpy(orderInfo.m_strMarket, "SGT");

            // 报单合约代码，必填字段。
            strcpy(orderInfo.m_strInstrument, "00001");

            // 报单委托量，必填字段。默认int最大值，填0或不填会被api打回
            orderInfo.m_nVolume = 1000;

            // 报单委托类型。必填字段。根据相应的业务选择，具体请参考XtDataType.h，默认为无效值(OPT_INVALID)。不填会被api打回
            orderInfo.m_eOperationType = OPT_BUY;

            // 报单价格类型，必填字段。默认为无效(PTRP_INVALID)，具体可参考XtDataType.h
            orderInfo.m_ePriceType = PRTP_LATEST;

            // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
            orderInfo.m_dPrice = 12.3;

            // 投机套保标志，选填字段。有"投机"/"套利"/"套保"方式。除期货三个方式都可选之外都是填“投机”。默认为“投机”
            orderInfo.m_eHedgeFlag = HEDGE_FLAG_SPECULATION;

            // 直接还款的金额。仅直接还款用，信用业务类型专用
            orderInfo.m_dOccurBalance = 100;

            // 投资备注
            strcpy(orderInfo.m_strRemark, "test002");

            m_client->order(&orderInfo, genRequestId());

        }
    }

    void Callback::testCreditOrdinaryOrder(const string& accountId,  int times)
    {
        // 参考股票和期货普通单
        for (int i = 0; i < times; ++i)
        {
            // 参数中所有char[]数组默认值都为空。
            COrdinaryOrder orderInfo;

            // 资金账号，必填参数。不填会被api打回，并且通过onOrder反馈失败
            strcpy(orderInfo.m_strAccountID, accountId.c_str());

            // 单笔超价百分比，选填字段。默认为0
            orderInfo.m_dSuperPriceRate = 0;

            // 报单市场。必填字段。股票市场有"SH"/"SZ"，如果填空或填错都会被api直接打回
            strcpy(orderInfo.m_strMarket, "SH");

            // 报单合约代码，必填字段。
            strcpy(orderInfo.m_strInstrument, "600000");

            // 报单委托量，必填字段。默认int最大值，填0或不填会被api打回
            orderInfo.m_nVolume = 1000;

            // 报单委托类型。必填字段。根据相应的业务选择，具体请参考XtDataType.h，默认为无效值(OPT_INVALID)。不填会被api打回
            orderInfo.m_eOperationType = OPT_FIN_BUY;

            // 报单价格类型，必填字段。默认为无效(PTRP_INVALID)，具体可参考XtDataType.h
            orderInfo.m_ePriceType = PRTP_FIX;

            // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
            orderInfo.m_dPrice = 11.21;

            // 投机套保标志，选填字段。有"投机"/"套利"/"套保"方式。除期货三个方式都可选之外都是填“投机”。默认为“投机”
            orderInfo.m_eHedgeFlag = HEDGE_FLAG_SPECULATION;

            // 直接还款的金额。仅直接还款用，信用业务类型专用
            orderInfo.m_dOccurBalance = 100;

            m_client->order(&orderInfo, genRequestId());

        }
    }

    void Callback::testStockOptionOrdinaryOrder(const std::string& accountId,  int times)
    {
        // 参考股票和期货普通单
        for (int i = 0; i < times; ++i)
        {
            // 参数中所有char[]数组默认值都为空。
            COrdinaryOrder orderInfo;

            // 资金账号，必填参数。不填会被api打回，并且通过onOrder反馈失败
            strcpy(orderInfo.m_strAccountID, accountId.c_str());

            // 单笔超价百分比，选填字段。默认为0
            orderInfo.m_dSuperPriceRate = 0;

            // 报单市场。必填字段。股票市场有"SH"/"SZ"，如果填空或填错都会被api直接打回
            strcpy(orderInfo.m_strMarket, "SZO");

            // 报单合约代码，必填字段。
            strcpy(orderInfo.m_strInstrument, "90006141");

            // 报单委托量，必填字段。默认int最大值，填0或不填会被api打回
            orderInfo.m_nVolume = 10;

            // 报单委托类型。必填字段。根据相应的业务选择，具体请参考XtDataType.h，默认为无效值(OPT_INVALID)。不填会被api打回
            orderInfo.m_eOperationType = OPT_OPTION_BUY_CLOSE;

            // 报单价格类型，必填字段。默认为无效(PTRP_INVALID)，具体可参考XtDataType.h
            orderInfo.m_ePriceType = PRTP_FIX;

            // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
            orderInfo.m_dPrice = 1;

            // 投机套保标志，选填字段。有"投机"/"套利"/"套保"方式。除期货三个方式都可选之外都是填“投机”。默认为“投机”
            orderInfo.m_eHedgeFlag = HEDGE_FLAG_SPECULATION;

            // 直接还款的金额。仅直接还款用，信用业务类型专用
            orderInfo.m_dOccurBalance = 100;

            m_client->order(&orderInfo, genRequestId());

        }
    }

    void Callback::testStockOptionOrdinaryOrder(const std::string& accountId, const std::string& accountKey,  int times)
    {
        // 参考股票和期货普通单
        for (int i = 0; i < times; ++i)
        {
            // 参数中所有char[]数组默认值都为空。
            COrdinaryOrder orderInfo;
            // 资金账号，必填参数。不填会被api打回，并且通过onOrder反馈失败
            strcpy(orderInfo.m_strAccountID, accountId.c_str());
            // 单笔超价百分比，选填字段。默认为0
            orderInfo.m_dSuperPriceRate = 0;
            // 报单市场。必填字段。股票市场有"SH"/"SZ"，如果填空或填错都会被api直接打回
            strcpy(orderInfo.m_strMarket, "SZO");
            // 报单合约代码，必填字段。
            strcpy(orderInfo.m_strInstrument, "90005369");
            // 报单委托量，必填字段。默认int最大值，填0或不填会被api打回
            orderInfo.m_nVolume = 1;
            // 报单委托类型。必填字段。根据相应的业务选择，具体请参考XtDataType.h，默认为无效值(OPT_INVALID)。不填会被api打回
            orderInfo.m_eOperationType = OPT_OPTION_RELEASE_COMB_STRATEGY;
            // 报单价格类型，必填字段。默认为无效(PTRP_INVALID)，具体可参考XtDataType.h
            orderInfo.m_ePriceType = PRTP_OPTION_COMB_STRATEGY_KS;
            // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
            orderInfo.m_dPrice = 1;
            // 投机套保标志，选填字段。有"投机"/"套利"/"套保"方式。除期货三个方式都可选之外都是填“投机”。默认为“投机”
            orderInfo.m_eHedgeFlag = HEDGE_FLAG_SPECULATION;
            // 直接还款的金额。仅直接还款用，信用业务类型专用
            orderInfo.m_dOccurBalance = 100;
            strcpy(orderInfo.m_strSecondInstrument, "90005372");
            strcpy(orderInfo.m_strCombID, "0010QLEKY10002TQ");
            orderInfo.m_dSecondPrice = 1;
            orderInfo.m_eFirstSideFlag = SIDE_FLAG_DUTY;
            orderInfo.m_eSecondSideFlag = SIDE_FLAG_DUTY;

            m_client->order(&orderInfo, genRequestId(), accountKey.c_str());

        }
    }

    void Callback::testFutureOptionOrdinaryOrder(const string& accountId, const std::string& accountKey, int times)
    {
        // 参考股票和期货普通单
        for (int i = 0; i < times; ++i)
        {
            // 参数中所有char[]数组默认值都为空。
            COrdinaryOrder orderInfo;

            // 资金账号，必填参数。不填会被api打回，并且通过onOrder反馈失败
            strcpy(orderInfo.m_strAccountID, accountId.c_str());

            // 单笔超价百分比，选填字段。默认为0
            orderInfo.m_dSuperPriceRate = 0;

            // 报单市场。必填字段。股票市场有"CFFEX"/"SHFE"/"DCE"/"CZCE"，如果填空或填错都会被api直接打回
            strcpy(orderInfo.m_strMarket, "CFFEX");
            //strcpy(orderInfo.m_strMarket, "SHFE");

            // 报单合约代码，必填字段。
            strcpy(orderInfo.m_strInstrument, "IF2009");
            //strcpy(orderInfo.m_strInstrument, "cu2010C33500");

            // 报单委托量，必填字段。默认int最大值，填0或不填会被api打回
            orderInfo.m_nVolume = 1;

            // 报单委托类型。必填字段。根据相应的业务选择，具体请参考XtDataType.h，默认为无效值(OPT_INVALID)。不填会被api打回
            orderInfo.m_eOperationType = OPT_OPEN_LONG;

            // 报单价格类型，必填字段。默认为无效(PTRP_INVALID)，具体可参考XtDataType.h
            orderInfo.m_ePriceType = PRTP_FIX;

            // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
            orderInfo.m_dPrice = 4550;

            // 投机套保标志，选填字段。有"投机"/"套利"/"套保"方式。除期货三个方式都可选之外都是填“投机”。默认为“投机”
            orderInfo.m_eHedgeFlag = HEDGE_FLAG_SPECULATION;

            // 直接还款的金额。仅直接还款用，信用业务类型专用
            orderInfo.m_dOccurBalance = 100;

            //m_client->order(&orderInfo, genRequestId(), accountKey.c_str());
            m_client->order(&orderInfo, genRequestId());

        }
    }


    void Callback::testOrdinaryOrder(AccoutType fundAccountType, const string& accountId,  int times)
    {
        switch(fundAccountType)
        {
            case CB_AT_FUTURE:
                testFutureOrdinaryOrder(accountId, times);
                break;

            case CB_AT_STOCK: // 资金账号为股票类型时
                testStockOrdinaryOrder(accountId, times);
                break;

            case CB_AT_CREDIT:
                testCreditOrdinaryOrder(accountId, times);
                break;

            case CB_AT_STOCK_OPTION:
                testStockOptionOrdinaryOrder(accountId, times);
                break;

            default:
                break;
        }
    }


    // ----------------------算法单（以股票、期货为例，不支持etf申赎）----------------------------------------------

    /*case CB_AT_FUTURE:
        {
            orderInfo.m_nVolume = 1; // 委托量
            strcpy(orderInfo.m_strMarket, "CZCE"); // 市场
            strcpy(orderInfo.m_strInstrument, "CF503"); // 合约代码
            orderInfo.m_eOperationType = OPT_OPEN_LONG; // 委托类型
            orderInfo.m_dPrice = 12895;// 当PriceType为PTRP_FIX时，必须填写。如果不为指定价，则apiservice会根据行情获取相应价格
            orderInfo.m_ePriceType = PRTP_LATEST;
        }
        break;

    case CB_AT_CREDIT:
        {
            orderInfo.m_nVolume = 100;
            strcpy(orderInfo.m_strMarket, "SH");
            strcpy(orderInfo.m_strInstrument, "600000");
            orderInfo.m_eOperationType = OPT_FIN_BUY;
            orderInfo.m_dPrice = 18;// 当PriceType为PTRP_FIX时，必须填写
            orderInfo.m_ePriceType = PRTP_LATEST;
        }
        break;

    case CB_AT_STOCK_OPTION:
        {
            orderInfo.m_nVolume = 1;
            strcpy(orderInfo.m_strMarket, "SHO");
            strcpy(orderInfo.m_strInstrument, "11120100");   
            orderInfo.m_eOperationType = OPT_OPTION_BUY_OPEN;
            orderInfo.m_dPrice = 18;// 当PriceType为PTRP_FIX时，必须填写
            orderInfo.m_ePriceType = PRTP_LATEST;
        }
        break;
    */

    void Callback::testAlgorithmOrder(AccoutType fundAccountType, const string& accountId) 
    {
        // 这里以股票为例，期货、信用和股票期权见上面
        CAlgorithmOrder orderInfo;

        // 资金账号，必填字段。如果不填写会被api打回
        strcpy(orderInfo.m_strAccountID, accountId.c_str());

        // 单笔超价比率，必填字段。
        orderInfo.m_dSuperPriceRate = 0.2;  

        // 指令有效起始终止时间，api处理，写了也没用
        orderInfo.m_nValidTimeStart = time(NULL);
        orderInfo.m_nValidTimeEnd = time(NULL) + 1800;

        // 报单下撤单间隔，股票最小为10s，期货为0.5s
        orderInfo.m_dPlaceOrderInterval = 10; 
        orderInfo.m_dWithdrawOrderInterval = 10; 

        // 超价起始笔数，默认为1
        orderInfo.m_nSuperPriceStart = 1;

        // 报单量，必填字段。不可为0，默认值为无效值。不填或填0或被api打回
        orderInfo.m_nVolume = 1000;

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
        orderInfo.m_eSingleVolumeType = VOLUME_FIX;

        // 投机套保标志，选填字段。有"投机"/"套利"/"套保"方式。除期货三个方式都可选之外都是填“投机”。默认为“投机”
        orderInfo.m_eHedgeFlag = HEDGE_FLAG_SPECULATION;

        // 市场，必填字段。应该填写MarketType.h里的，股票市场有"SH"/"SZ"，如果填空或填错都会被api直接打回
        strcpy(orderInfo.m_strMarket, "CFFEX");

        // 合约代码，必填字段。
        strcpy(orderInfo.m_strInstrument, "IF2009");

        // 报单委托类型。必填字段。根据相应的业务选择，具体请参考XtDataType.h，默认为无效值(OPT_INVALID)。不填会被api打回
        orderInfo.m_eOperationType = OPT_OPEN_LONG;

        // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
        orderInfo.m_dPrice = 222.2;

        // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
        orderInfo.m_ePriceType = PRTP_FIX;

        orderInfo.m_eTimeCondition = TIME_CONDITION_IOC;
        orderInfo.m_eVolumeCondition = VOLUME_CONDITION_MIN;

        //requestID，本地用于确定服务器返回的 
        m_client->order(&orderInfo, genRequestId());
    }

    void Callback::testExternAlgorithmOrder(const std::string& accoundId)
    {
        // 这里以股票为例，期货、信用和股票期权见上面
        CExternAlgorithmOrder orderInfo;
        // 资金账号，必填字段。如果不填写会被api打回
        strcpy(orderInfo.m_strAccountID, accoundId.c_str());
        // 指令有效起始终止时间，api处理，写了也没用
        orderInfo.m_nValidTimeStart = time(NULL);
        orderInfo.m_nValidTimeEnd = time(NULL) + 1800;
        // 报单量，必填字段。不可为0，默认值为无效值。不填或填0或被api打回
        orderInfo.m_nVolume = 1000;
        // 市场，必填字段。应该填写MarketType.h里的，股票市场有"SH"/"SZ"，如果填空或填错都会被api直接打回
        strcpy(orderInfo.m_strMarket, "SH");
        // 合约代码，必填字段。
        strcpy(orderInfo.m_strInstrument, "600000");
        // 报单委托类型。必填字段。根据相应的业务选择，具体请参考XtDataType.h，默认为无效值(OPT_INVALID)。不填会被api打回
        orderInfo.m_eOperationType = OPT_BUY;
        // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
        orderInfo.m_dPrice = 222.2;
        //算法名称
        strcpy(orderInfo.m_strOrderType, "ALGOINTERFACE_TEST");
        //requestID，本地用于确定服务器返回的 
        m_client->order(&orderInfo, genRequestId());
    }

    void Callback::testAlgoGroupOrder(const string& accountId, const std::string& accountKey)
    {
        CAlgGroupOrder orderInfo;
        // m_orderParam为算法单结构体，具体请参考面文件
        // 资金账号，必填参数。不填会被api打回，并且通过onOrder反馈失败
        strcpy(orderInfo.m_orderParam.m_strAccountID, accountId.c_str());
        // 报单委托类型。必填字段，目前只有买入和卖出两种方式
        orderInfo.m_orderParam.m_eOperationType = OPT_BUY;
        // 报单价格类型，必填字段。目前只支持市价和指定价
        orderInfo.m_orderParam.m_ePriceType = PRTP_FIX;
        // 报单价格，默认为double最大值。
        orderInfo.m_orderParam.m_dPrice = 222;
        //有效开始时间
        orderInfo.m_orderParam.m_nValidTimeStart = time(NULL) - 1800;
        //有效结束时间
        orderInfo.m_orderParam.m_nValidTimeEnd = time(NULL) + 1800;
        //算法名称，VWAP，TWAP，VP，PINLINE，FLOA
        strcpy(orderInfo.m_orderParam.m_strOrderType, "VWAP");
        //量比比例, 用户设定, 当MaxPartRate==100%, 表示没有限制
        orderInfo.m_orderParam.m_dMaxPartRate = 0.2;
        //委托最小金额
        orderInfo.m_orderParam.m_dMinAmountPerOrder = 0;
        // 股票只数，必填参数，默认值为0。必须大于0，小于等于500
        orderInfo.m_nOrderNum = 2;
        // 合约代码， 必填字段。不填会被api打回
        strcpy(orderInfo.m_strInstrument[0], "000002");
        strcpy(orderInfo.m_strInstrument[1], "600004");
        strcpy(orderInfo.m_strMarket[0], "SZ");
        strcpy(orderInfo.m_strMarket[1], "SH");
        // 报单数量
        orderInfo.m_nVolume[0] = 100;
        orderInfo.m_nVolume[1] = 200;
        // 说明：m_nOrderNum、m_strInstrument、m_strMarket、m_nVolume必须统一
        //m_client->order(&orderInfo, m_nRequestId++);
        XtError error = XtError();
        int orderId = m_client->orderSync(&orderInfo, error, accountKey.c_str());
        if (error.isSuccess())
        {
            cout << "CIntelligentAlgorithmOrder orderId: " << orderId << endl;
            testCancelSync(orderId, accountKey.c_str());
        }
    }

    // ----------------------组合单<只支持股票>----------------------------------------------

    void Callback::testGroupOrder(const string& accountId)
    {
        CGroupOrder orderInfo;


        // m_orderParam为算法单结构体，具体请参考面文件
        // 单笔超价
        orderInfo.m_orderParam.m_dSuperPriceRate = 0.01;
        // 报价类型
        orderInfo.m_orderParam.m_ePriceType = PRTP_LATEST;
        // 下单类型
        orderInfo.m_orderParam.m_eOperationType = OPT_BUY;
        // 超价起始笔数
        orderInfo.m_orderParam.m_nSuperPriceStart = 1;
        // 下单间隔(秒）
        orderInfo.m_orderParam.m_dPlaceOrderInterval = 30;
        // 撤单间隔（秒）
        orderInfo.m_orderParam.m_dWithdrawOrderInterval = 30;
        // 单比下单比率(1 为一次全部下单）
        orderInfo.m_orderParam.m_dSingleVolumeRate = 1; 
        // 单笔下单基准
        orderInfo.m_orderParam.m_eSingleVolumeType = VOLUME_FIX;
        // 最大下单次数
        orderInfo.m_orderParam.m_nMaxOrderCount = 100;
        // 单笔下单量最大值，必须大于或等于 m_nVolume[i] * m_dSingleVolumeRate
        // 否则，以单笔下单量最大值为准
        orderInfo.m_orderParam.m_nSingleNumMax = 200;
        // 单笔下单量最小值, 不能比100 再小了
        orderInfo.m_orderParam.m_nLastVolumeMin = 100;

        // 资金账号，必填字段。如果不填写会被api打回
        strcpy(orderInfo.m_orderParam.m_strAccountID, accountId.c_str());

        // 股票只数，必填参数，默认值为0。必须大于0，小于等于500
        orderInfo.m_nOrderNum = 2;

        // 合约代码， 必填字段。不填会被api打回
        strcpy(orderInfo.m_strInstrument[0], "000002");
        strcpy(orderInfo.m_strInstrument[1], "000004");

        // 市场，只有"SH"/"SZ"两个市场可以填写
        strcpy(orderInfo.m_strMarket[0], "SZ");
        strcpy(orderInfo.m_strMarket[1], "SZ");

        // 报单数量
        orderInfo.m_nVolume[0] = 100;
        orderInfo.m_nVolume[1] = 200;

        // 说明：m_nOrderNum、m_strInstrument、m_strMarket、m_nVolume必须统一
        m_client->order(&orderInfo, m_nRequestId++);
    }


    void Callback::testRandomOrder(const string& accountId) 
    {

        CRandomOrder orderInfo;

        // 资金账号，必填字段。如果不填写会被api打回
        strcpy(orderInfo.m_strAccountID, accountId.c_str());

        //单笔量区间左值，必填字段，默认值为0
        orderInfo.m_nSingleNumMin = 100;

        //单笔量区间右值，必填字段
        orderInfo.m_nSingleNumMax = 500;

        // 报单量，必填字段。不可为0，默认值为无效值。不填或填0或被api打回
        orderInfo.m_nVolume = 1000;

        orderInfo.m_nValidTimeElapse = 60*60;

        // 市场，必填字段。应该填写MarketType.h里的，股票市场有"SH"/"SZ"，如果填空或填错都会被api直接打回
        strcpy(orderInfo.m_strMarket, "SH");

        // 合约代码，必填字段。
        strcpy(orderInfo.m_strInstrument, "600000");

        // 报单委托类型。必填字段。根据相应的业务选择，具体请参考XtDataType.h，默认为无效值(OPT_INVALID)。不填会被api打回
        orderInfo.m_eOperationType = OPT_BUY;

        // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
        orderInfo.m_dPrice = 12.3;

        // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
        orderInfo.m_ePriceType = PRTP_LATEST;

        //requestID，本地用于确定服务器返回的 
        m_client->order(&orderInfo, genRequestId());
    }

    void Callback::testIntelligentAlgorithmOrder(const string& accountId, const std::string& accountKey)
    {
        cout << "testIntelligentAlgorithmOrder start"<< endl;
        // 参数中所有char[]数组默认值都为空。
        CIntelligentAlgorithmOrder orderInfo;
        // 资金账号，必填参数。不填会被api打回，并且通过onOrder反馈失败
        strcpy(orderInfo.m_strAccountID, accountId.c_str());
        // 报单市场。必填字段。股票市场有"SH"/"SZ"，如果填空或填错都会被api直接打回
        strcpy(orderInfo.m_strMarket, "SH");
        // 报单合约代码，必填字段。
        strcpy(orderInfo.m_strInstrument, "600004");
        //算法名称，VWAP，TWAP，VP，PINLINE，DMA，FLOAT，MSO，SWITCH，ICEBERG，MOC，GRID，VWAPPLUS，MOO，IS，STWAP，SLOS，VPPLUS，XTFAST，SLOH，MOOPLUS，IVWAP，VWAPPLUS2
        strcpy(orderInfo.m_strOrderType, "MOOPLUS");
        // 报单价格，默认为double最大值。
        orderInfo.m_dPrice = 12.3;
        // 报单委托量，必填字段。默认int最大值，填0或不填会被api打回
        orderInfo.m_nVolume = 10000;
        //有效开始时间
        orderInfo.m_nValidTimeStart = time(NULL) - 1800;
        //有效结束时间
        orderInfo.m_nValidTimeEnd = time(NULL) + 1800;
        //量比比例, 用户设定, 当MaxPartRate==100%, 表示没有限制
        orderInfo.m_dMaxPartRate = 0.2;
        //委托最小金额
        orderInfo.m_dMinAmountPerOrder = 0;
        // 报单委托类型。必填字段，目前只有买入和卖出两种方式
        orderInfo.m_eOperationType = OPT_BUY;
        // 报单价格类型，必填字段。目前只支持市价和指定价
        orderInfo.m_ePriceType = PRTP_FIX;
        //投资备注
        strcpy(orderInfo.m_strRemark, "mooplus test");
        //开盘集合竞价参与比例(取值0-1) 仅开盘+算法有用
        orderInfo.m_dOrderRateInOpenAcution = 0.5;
        //开盘集合竞价价格偏移量(取值0-10000) 仅开盘+算法有用
        orderInfo.m_dPriceOffsetBpsForAuction = 100;
        //涨跌停控制
        orderInfo.m_nStopTradeForOwnHiLow = STOPTRADE_NONE;
        //收盘后是否继续执行， 0不继续，非0继续
        orderInfo.m_nMaxTradeDurationAfterET = 0;
        //算法下单方式
        orderInfo.m_eOrderStrategyType = E_ORDER_STRATEGY_TYPE_NORMAL;
        //m_client->order(&orderInfo, genRequestId());
        XtError error = XtError();
        int orderId = m_client->orderSync(&orderInfo, error, accountKey.c_str());
        if (error.isSuccess())
        {
            cout << "CIntelligentAlgorithmOrder orderId: " << orderId << endl;
            testCancelSync(orderId, accountKey.c_str());
        }
    }


    void Callback::testCancelSync(int orderID, const char* accountKey)
    {
        XtError error = XtError();
        orderID = 472;
        m_client->cancelSync(orderID, error,accountKey);
        if (error.isSuccess())
        {
            cout << "testCancelSync success, orderID:" << orderID << ", accountkey:" << accountKey << endl;
        }
    }

    // ----------------------撤委托----------------------------------------------

    void Callback::testCancelOrder(AccoutType fundAccountType, const char* accountId)
    {
        switch(fundAccountType)
        {
            case CB_AT_STOCK:
                {
                    char* market = "SZ";
                    char* code = "000002";
                    char orderSyeId[32];
                    strcpy(orderSyeId, "B2151109");
                    m_client->cancelOrder(accountId, orderSyeId, market, code, genRequestId());
                }
                break;

            case CB_AT_FUTURE:
                {
                    char* market = "CFFEX";
                    char* code = "IF1504";
                    char orderSyeId[32];
                    strcpy(orderSyeId,"1288606");
                    m_client->cancelOrder(accountId, orderSyeId, market, code, genRequestId());
                }
                break;
        }
    }

    void Callback::checkOrdinaryOrder(const string& accountId)
    {
        // 参数中所有char[]数组默认值都为空。
        COrdinaryOrder orderInfo;

        // 资金账号，
        strcpy(orderInfo.m_strAccountID, accountId.c_str());

        // 单笔超价百分比，选填字段。默认为0
        orderInfo.m_dSuperPriceRate = 0;

        // 报单市场。必填字段。股票市场有"SH"/"SZ"
        strcpy(orderInfo.m_strMarket, "SH");

        // 报单合约代码，必填字段。
        strcpy(orderInfo.m_strInstrument, "600000");

        // 报单委托量，必填字段。默认int最大值
        orderInfo.m_nVolume = 1000;

        // 报单委托类型。必填字段。根据相应的业务选择，具体请参考XtDataType.h，默认为无效值(OPT_INVALID)。不填会被api打回

        orderInfo.m_eOperationType = OPT_BUY;

        // 报单价格类型，必填字段。默认为无效(PTRP_INVALID)，具体可参考XtDataType.h
        orderInfo.m_ePriceType = PRTP_FIX;

        // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
        orderInfo.m_dPrice = 12.3;

        // 投机套保标志，选填字段。有"投机"/"套利"/"套保"方式。除期货三个方式都可选之外都是填“投机”。默认为“投机”
        orderInfo.m_eHedgeFlag = HEDGE_FLAG_SPECULATION;

        // 直接还款的金额。仅直接还款用，信用业务类型专用
        orderInfo.m_dOccurBalance = 100;

        m_client->check(&orderInfo, genRequestId());
    }

    void Callback::onOrder(int nRequestId, int orderId, const char* strRemark, const XtError& error)
    {
        cout << "[" <<__FUNCTION__ <<"] isSuccess: " << (error.isSuccess()?"true":"false") 
            << "\n    orderId:  " << orderId
            << "\n    RequestId: " << nRequestId  
            << "\n    strRemark: " << strRemark
            << "\n    errorMsg: " << error.errorMsg()
            << endl;
        if (error.isSuccess())
        {
            // 撤单<撤单与撤委托的区别请详见常见错误文档>
            //utils::sleep(1);
            //m_client->cancel(orderId, genRequestId());
        }
    }


    void Callback::onDirectOrder(int nRequestId, const char* strOrderSysID, const char* strRemark, const XtError& error)
    {
        if (error.isSuccess())
        {
            cout << "onDirectOrder strOrderSysID:" << strOrderSysID << endl;
        }
        else
        {
            cout << "onDirectOrder failed errmsg:" << error.errorMsg() << endl;
        }
        m_nRespCnt += 1;
        if (m_nRespCnt == 2)
        {
            cout << "onDirectOrder all finished" << endl;
        }
    }

    void Callback::onReqCInstrumentDetail(const char* accountId, int nRequestId, const CInstrumentDetail* data, bool isLast, const XtError& error)
    {
        if (NULL != data)
        {

            cout << "[" << __FUNCTION__ << "]"
                << "\n    合约代码: " << data->m_strInstrumentID
                << "\n    期权标的代码: " << data->m_strOptUndlCode
                <<endl;
        }
    }


    void Callback::onBatchReqCInstrumentDetail(const char* accountID, int nRequestId, std::vector<CInstrumentDetail>* data, bool isLast, const XtError& error)
    {

    }

    void Callback::onCancel(int nRequestId, const XtError& error)
    {
        cout << "[onCancel] success:  " << (error.isSuccess()?"true":error.errorMsg()) << ", requestID: " << nRequestId << endl;
    }

    void Callback::onCancelOrder(int nRequestId, const XtError& error)
    {
        cout << "[onCancelOrder] success:  " << (error.isSuccess()?"true":error.errorMsg()) << ", requestID: " << nRequestId << endl;
    }

    void Callback::onCheck(int nRequestId ,const CCheckData* checkData , const XtError& error)
    {
        if (checkData)
        {
            if (checkData->m_singleResult.isSuccess())
            {
                cout<< "[" << __FUNCTION__ << "]"<<"singleResult : true" <<endl;
            }
            else
            {
                cout<< "[" << __FUNCTION__ << "]"
                    << "singleResult : has error" 
                    << checkData->m_singleResult.errorMsg() <<endl;
            }
            if (checkData->m_allResult.isSuccess())
            {
                cout<< "[" << __FUNCTION__ << "]"<<"allResult : true" <<endl;
            } 
            else
            {
                cout<< "[" << __FUNCTION__ << "]"
                    << "allResult : has error" 
                    << checkData->m_allResult.errorMsg() <<endl;
            }
        }

    }
    void Callback::onUserLogout(const string& userName, const string& password, int nRequestId, const XtError& error) 
    {
        cout << "[onUserLogout]" << endl;
    }

    // 通用
    void Callback::onReqAccountDetail(const char* accountId, int nRequestId, const CAccountDetail* data, bool isLast, const XtError& error)
    {
        cout << "[onReqAccountDetail] accountId: " << accountId << ", success: " << (error.isSuccess()?"true":error.errorMsg()) << endl;
    }

    void Callback::onBatchReqAccountDetail(const char* accountId, int nRequestId, std::vector<CAccountDetail>* data, bool isLast, const XtError& error)
    {
        cout << "[onBatchReqAccountDetail] accountId: " << accountId << ", success: " << (error.isSuccess() ? "true" : error.errorMsg())<< "records:"<< (*data).size() << endl;
        cout << (*data)[0].m_strAccountID << endl;
    }

    void Callback::onReqCreditAccountDetail(const char* accountId, int nRequestId, const CCreditAccountDetail* data, bool isLast, const XtError& error) 
    {
        cout << "[onReqCreditAccountDetail] accountId: " << accountId << ", success: " << (error.isSuccess()?"true":error.errorMsg()) << endl;
    }

    void Callback::onBatchReqCreditAccountDetail(const char* accountId, int nRequestId, std::vector<CCreditAccountDetail>* data, bool isLast, const XtError& error)
    {
        cout << "[onBatchReqCreditAccountDetail] accountId: " << accountId << ", success: " << (error.isSuccess() ? "true" : error.errorMsg()) << "records:" << (*data).size() << endl;
    }

    void Callback::onReqOrderDetail(const char* accountId, int nRequestId, const COrderDetail* data, bool isLast, const XtError& error)
    {
        cout << "[onReqOrderDetail] accountId: " << accountId << ", success: " << (error.isSuccess()?"true":error.errorMsg()) << endl;
    }

    void Callback::onBatchReqOrderDetail(const char* accountId, int nRequestId, std::vector<COrderDetail>* data, bool isLast, const XtError& error)
    {
        cout << "[onBatchReqOrderDetail] accountId: " << accountId << ", success: " << (error.isSuccess() ? "true " : error.errorMsg())<<"islast: "<<(isLast?"true ":"false ")<< "records:" << (*data).size() << endl;
        //for (int i = 0; i < (*data).size(); ++i)
        //{
        //    cout << (*data)[i].m_nOrderID << "," << (*data)[i].m_strOrderSysID << endl;
        //}
    }
    void Callback::onReqDealDetail(const char* accountId, int nRequestId, const CDealDetail* data, bool isLast, const XtError& error)
    {
        cout << "[onReqDealDetail] accountId: " << accountId << ", success: " << (error.isSuccess()?"true":error.errorMsg()) << endl;
    }

    void Callback::onBatchReqDealDetail(const char* accountID, int nRequestId, std::vector<CDealDetail>* data, bool isLast, const XtError& error)
    {
        cout << "[onBatchReqDealDetail] accountId: " << accountID << ", success: " << (error.isSuccess() ? "true " : error.errorMsg()) << " islast: " << (isLast ? "true ":"false ") << "records:" << "records:" << (*data).size() << endl;
        for (int i=0; i< (*data).size(); ++i)
        {
            cout << (*data)[i].m_nOrderID << "," << (*data)[i].m_strOrderSysID << endl;
        }
    }

    void Callback::onReqPositionDetail(const char* accountId, int nRequestId, const CPositionDetail* data, bool isLast, const XtError& error)
    {
        if (data)
        {
            cout << "[onReqPositionDetail] accountId: " << accountId << ", success: " << (error.isSuccess() ? "true" : error.errorMsg()) << "   m_strInstrumentID: " << data->m_strInstrumentID << "m_nVolume: " << data->m_nVolume << "m_dSettlementPrice: " << data->m_dSettlementPrice <<" m_nCanUseVolume: "<<data->m_nCanUseVolume << endl;

        }
    }

    void Callback::onBatchReqPositionDetail(const char* accountID, int nRequestId, std::vector <CPositionDetail>* data, bool isLast, const XtError& error)
    {
        cout << "[onBatchReqPositionDetail] accountId: " << accountID << ", success: " << (error.isSuccess() ? "true" : error.errorMsg()) << "records:" << (*data).size() << endl;
        for (int i = 0; i< (*data).size(); ++i)
        {
            CPositionDetail  positionData = (*data)[i];
            cout <<"m_strInstrumentID"<< (positionData).m_strInstrumentID << endl;
        }
    }

    void Callback::onReqPositionStatics(const char* accountId, int nRequestId, const CPositionStatics* data, bool isLast, const XtError& error)
    {
        if (data)
        {
            cout << "[onReqPositionStatics] accountId: " << accountId << ", success: " << (error.isSuccess() ? "true" : error.errorMsg()) << "m_nCoveredAmount:" << data->m_nCoveredAmount << endl;
        }
    }


    void Callback::onBatchReqPositionStatics(const char* accountID, int nRequestId, std::vector<CPositionStatics>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onReqStkOptCombPositionDetail(const char* accountId, int nRequestId, const CStockOptionCombPositionDetail* data, bool isLast, const XtError& error)
    {
        cout << "[onReqStkOptCombPositionDetail] accountId: " << accountId << ", success: " << (error.isSuccess()?"true":error.errorMsg()) << "m_strInstrumentID:" <<endl;
    }


    void Callback::onBatchReqStkOptCombPositionDetail(const char* accountID, int nRequestId, std::vector<CStockOptionCombPositionDetail>* data, bool isLast, const XtError& error)
    {

    }

    // 信用
    void Callback::onReqStksubjects(const char* accountId, int nRequestId, const CStkSubjects* data, bool isLast, const XtError& error)
    {
        cout << "[onReqStksubjects] accountId: " << accountId << ", success: " << (error.isSuccess()?"true":error.errorMsg()) << endl;
    }


    void Callback::onBatchReqStksubjects(const char* accountID, int nRequestId, std::vector<CStkSubjects>* data, bool isLast, const XtError& error)
    {

    }

    void Callback::onReqStkcompacts(const char* accountId, int nRequestId, const CStkCompacts* data, bool isLast, const XtError& error)
    {
        cout << "[onReqStkcompacts] accountId: " << accountId << ", success: " << (error.isSuccess()?"true":error.errorMsg()) << endl;
    }


    void Callback::onBatchReqStkcompacts(const char* accountID, int nRequestId, std::vector<CStkCompacts>* data, bool isLast, const XtError& error)
    {

    }

    // 股票期权
    void Callback::onReqCoveredStockPosition(const char* accountId, int nRequestId, const CCoveredStockPosition* data, bool isLast, const XtError& error)
    {
        cout << "[onReqCoveredStockPosition] accountId: " << accountId << ", success: " << (error.isSuccess()?"true":error.errorMsg()) << endl;
    }


    void Callback::onBatchReqCoveredStockPosition(const char* accountID, int nRequestId, std::vector<CCoveredStockPosition>* data, bool isLast, const XtError& error)
    {

    }

    void Callback::onReqReferenceRate(const char* accountId, int nRequestId, const CReferenceRate* data, bool isLast, const XtError& error)
    {
        cout << "[onReqReferenceRate] accountId: " << accountId << ", success: " << (error.isSuccess()?"true":error.errorMsg()) << endl;
    }


    void Callback::onBatchReqReferenceRate(const char* accountID, int nRequestId, std::vector<CReferenceRate>* data, bool isLast, const XtError& error)
    {

    }

    void Callback::onReqCreditDetail(const char* accountId, int nRequestId, const CCreditDetail* data, bool isLast, const XtError& error)
    {
        cout << "[onReqCreditDetail] accountId: " << accountId << ", success: " << (error.isSuccess()?"true":error.errorMsg()) << endl;
    }


    void Callback::onBatchReqCreditDetail(const char* accountID, int nRequestId, std::vector<CCreditDetail>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqSubscribeInfo(const char* accountID, int nRequestId, std::vector<CSubscribeInfo>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqStkUnCloseCompact(const char* accountID, int nRequestId, std::vector<CStkUnClosedCompacts>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqStkClosedCompact(const char* accountID, int nRequestId, std::vector<CStkClosedCompacts>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqAccountKey(int nRequestId, std::vector<CAccountKey>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqDealDetailBySysID(const char* accountID, int nRequestId, const char* orderSyeId, const char* exchangeId, std::vector<CDealDetail>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqDeliveryDetail(const char* accountID, int nRequestId, std::vector<CDeliveryDetail>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqCreditSloCode(const char* accountID, int nRequestId, std::vector<CCreditSloCode>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqCreditSubjects(const char* accountID, int nRequestId, std::vector<CCreditSubjects>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqCreditAssure(const char* accountID, int nRequestId, std::vector<CCreditAssure>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqTransferBank(const char* accountID, int nRequestId, std::vector<CQueryBankInfo>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqTransferSerial(const char* accountID, int nRequestId, std::vector<CTransferSerial>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqInstrumentInfoByMarket(int nRequestId, std::vector<CInstrumentInfo>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqCanCancelOrderDetail(const char* accountID, int nRequestId, std::vector<COrderDetail>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqCommandsInfo(int nRequestId, std::vector<COrderInfo>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqComFund(const char* accountID, int nRequestId, std::vector<CStockComFund>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqComPosition(const char* accountID, int nRequestId, std::vector<CStockComPosition>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqHistoryOrderDetail(const char* accountID, int nRequestId, std::vector<COrderDetail>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqHistoryDealDetail(const char* accountID, int nRequestId, std::vector<CDealDetail>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqHistoryPositionStatics(const char* accountID, int nRequestId, std::vector<CPositionStatics>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqProductPortfolio(int nProductID, int nRequestId, std::vector<CPortfolioInfo>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqPortfolioOrder(int nPortfolioID, int nRequestId, std::vector<COrderDetail>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqPortfolioMultiOrder(int nPortfolioID, int nRequestId, std::vector<COrderDetail>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqPortfolioDeal(int nPortfolioID, int nRequestId, std::vector<CDealDetail>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqPortfolioMultiDeal(int nPortfolioID, int nRequestId, std::vector<CDealDetail>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqPortfolioPosition(int nPortfolioID, int nRequestId, std::vector<CPositionStatics>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqStrategyInfo(const char* accountID, int nRequestId, const char* accountKey, std::vector<CStrategyInfo>* data, bool isLast, const XtError& error)
    {

    }


    void Callback::onBatchReqSecuAccount(const char* accountID, int nRequestId, const char* accountKey, std::vector<CSecuAccount>* data, bool isLast, const XtError& error)
    {

    }

    void Callback::onReqProductData(int nRequestId, const CProductData* data, bool isLast, const XtError& error)
    {
        if (error.isSuccess())
        {
            cout << "[onReqProductData]  产品净值 :" << data->m_dTotalNetValue
                << "\n    产品ID:" << data->m_nProductId
                << "\n    当前资金余额:" << data->m_dBalance
                << "\n    期初资金余额:" << data->m_dPreBalance
                << "\n    期货帐号的可用资金之和:" << data->m_dAvaliableFuture
                << "\n    期货账号占用保证金:" << data->m_dCurrMargin
                << "\n    期货动态权益之和:" << data->m_dBalancefuture
                << "\n    股票总市值:" << data->m_dStockValue
                << "\n    债券总市值:" << data->m_dLoanValue
                << "\n    基金总市值:" << data->m_dFundValue
                << "\n    回购总市值:" << data->m_dRepurchaseValue << endl;
        }
        else
        {
            cout << "[onReqProductData] error errmsg :" << error.errorMsg();
        }



    }


    void Callback::onBatchReqProductData(int nRequestId, std::vector<CProductData>* data, bool isLast, const XtError& error)
    {
        for (int i = 0; i< (*data).size(); ++i)
        {
            CProductData  productData = (*data)[i];
            cout << "[onReqProductData]  产品净值 :" << productData.m_dTotalNetValue
                << "\n    产品ID:" << productData.m_nProductId
                << "\n    当前资金余额:" << productData.m_dBalance
                << "\n    期初资金余额:" << productData.m_dPreBalance
                << "\n    期货帐号的可用资金之和:" << productData.m_dAvaliableFuture
                << "\n    期货账号占用保证金:" << productData.m_dCurrMargin
                << "\n    期货动态权益之和:" << productData.m_dBalancefuture
                << "\n    股票总市值:" << productData.m_dStockValue
                << "\n    债券总市值:" << productData.m_dLoanValue
                << "\n    基金总市值:" << productData.m_dFundValue
                << "\n    回购总市值:" << productData.m_dRepurchaseValue << endl;
        }

    }

    void Callback::onReqPriceData(int nRequestId, const CPriceData* data, const XtError& error)
    {
        cout << "[" << __FUNCTION__ << "]";
        if (!error.isSuccess())
        {
            cout << "error msg: " << error.errorMsg() << endl;
        }
        else
        {
            cout << " m_strInstrumentID : "<< data->m_strInstrumentID << " m_dLastPrice :" << data->m_dLastPrice<<endl;
        }
    }

    void Callback::onSubscribQuote(int nRequestId, const CSubscribData* data, const XtError& error)
    {
        if (error.isSuccess())
        {
            cout << __FUNCTION__ << " 合约：" << data->m_strInstrumentID
                << " 市场 " << data->m_strExchangeID << " sub success " << endl;
        }
        else
        {
            cout << __FUNCTION__ << " 合约：" << data->m_strInstrumentID
                << " 市场 " << data->m_strExchangeID << "  error msg: "
                << error.errorMsg() << endl;
            cout << endl;
            cout << endl;

        }
    }

    void Callback::onUnSubscribQuote(int nRequestId, const CSubscribData* data, const XtError& error)
    {
        cout << __FUNCTION__ <<"合约：" <<data->m_strInstrumentID
            <<"市场"<< data->m_strExchangeID 
            <<"  error msg: "<<error.errorMsg() << "end"<< endl;
    }

    void Callback::onRtnPriceData(const CPriceData& data)
    {
        cout<<__FUNCTION__ <<"Receive PirceData: "<<data.m_strExchangeID<<"  "<<data.m_strInstrumentID<< endl;
        // 参数中所有char[]数组默认值都为空。
        COrdinaryOrder orderInfo;
        // 资金账号，必填参数。不填会被api打回，并且通过onOrder反馈失败
        strcpy(orderInfo.m_strAccountID, m_strStockAccount.c_str());
        // 单笔超价百分比，选填字段。默认为0
        orderInfo.m_dSuperPriceRate = 0;
        // 报单市场。必填字段。股票市场有"SH"/"SZ"，如果填空或填错都会被api直接打回
        strcpy(orderInfo.m_strMarket, data.m_strExchangeID);
        // 报单合约代码，必填字段。
        strcpy(orderInfo.m_strInstrument, data.m_strInstrumentID);
        // 报单委托量，必填字段。默认int最大值，填0或不填会被api打回
        orderInfo.m_nVolume = 1000;
        // 报单委托类型。必填字段。根据相应的业务选择，具体请参考XtDataType.h，默认为无效值(OPT_INVALID)。不填会被api打回
        orderInfo.m_eOperationType = OPT_BUY;
        // 报单价格类型，必填字段。默认为无效(PTRP_INVALID)，具体可参考XtDataType.h
        orderInfo.m_ePriceType = PRTP_FIX;
        // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
        orderInfo.m_dPrice = data.m_dLastPrice;
        // 投机套保标志，选填字段。有"投机"/"套利"/"套保"方式。除期货三个方式都可选之外都是填“投机”。默认为“投机”
        orderInfo.m_eHedgeFlag = HEDGE_FLAG_SPECULATION;
        // 投资备注
        strcpy(orderInfo.m_strRemark, "test orderByQuote");
        //m_client->order(&orderInfo, genRequestId());
    }

    // 主推类接口回调函数
    void Callback::onRtnOrder(const COrderInfo* data)
    {
        string orderStatus = "";
        switch(data->m_eStatus)
        {
        case OCS_CHECKING:   orderStatus = "风控检查中";  break;
        case OCS_APPROVING:  orderStatus = "审批中";  break;
        case OCS_REJECTED:   orderStatus = "已驳回";  break;
        case OCS_RUNNING:    orderStatus = "运行中";  break;
        case OCS_CANCELING:  orderStatus = "撤销中";  break;
        case OCS_FINISHED:   orderStatus = "已完成";  break;
        case OCS_STOPPED:    orderStatus = "已撤销";  break;
        }

        cout << "[" << __FUNCTION__ << "]"
            << "\n    下单ID: " << data->m_nOrderID
            << "\n    m_startTime：" << data->m_startTime
            << "\n    m_endTime: " << data->m_endTime
            << "\n    指令状态：" << orderStatus
            << "\n    成交量：" << data->m_dTradedVolume
            << "\n    撤销者：" << data->m_canceler
            << "\n    指令执行信息：" << data->m_strMsg
            << endl;
    }

    void Callback::onRtnOrderDetail(const COrderDetail* data)
    {
        string entrust_status;
        switch(data->m_eOrderStatus)
        {
        case ENTRUST_STATUS_UNREPORTED:  entrust_status = "未报";  break;
        case ENTRUST_STATUS_WAIT_REPORTING:  entrust_status = "待报"; break;
        case ENTRUST_STATUS_REPORTED:        entrust_status = "已报"; break;
        case ENTRUST_STATUS_REPORTED_CANCEL: entrust_status = "已报待撤";  break;
        case ENTRUST_STATUS_PARTSUCC_CANCEL: entrust_status = "部成待撤";  break;
        case ENTRUST_STATUS_PART_CANCEL:     entrust_status = "部撤";  break;
        case ENTRUST_STATUS_CANCELED:        entrust_status = "已撤";  break;
        case ENTRUST_STATUS_PART_SUCC:       entrust_status = "部成";  break;
        case ENTRUST_STATUS_SUCCEEDED:       entrust_status = "已成";  break;
        case ENTRUST_STATUS_JUNK:            entrust_status = "废单";  break;
        }
        if (data == NULL)
        {
            return;
        }
        cout << "[onRtnOrderDetail]"
            << "\n    委托号：" << data->m_strOrderSysID
            << "\n    委托状态：" << entrust_status
            << "\n    已成交量：" << data->m_nTradedVolume 
            << "\n    成交均价：" << data->m_dTradeAmount 
            << "\n    成交额: " << data->m_dTradeAmount 
            << "\n    市场ID：" << data->m_strExchangeID
            << "\n    产品ID：" << data->m_strProductID
            << "\n    股票/期货代码：" << data->m_strInstrumentID
            << "\n    冻结保证金：" << data->m_dFrozenMargin
            << "\n    冻结手续费：" << data->m_dFrozenCommission
            << "\n    ErrorID：" << data->m_nErrorID
            << "\n    ErrorMsg: " << data->m_strErrorMsg
            << endl;

    }


    void Callback::onRtnDealDetail(const CDealDetail* data)
    {
        if (data == NULL)
        {
            return;
        }
        cout << "[" << __FUNCTION__ << "]"
            << "\n    orderId: " << data->m_nOrderID 
            << "\n    成交量： " << data->m_nVolume
            << "\n    成交额: " << data->m_dAmount
            << "\n    成交均价： " << data->m_dAveragePrice
            << endl;
    }

    void Callback::onRtnOrderError(const COrderError* data)
    {
        if (data == NULL)
        {
            return;
        }
        cout << "[onRtnOrderError] orderId: " << data->m_nOrderID 
            << "\n    error id: " << data->m_nErrorID
            << "\n    errormsg: " << data->m_strErrorMsg
            << "\n    m_nRequestID: " << data->m_nRequestID
            << "\n    m_nOrderID: " << data->m_nOrderID
            << endl;
    }

    ///获得主推的撤销信息
    void Callback::onRtnCancelError(const CCancelError* data)
    {
        if (data == NULL)
        {
            return;
        }
        cout << "[" << __FUNCTION__ << "]"
            << "\n      OrderId: " << data->m_nOrderID 
            << "\n      ErrorId: " << data->m_nErrorID 
            << "\n      ErrorMsg: " << data->m_strErrorMsg
            << endl;
    }

    void Callback::onRtnAccountDetail(const char* accountId, const CAccountDetail* accountDetail)
    {
        //cout << "[" << __FUNCTION__ << "] accountId: " << accountId << endl;
    }

    void Callback::onRtnCreditAccountDetail(const char* accountId, const CCreditAccountDetail* data)
    {

    }

    void Callback::onRtnNetValue(const CNetValue* data)
    {
        //cout << "[onRtnNetValue] productId: " << data->m_nProductId
        //<< "\n    产品类型: " << data->m_nTypes // 产品类型 1-普通基金 2-分级基金
        //<< "\n    产品净值: " << data->m_dTotalNetValue  //产品净资产, 产品净值
        //<< "\n    母基金单位净值: " << data->m_dNetValue 
        //<< "\n    B级基金单位净值:" << data->m_dBNetValue
        //<< "\n    更新时间：      " << data->m_nUpdateTime
        //<< endl;
    }


    void Callback::onCustomTimer()
    {
        cout << "[" << __FUNCTION__ << "]"
            << endl;
    }

}
