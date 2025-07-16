#ifndef API_CALL_BACK_H_
#define API_CALL_BACK_H_

#include <iostream>
#include <string>
#include <XtDataType.h>
#include <XtTraderApi.h>

using namespace xti;
using namespace std;

namespace demo7
{
    /**
    账号类型
    */
    enum AccoutType
    {
        CB_AT_DEFAULT,
        CB_AT_FUTURE = 1,          //期货账号
        CB_AT_STOCK = 2,           //股票账号
        CB_AT_CREDIT = 3,          //信用账号
        CB_AT_STOCK_OPTION = 6,    //股票期权账号
    };

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

        /** 
        @brief创建api实例，并进行初始化
        */
        int init();
        // 等待线程结束（需要客户主动结束程序）
        void join();

        /**
        * @brief 启动XtTraderApi多实例线程, 多实例情况下必须使用该函数, 同时单实例也可调用该函数
        * @note 需要调用该函数阻塞线程，否则没有请求XtTraderApi实例会退出
        */
        void joinAll();

        void doRequest();
        std::string getAccountKey(const char* accountId, EXTBrokerType brokerType);
        std::string getAccountTypeDesc(int brokerType);
        std::string getAccountStatusDesc(int status);
        long long genRequestId();

        // 普通单测试
        // @param   fundAccountType 资金账号类型，支持现货、期货、期权、etf、信用等
        // @param   accountId 资金账号
        // @param   times 报单次数
        void testOrdinaryOrder(AccoutType fundAccountType, const std::string& accountId,  int times = 1);
        void testFutureOrdinaryOrder(const std::string& accountId,  int times);
        void testFutureOrdinaryOrder(const std::string& accountId, const std::string& accountKey, int times);
        void testFutureOrdinaryGroupOrder(const string& accountId, string accountKey = "");
        void testStockOrdinaryOrder(const std::string& accountId,  int times, std::string accountKey = "");
        void testStockOrdinaryGroupOrder(const string& accountId, string accountKey= "");
        void testHGTOrdinaryOrder(const string& accountId, int times, string accountKey= "");
        void testSGTOrdinaryOrder(const string& accountId, int times, string accountKey= "");
        void testCreditOrdinaryOrder(const std::string& accountId,  int times);
        void testStockOptionOrdinaryOrder(const std::string& accountId,  int times);
        void testStockOptionOrdinaryOrder(const std::string& accountId, const std::string& accountKey, int times);
        void testFutureOptionOrdinaryOrder(const std::string& accountId,  int times);
        void testFutureOptionOrdinaryOrder(const std::string& accountId, const std::string& accountKey,  int times);


        void testReqAccountKeySync();
        void testReqAccountDetailSyncWithProductId();
        void testReqDealDetailSyncWithProductId();
        void testReqDealStaticsSyncWithProductId();
        void testReqHistoryDealDetailSyncWithProductID();
        void testReqHistoryDealStaticsSyncWithProductID();
        void testReqHistoryPositionStaticsSyncWithProductID();

        void testReqProductData();
        void testReqProductDataSync();
        // 算法单测试
        // @param   fundAccountType 资金账号类型，支持现货、期货、期权、etf、信用等
        // @param   accountId 资金账号
        void testAlgorithmOrder(AccoutType fundAccountType, const std::string& accoundId);

        // 三方算法单测试
        // @param   accountId 资金账号
        void testExternAlgorithmOrder(const std::string& accoundId);

        // 组合单测试
        // @param   accountId 资金账号
        //@remark  目前组合单只支持股票业务
        void testGroupOrder(const std::string& accoundId);

        void testAlgoGroupOrder(const std::string& accoundId, const std::string& accountKey);

        //随机量下单测试
        // @param   accountId 资金账号
        //@remark  目前随机量下单只支持股票业务
        void testRandomOrder(const std::string& accountId);

        //智能算法下单测试
        //@param   accountId 资金账号
        void testIntelligentAlgorithmOrder(const std::string& accountId, const std::string& accountKey);

        // 撤委托
        void testCancelSync(int orderID, const char* accountKey);
        void testCancelOrder(AccoutType fundAccountType, const char* accountId);

        //风险试算测试
        void checkOrdinaryOrder(const std::string& accountId);

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

        // 三种报单方式的回调
        // @param   nRequestId 客户自己维护的请求号
        // @param   orderID 服务器反馈的指令号，成功为大于0的整数，失败统一为-1
        // @param   strRemark 下单时填写的投资备注
        // @param   error 反馈报单信息，error的isSuccess可判断是否报单成功
        virtual void onOrder(int nRequestId, int orderID, const char* strRemark, const XtError& error);

        /**
        * @brief 直接下单的回调函数
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] strOrderSysID 委托号
        * @param[out] strRemark 下单时填写的投资备注
        * @param[out] error 错误信息
        * @attention 当error返回报错时，error.errorMsg()包含下单失败原因
        */
        virtual void onDirectOrder(int nRequestId, const char* strOrderSysID, const char* strRemark, const XtError& error);

        // 撤单方式的回调
        // @param   nRequestId 客户自己维护的请求号
        // @param   error 反馈报单信息，error的isSuccess可判断是否报单成功
        virtual void onCancel(int nRequestId, const XtError& error);

        // 撤单方式的回调
        // @param   nRequestId 客户自己维护的请求号
        // @param   error 反馈报单信息，error的isSuccess可判断是否报单成功
        virtual void onCancelOrder(int nRequestId, const XtError& error);

        // 风险试算的回调
        // @param   nRequestId 客户自己维护的请求号
        // @param   error 反馈报单信息，error的isSuccess可判断是否报单成功
        virtual void onCheck(int nRequestId ,const CCheckData* checkData , const XtError& error);

        // 用户退出登录的回调，暂时无用
        virtual void onUserLogout(const std::string& userName, const std::string& password, int nRequestId, const XtError& error); 


        // 查询资金账号的各个记录信息

        // 查询资金账号的信息
        // @param   accountId 资金账户
        // @param   nRequestId 客户自己维护的请求号
        // @param   data 资金账号的具体信息，具体可参考XtStructs.h
        // @param   isLast 是否为返回最后一条记录，一次请求的结果一般只有一条资金账号信息
        // @param   error 反馈这次查询请求是否有错误
        virtual void onReqAccountDetail(const char* accountId, int nRequestId, const CAccountDetail* data, bool isLast, const XtError& error);

        /**
        * @brief 请求账号资金的回调函数
        * @param[out] accountID 账号ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 账号资金数据, 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqAccountDetail(const char* accountID, int nRequestId, std::vector<CAccountDetail>* data, bool isLast, const XtError& error);


        // 查询信用资金账号的信息，当资金账号是信用类型的时候，请求资金账号会返回两条数据
        // @param   accountId 资金账户
        // @param   nRequestId 客户自己维护的请求号
        // @param   data 信用的资金账号的具体信息，具体可参考XtStructs.h
        // @param   isLast 是否为返回最后一条记录，一次请求的结果一般只有一条资金账号信息，其余类型的账号无返回
        // @param   error 反馈这次查询请求是否有错误
        virtual void onReqCreditAccountDetail(const char* accountId, int nRequestId, const CCreditAccountDetail* data, bool isLast, const XtError& error);

        // 查询信用资金账号的信息，当资金账号是信用类型的时候，请求资金账号会返回两条数据
        // @param   accountId 资金账户
        // @param   nRequestId 客户自己维护的请求号
        // @param   data 信用的资金账号的具体信息，具体可参考XtStructs.h
        // @param   isLast 是否为返回最后一条记录，一次请求的结果一般只有一条资金账号信息，其余类型的账号无返回
        // @param   error 反馈这次查询请求是否有错误
        virtual void onBatchReqCreditAccountDetail(const char* accountId, int nRequestId, std::vector<CCreditAccountDetail>* data, bool isLast, const XtError& error);

        // 委托记录明细的回调
        // @param   accountId 资金账户
        // @param   nRequestId 客户自己维护的请求号
        // @param   data 委托记录具体信息，具体可参考XtStructs.h
        // @param   isLast 是否为返回最后一条记录，一次请求当日委托的结果可能有多条记录
        // @param   error 反馈这次查询请求是否有错误
        virtual void onReqOrderDetail(const char* accountId, int nRequestId, const COrderDetail* data, bool isLast, const XtError& error);

        /**
        * @brief 请求账号委托明细的回调函数
        * @param[out] accountID 账号ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 账号委托明细数据，数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqOrderDetail(const char* accountID, int nRequestId, std::vector<COrderDetail>* data, bool isLast, const XtError& error);

        // 成交记录明细的回调
        // @param   accountId 资金账户
        // @param   nRequestId 客户自己维护的请求号
        // @param   data 成交记录的具体信息，具体可参考XtStructs.h
        // @param   isLast 是否为返回最后一条记录，一次请求当日成交的结果可能有多条记录
        // @param   error 反馈这次查询请求是否有错误
        virtual void onReqDealDetail(const char* accountId, int nRequestId, const CDealDetail* data, bool isLast, const XtError& error);

        /**
        * @brief 请求账号成交明细的回调函数
        * @param[out] accountID 账号ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 账号成交明细数据 ，数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqDealDetail(const char* accountID, int nRequestId, std::vector<CDealDetail>* data, bool isLast, const XtError& error);

        // 持仓明细的回调
        // @param   accountId 资金账户
        // @param   nRequestId 客户自己维护的请求号
        // @param   data 持仓明细的具体信息，具体可参考XtStructs.h
        // @param   isLast 是否为返回最后一条记录，一次请求当日持仓明细的结果可能有多条记录
        // @param   error 反馈这次查询请求是否有错误
        virtual void onReqPositionDetail(const char* accountId, int nRequestId, const CPositionDetail* data, bool isLast, const XtError& error);

        /**
       * @brief 请求账号持仓明细的回调函数
       * @param[out] accountID 账号ID
       * @param[out] nRequestId 客户自己维护的请求顺序ID
       * @param[out] data 账号持仓明细数据，数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
       * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
       * @param[out] error 错误信息
       * @attention 当error返回报错时，data内容不可用
       */
        virtual void onBatchReqPositionDetail(const char* accountID, int nRequestId, std::vector <CPositionDetail>* data, bool isLast, const XtError& error);


        // 持仓统计的回调
        // @param   accountId 资金账户
        // @param   nRequestId 客户自己维护的请求号
        // @param   data 持仓统计的具体信息，具体可参考XtStructs.h
        // @param   isLast 是否为返回最后一条记录，一次请求当日持仓统计的结果可能有多条记录。持仓统计一般比持仓明细的记录数要少。
        // @param   error 反馈这次查询请求是否有错误
        virtual void onReqPositionStatics(const char* accountId, int nRequestId, const CPositionStatics* data, bool isLast, const XtError& error);

        /**
        * @brief 请求账号持仓统计的回调函数
        * @param[out] accountID 账号ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 账号持仓统计数据，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqPositionStatics(const char* accountID, int nRequestId, std::vector<CPositionStatics>* data, bool isLast, const XtError& error) ;

        // 信用业务
        // 信用负债合约的回调
        // @param   accountId 资金账户
        // @param   nRequestId 客户自己维护的请求号
        // @param   data 信用负债合约的具体信息，具体可参考XtStructs.h
        // @param   isLast 是否为返回最后一条记录，一次请求负债合约的结果可能有多条记录
        // @param   error 反馈这次查询请求是否有错误
        virtual void onReqStksubjects(const char* accountId, int nRequestId, const CStkSubjects* data, bool isLast, const XtError& error);

        /**
        * @brief 请求两融账号标的的回调函数
        * @param[out] accountID 账号ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 两融账号标的数据，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqStksubjects(const char* accountID, int nRequestId, std::vector<CStkSubjects>* data, bool isLast, const XtError& error) ;

        // 信用标的的回调
        // @param   accountId 资金账户
        // @param   nRequestId 客户自己维护的请求号
        // @param   data 信用标的的具体信息，具体可参考XtStructs.h
        // @param   isLast 是否为返回最后一条记录，一次请求信用标的的结果可能有多条记录
        // @param   error 反馈这次查询请求是否有错误
        virtual void onReqStkcompacts(const char* accountId, int nRequestId, const CStkCompacts* data, bool isLast, const XtError& error);

        /**
        * @brief 请求两融账号负债的回调函数
        * @param[out] accountID 账号ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 两融账号负债数据，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqStkcompacts(const char* accountID, int nRequestId, std::vector<CStkCompacts>* data, bool isLast, const XtError& error) ;

        // 股票期权的备兑持仓的回调
        // @param   accountId 资金账户
        // @param   nRequestId 客户自己维护的请求号
        // @param   data 备兑持仓的具体信息，具体可参考XtStructs.h
        // @param   isLast 是否为返回最后一条记录，一次请求备兑持仓的结果可能有多条记录
        // @param   error 反馈这次查询请求是否有错误
        virtual void onReqCoveredStockPosition(const char* accountId, int nRequestId, const CCoveredStockPosition* data, bool isLast, const XtError& error);
        /**
        * @brief 请求期权账号备兑持仓的回调函数
        * @param[out] accountID 账号ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 期权账号备兑持仓数据，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqCoveredStockPosition(const char* accountID, int nRequestId, std::vector<CCoveredStockPosition>* data, bool isLast, const XtError& error) ;

        // 查询港股汇率
        virtual void onReqReferenceRate(const char* accountId, int nRequestId, const CReferenceRate* data, bool isLast, const XtError& error);

        /**
       * @brief 请求港股账号汇率数据的回调函数
       * @param[out] accountID 账号ID
       * @param[out] nRequestId 客户自己维护的请求顺序ID
       * @param[out] data 港股账号汇率数据，一次最大返回设置返回条数，数据超过设置数量多次返回
       * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
       * @param[out] error 错误信息
       * @attention 当error返回报错时，data内容不可用
       */
        virtual void onBatchReqReferenceRate(const char* accountID, int nRequestId, std::vector<CReferenceRate>* data, bool isLast, const XtError& error) ;

        //两融综合资金
        virtual void onReqCreditDetail(const char* accountId, int nRequestId, const CCreditDetail* data, bool isLast, const XtError& error);
        
        /**
       * @brief 请求两融账号两融综合资金数据的回调函数
       * @param[out] accountID 账号ID
       * @param[out] nRequestId 客户自己维护的请求顺序ID
       * @param[out] data 两融账号两融综合资金数据，一次最大返回设置返回条数，数据超过设置数量多次返回
       * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
       * @param[out] error 错误信息
       * @attention 当error返回报错时，data内容不可用
       */
        virtual void onBatchReqCreditDetail(const char* accountID, int nRequestId, std::vector<CCreditDetail>* data, bool isLast, const XtError& error) ;

        /**
        * @brief 请求新股额度数据的回调函数
        * @param[out] accountID 账号ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 新股信息数据, 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqSubscribeInfo(const char* accountID, int nRequestId, std::vector<CSubscribeInfo>* data, bool isLast, const XtError& error) ;

        /**
        * @brief 请求未了结负债信息的回调函数
        * @param[out] accountID 账号ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 未了结负债信息数据, 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqStkUnCloseCompact(const char* accountID, int nRequestId, std::vector<CStkUnClosedCompacts>* data, bool isLast, const XtError& error) ;

       /**
       * @brief 请求已了结负债信息的回调函数
       * @param[out] accountID 账号ID
       * @param[out] nRequestId 客户自己维护的请求顺序ID
       * @param[out] data 已了结负债信息数据 , 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
       * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
       * @param[out] error 错误信息
       * @attention 当error返回报错时，data内容不可用
       */
        virtual void onBatchReqStkClosedCompact(const char* accountID, int nRequestId, std::vector<CStkClosedCompacts>* data, bool isLast, const XtError& error) ;

        /**
       * @brief 获取用户下所有账号key的回调函数
       * @param[out] nRequestId 客户自己维护的请求顺序ID
       * @param[out] data 已了结负债信息数据 , 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
       * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
       * @param[out] error 错误信息
       * @attention 当error返回报错时，data内容不可用
       */
        virtual void onBatchReqAccountKey(int nRequestId, std::vector<CAccountKey>* data, bool isLast, const XtError& error) ;

        /**
        * @brief 根据委托号请求账号成交明细信息的回调函数
        * @param[out] accountID 账号ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] orderSyeId 委托号
        * @param[out] exchangeId 委托所属市场
        * @param[out] data 账号成交明细数据, 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqDealDetailBySysID(const char* accountID, int nRequestId, const char* orderSyeId, const char* exchangeId, std::vector<CDealDetail>* data, bool isLast, const XtError& error) ;

        /**
        * @brief 请求账号结算单信息的回调函数
        * @param[out] accountID 账号ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 账号结算单数据, 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqDeliveryDetail(const char* accountID, int nRequestId, std::vector<CDeliveryDetail>* data, bool isLast, const XtError& error) ;

        /**
        * @brief 请求两融账号融券可融数量的回调函数
        * @param[out] accountID 账号ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 融券可融数量数据, 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqCreditSloCode(const char* accountID, int nRequestId, std::vector<CCreditSloCode>* data, bool isLast, const XtError& error) ;

        /**
       * @brief 请求两融账号融资融券标的的回调函数
       * @param[out] accountID 账号ID
       * @param[out] nRequestId 客户自己维护的请求顺序ID
       * @param[out] data 融资融券标的数据, 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
       * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
       * @param[out] error 错误信息
       * @attention 当error返回报错时，data内容不可用
       */
        virtual void onBatchReqCreditSubjects(const char* accountID, int nRequestId, std::vector<CCreditSubjects>* data, bool isLast, const XtError& error) ;

        /**
        * @brief 请求两融账号担保标的的回调函数
        * @param[out] accountID 账号ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 担保标的数据, 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqCreditAssure(const char* accountID, int nRequestId, std::vector<CCreditAssure>* data, bool isLast, const XtError& error) ;

        /**
        * @brief 请求账号银证转账银行信息的回调函数
        * @param[out] accountID 账号ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 账号银证转账银行信息数据, 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqTransferBank(const char* accountID, int nRequestId, std::vector<CQueryBankInfo>* data, bool isLast, const XtError& error) ;

        /**
        * @brief 请求账号银证转账银行流水的回调函数
        * @param[out] accountID 账号ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 账号银证转账银行流水数据, 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqTransferSerial(const char* accountID, int nRequestId, std::vector<CTransferSerial>* data, bool isLast, const XtError& error) ;

        /**
        * @brief 按市场请求合约信息的回调函数
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 合约信息数据 , 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqInstrumentInfoByMarket(int nRequestId, std::vector<CInstrumentInfo>* data, bool isLast, const XtError& error) ;

        /**
        * @brief 请求账号可撤单委托明细的回调函数
        * @param[out] accountID 账号ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 账号委托明细数据, 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqCanCancelOrderDetail(const char* accountID, int nRequestId, std::vector<COrderDetail>* data, bool isLast, const XtError& error) ;

        /**
        * @brief 请求所有下单信息的回调函数
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 下单信息数据, 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqCommandsInfo(int nRequestId, std::vector<COrderInfo>* data, bool isLast, const XtError& error) ;

        /**
        * @brief 请求账号账号普通柜台资金的回调函数
        * @param[out] accountID 账号ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 账号资金划拨普通柜台资金数据 , 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqComFund(const char* accountID, int nRequestId, std::vector<CStockComFund>* data, bool isLast, const XtError& error) ;

        /**
        * @brief 请求账号普通柜台持仓的回调函数
        * @param[out] accountID 账号ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 账号股份划拨普通柜台持仓数据, 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqComPosition(const char* accountID, int nRequestId, std::vector<CStockComPosition>* data, bool isLast, const XtError& error) ;

        /**
        * @brief 请求账号历史委托明细的回调函数
        * @param[out] accountID 账号ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 账号委托明细数据, 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqHistoryOrderDetail(const char* accountID, int nRequestId, std::vector<COrderDetail>* data, bool isLast, const XtError& error) ;

        /**
        * @brief 请求账号历史成交明细的回调函数
        * @param[out] accountID 账号ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 账号成交明细数据, 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqHistoryDealDetail(const char* accountID, int nRequestId, std::vector<CDealDetail>* data, bool isLast, const XtError& error) ;

        /**
       * @brief 请求账号历史持仓统计的回调函数
       * @param[out] accountID 账号ID
       * @param[out] nRequestId 客户自己维护的请求顺序ID
       * @param[out] data 账号持仓统计数据 , 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
       * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
       * @param[out] error 错误信息
       * @attention 当error返回报错时，data内容不可用
       */
        virtual void onBatchReqHistoryPositionStatics(const char* accountID, int nRequestId, std::vector<CPositionStatics>* data, bool isLast, const XtError& error) ;

        /**
       * @brief 查询产品Id下所有的投资组合的回调函数
       * @param[out] nProductID 产品ID
       * @param[out] nRequestId 客户自己维护的请求顺序ID
       * @param[out] data 投资组合数据, 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
       * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
       * @param[out] error 错误信息
       * @attention 当error返回报错时，data内容不可用
       */
        virtual void onBatchReqProductPortfolio(int nProductID, int nRequestId, std::vector<CPortfolioInfo>* data, bool isLast, const XtError& error) ;
        /**
        * @brief 请求投资组合委托信息的回调函数
        * @param[out] nPortfolioID 投资组合ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 账号委托明细数据, 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqPortfolioOrder(int nPortfolioID, int nRequestId, std::vector<COrderDetail>* data, bool isLast, const XtError& error) ;
        /**
       * @brief 请求投资组合一段时间内的委托信息的回调函数
       * @param[out] nPortfolioID 投资组合ID
       * @param[out] nRequestId 客户自己维护的请求顺序ID
       * @param[out] data 账号委托明细数据, 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
       * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
       * @param[out] error 错误信息
       * @attention 当error返回报错时，data内容不可用
       */
        virtual void onBatchReqPortfolioMultiOrder(int nPortfolioID, int nRequestId, std::vector<COrderDetail>* data, bool isLast, const XtError& error) ;
        /**
       * @brief 请求账号成交明细的回调函数
       * @param[out] nPortfolioID 投资组合ID
       * @param[out] nRequestId 客户自己维护的请求顺序ID
       * @param[out] data 账号成交明细数据, 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
       * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
       * @param[out] error 错误信息
       * @attention 当error返回报错时，data内容不可用
       */
        virtual void onBatchReqPortfolioDeal(int nPortfolioID, int nRequestId, std::vector<CDealDetail>* data, bool isLast, const XtError& error) ;

        /**
        * @brief 请求投资组合一段时间内的成交信息的回调函数
        * @param[out] nPortfolioID 投资组合ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 账号成交明细数据, 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqPortfolioMultiDeal(int nPortfolioID, int nRequestId, std::vector<CDealDetail>* data, bool isLast, const XtError& error) ;

        /**
        * @brief 请求投资组合持仓信息的回调函数
        * @param[out] nPortfolioID 投资组合ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 账号持仓统计数据, 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqPortfolioPosition(int nPortfolioID, int nRequestId, std::vector<CPositionStatics>* data, bool isLast, const XtError& error) ;

        /**
       * @brief 请求收益互换账号框架号的回调函数
       * @param[out] accountID 账号ID
       * @param[out] nRequestId 客户自己维护的请求顺序ID
       * @param[out] accountKey 账号key
       * @param[out] data 收益互换账号框架号数据, 数据可能有多条，一次最大返回设置返回条数，数据超过设置数量多次返回
       * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
       * @param[out] error 错误信息
       * @attention 当error返回报错时，data内容不可用
       */
        virtual void onBatchReqStrategyInfo(const char* accountID, int nRequestId, const char* accountKey, std::vector<CStrategyInfo>* data, bool isLast, const XtError& error) ;

        /**
        * @brief 请求股东号的回调函数
        * @param[out] accountID 账号ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] accountKey 账号key
        * @param[out] data 股东号数据
        * @param[out] isLast 请求数据可能有多条，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqSecuAccount(const char* accountID, int nRequestId, const char* accountKey, std::vector<CSecuAccount>* data, bool isLast, const XtError& error) ;

        // 查询产品
        virtual void onReqProductData(int nRequestId, const CProductData* data, bool isLast, const XtError& error);

        /**
        * @brief 请求产品信息的回调函数
        * @param[out] accountID 账号ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 产品信息数据，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqProductData(int nRequestId, std::vector<CProductData>* data, bool isLast, const XtError& error) ;

        // 期权组合持仓
       virtual void onReqStkOptCombPositionDetail(const char* accountId, int nRequestId, const CStockOptionCombPositionDetail* data, bool isLast, const XtError& error);

       /**
        * @brief 请求期权账号组合持仓数据的回调函数
        * @param[out] accountID 账号ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 期权账号组合持仓数据，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
       virtual void onBatchReqStkOptCombPositionDetail(const char* accountID, int nRequestId, std::vector<CStockOptionCombPositionDetail>* data, bool isLast, const XtError& error) ;


        // 请求行情的回调
        // @param   nRequestId 客户自己维护的请求号
        // @param   data 具体的行情信息，具体可参考XtStructs.h
        virtual void onReqPriceData(int nRequestId, const CPriceData* data, const XtError& error);

        // 查询期权行情的回调
        // @param   nRequestId 客户自己维护的请求号
        // @param   datas 具体的行情信息，具体可参考XtStructs.h

        virtual void onReqCInstrumentDetail(const char* accountId, int nRequestId, const CInstrumentDetail* data, bool isLast, const XtError& error);

        /**
        * @brief 请求合约数据的回调函数
        * @param[out] accountID 账号ID
        * @param[out] nRequestId 客户自己维护的请求顺序ID
        * @param[out] data 合约数据，一次最大返回设置返回条数，数据超过设置数量多次返回
        * @param[out] isLast 请求数据可能超过单次最大返回条数，需要多次回调该函数，标记是否是一次请求的最后一次回调
        * @param[out] error 错误信息
        * @attention 当error返回报错时，data内容不可用
        */
        virtual void onBatchReqCInstrumentDetail(const char* accountID, int nRequestId, std::vector<CInstrumentDetail>* data, bool isLast, const XtError& error) ;


        //订阅行情反馈
        virtual void onSubscribQuote(int nRequestId, const CSubscribData* data, const XtError& error);

        //订阅行情反馈
        virtual void onUnSubscribQuote(int nRequestId, const CSubscribData* data, const XtError& error);

        // 行情主推接口
        virtual void onRtnPriceData(const CPriceData& data);

        // 主推的接口
        // 资金账号的主推信息
        // @param   accountId 资金账户
        // @param   status 表明这个资金账号目前在迅投系统的登录状态
        // @param   brokerType 表明这个资金账号的类型，1:期货，2:股票，3:信用，6:股票期权
        // @param   errorMsg 如果有错误，通过errorMsg反馈错误信息
        virtual void onRtnLoginStatus(const char* accountId, EBrokerLoginStatus status, int brokerType, const char* errorMsg);
        virtual void onRtnLoginStatusWithActKey(const char* accountId, EBrokerLoginStatus status, int brokerType, const char* accountKey, const char* errorMsg);

        // 指令状态的主推信息
        // @param   data 具体信息有COrderInfo携带
        virtual void onRtnOrder(const COrderInfo* data);

        // 委托回报的主推信息
        // @param   data COrderDetail
        virtual void onRtnOrderDetail(const COrderDetail* data);

        // 成交回报的主推信息
        // @param   data 具体信息有CDealDetail携带
        virtual void onRtnDealDetail(const CDealDetail* data);

        // 委托错误的主推信息
        // @param   data 具体信息有COrderError携带
        virtual void onRtnOrderError(const COrderError* data);

        // 委托回报的主推信息
        // @param   data 具体信息有CDealDetail携带
        virtual void onRtnCancelError(const CCancelError* data);

        // 资金账号的主推信息
        // @param   accountId 资金账户
        // @param   accountDetail 具体信息有CAccountDetail携带
        virtual void onRtnAccountDetail(const char* accountId, const CAccountDetail* accountDetail);

        // 信用资金账号信息的主推信息
        // @param   accountId 资金账户
        // @param   accountDetail 具体信息有CAccountDetail携带
        virtual void onRtnCreditAccountDetail(const char* accountId, const CCreditAccountDetail* data);

        // 产品净值的主推信息
        // @param   data 具体信息有CNetValue携带
        virtual void onRtnNetValue(const CNetValue* data);

        // 用户自己的定时器回调
        virtual void onCustomTimer();

    private:
        string          m_strStockAccount;   // 股票账号
        string          m_strFutureAccount;  // 期货账号
        string          m_strOptionAccount;  // 股票期权账号
        string          m_strCreditAccount;  // 信用账号
        string          m_strAccountKey;  // 股票账号key
        string          m_strFutureAccountKey;  // 期货账号key
        int             m_nRequestId;        // 请求序号
        std::string     m_strAddress;
        std::string     m_strUserName;
        std::string     m_strPassWord;
        XtTraderApi*    m_client;
        bool            m_blogin;//onUserLogin成功
        bool            m_bloginStatus;//onRtnLoginStatus成功
        bool            m_bDoRequest;

        int             m_nRespCnt;
    };
}
#endif   // API_CALL_BACK_H_
