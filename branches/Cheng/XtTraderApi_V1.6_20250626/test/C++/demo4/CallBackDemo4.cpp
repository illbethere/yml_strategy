#include "time.h"
#include <demo4/CallBackDemo4.h>

namespace demo4
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
        m_client->cancel(60, genRequestId()); // 要正确撤指令，orderID必须存在
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

    void Callback::onCancel(int nRequestId, const XtError& error)
    {
        cout << "[onCancel] success:  " << (error.isSuccess() ? "true" : error.errorMsg()) << ", requestID: " << nRequestId << endl;
    }
}
