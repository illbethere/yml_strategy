#ifndef API_CALL_BACK_DEMO2_H_
#define API_CALL_BACK_DEMO2_H_

#include <iostream>
#include <string>
#include <XtDataType.h>
#include <MarketType.h>
#include <XtTraderApi.h>

using namespace xti;
using namespace std;

namespace demo2
{
    /**
    * @brief 交易回调实现
    *
    * 实现XtTraderApiCallback定义的各个接口，可获取查询反馈、委托和成交主推、账号状态等信息
    */
    class Callback : public XtTraderApiCallback
    {
    public:
        Callback(const std::string& address, const std::string& username, const std::string& password);
        ~Callback();

        // 创建api实例，并进行初始化
        int init();
        // 等待线程结束（需要客户主动结束程序）
        void join();

        // 生成请求序号
        long long genRequestId();
        // 资金账号类型描述
        std::string getAccountTypeDesc(int brokerType);
        // 资金账号状态描述
        std::string getAccountStatusDesc(int status);

        // 建立连接的回调
        // @param   success 反馈是否成功与服务器建立连接
        // @param   errorMsg 反馈连接失败时具体的错误信息
        virtual void onConnected(bool success, const char* errorMsg);

        // 用户登录的回馈
        // @param   userName 用户名
        // @param   password 用户对应的密码
        // @param   nRequestId 客户自己维护的请求号
        // @param   error 反馈登录信息，error的isSuccess可判断是否登录成功
        virtual void onUserLogin(const char* userName, const char* password, int nRequestId, const XtError& error);

        // 资金账号的信息
        // @param   accountId 资金账户
        // @param   nRequestId 客户自己维护的请求号
        // @param   data 资金账号的具体信息，具体可参考XtStructs.h
        // @param   isLast 是否为返回最后一条记录，一次请求的结果一般只有一条资金账号信息
        // @param   error 反馈这次查询请求是否有错误
        virtual void onReqAccountDetail(const char* accountId, int nRequestId, const CAccountDetail* data, bool isLast, const XtError& error);

        // 产品信息
        virtual void onReqProductData(int nRequestId, const CProductData* data, bool isLast, const XtError& error);

        // 资金账号的主推信息
        // @param   accountId 资金账户
        // @param   status 表明这个资金账号目前在迅投系统的登录状态
        // @param   brokerType 表明这个资金账号的类型，1:期货，2:股票，3:信用，6:股票期权
        // @param   errorMsg 如果有错误，通过errorMsg反馈错误信息
        virtual void onRtnLoginStatus(const char* accountId, EBrokerLoginStatus status, int brokerType, const char* errorMsg);

    private:
        string          m_strStockAccount;   // 股票账号
        string          m_strFutureAccount;  // 期货账号
        string          m_strOptionAccount;  // 股票期权账号
        string          m_strCreditAccount;  // 信用账号
        int             m_nRequestId;        // 请求序号
        std::string     m_strAddress;
        std::string     m_strUserName;
        std::string     m_strPassWord;
        XtTraderApi*    m_client;
    };
}
#endif   // API_CALL_BACK_H_
