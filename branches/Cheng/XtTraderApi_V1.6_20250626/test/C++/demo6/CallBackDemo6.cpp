#include "time.h"
#include <demo6/CallBackDemo6.h>

namespace demo6
{
    Callback::Callback(const string& address, const string& username, const string& password):
        m_nRequestId(1),
        m_strAddress(address),
        m_strUserName(username),
        m_strPassWord(password),
        m_client(NULL)
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

    void Callback::testStockOrdinaryOrder(const string& accountId)
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
        orderInfo.m_eOperationType = OPT_BUY;

        // 报单价格类型，必填字段。默认为无效(PTRP_INVALID)，具体可参考XtDataType.h
        orderInfo.m_ePriceType = PRTP_MARKET;

        // 报单价格，默认为double最大值。当价格类型m_ePriceType为指定价PRTP_FIX时，必填字段。当价格类型为其他时填了也没用
        orderInfo.m_dPrice = 0;

        // 投机套保标志，选填字段。有"投机"/"套利"/"套保"方式。除期货三个方式都可选之外都是填“投机”。默认为“投机”
        orderInfo.m_eHedgeFlag = HEDGE_FLAG_SPECULATION;

        // 投资备注
        strcpy(orderInfo.m_strRemark, "test004");

        m_client->order(&orderInfo, genRequestId());
    }

    void Callback::onConnected(bool success, const char* errorMsg)
    {
        cout << "[onConnected] server connect " << (success ? string("success") : string("failure, err: ") + errorMsg) << endl;
        if (success)
        {
            m_client->userLogin(m_strUserName.c_str(), m_strPassWord.c_str(), m_nRequestId++);
        }
    }

    void Callback::onUserLogin(const char* userName, const char* password, int nRequestId, const XtError& error)
    {
        cout << "[onUserLogin] login " << (error.isSuccess() ? "success" : string("failure, err: ") + error.errorMsg()) << endl;

        // 设置定时器，每5秒运行一次
        m_client->startTimer(5000);
    }

    void Callback::onRtnLoginStatus(const char* accountId, EBrokerLoginStatus status, int brokerType, const char* errorMsg)
    {
        cout << "[onRtnLoginStatus] account id: " << accountId << ", type: " << getAccountTypeDesc(brokerType) << ", status: " << getAccountStatusDesc(status) << endl;

        switch (brokerType)
        {
        case AT_STOCK:
            m_strStockAccount = accountId;
            break;
        case AT_FUTURE:
            m_strFutureAccount = accountId;
            break;
        case AT_STOCK_OPTION:
            m_strOptionAccount = accountId;
            break;
        case AT_CREDIT:
            m_strCreditAccount = accountId;
            break;
        default:
            break;
        }
    }

    void Callback::onOrder(int nRequestId, int orderId, const char* strRemark, const XtError& error)
    {
        cout << "[onOrder] isSuccess: " << (error.isSuccess() ? "true" : "false")
            << "\n    orderId:  " << orderId
            << "\n    RequestId: " << nRequestId
            << "\n    errorMsg: " << error.errorMsg()
            << endl;
    }

    void Callback::onRtnOrder(const COrderInfo* data)
    {
        string orderStatus = "";
        switch (data->m_eStatus)
        {
        case OCS_CHECKING:   orderStatus = "风控检查中";  break;
        case OCS_APPROVING:  orderStatus = "审批中";  break;
        case OCS_REJECTED:   orderStatus = "已驳回";  break;
        case OCS_RUNNING:    orderStatus = "运行中";  break;
        case OCS_CANCELING:  orderStatus = "撤销中";  break;
        case OCS_FINISHED:   orderStatus = "已完成";  break;
        case OCS_STOPPED:    orderStatus = "已撤销";  break;
        }

        cout << "[onRtnOrder]"
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
        switch (data->m_eOrderStatus)
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
            << "\n    成交均价：" << data->m_dAveragePrice
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
        cout << "[onRtnDealDetail]"
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


    void Callback::onCustomTimer()
    {
        cout << "[onCustomTimer] time up" << endl;
        testStockOrdinaryOrder(m_strStockAccount);
    }

}
