/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   XtTraderNetApi.h
      author:     jianxin
      purpose:    C#使用CLR接口 函数声明
      WARNING:    the code is machine generated, do not modify
*********************************************************************/
#ifndef _Included_XtTraderNetApi
#define _Included_XtTraderNetApi
#include "XtTraderApi/XtTraderApi.h"
#include "XtTraderNetApi/XtNetStructs.h"
#include "XtTraderNetApi/XtNetDataType.h"
#include "XtTraderNetApi/XtTraderNetApiCallback.h"

using namespace System;

namespace NetApi{
    public ref class XtTraderApi
    {
    public:
        virtual ~XtTraderApi(){};
        static XtTraderApi^ createXtTraderApi(String^ address);
        void setCallback(NetApi::XtTraderApiCallback^ pCallback);
        bool init(String^ configFilePath);
        void destroy();
        void join();
        void join_async();
        static void joinAll();
        static void destroyAll();
        void joinAll_async();
        int reqProductIdByAccountKey(String^ accountKey);
        void userLogin(String^ userName, String^ password, int nRequestId ,String^ machineInfo,String^ appid,String^ authcod);
        void userLogout(String^ userName, String^ password, int nRequestId);
        void reqAccountDetail(String^ accountID, int nRequestId,String^ accountKey);
        void reqOrderDetail(String^ accountID, int nRequestId,String^ accountKey);
        void reqOrderDetail(String^ accountID, int nRequestId, int nOrderID,String^ accountKey);
        void reqDealDetail(String^ accountID, int nRequestId,String^ accountKey);
        void reqDealDetail(String^ accountID, int nRequestId, int nOrderID,String^ accountKey);
        void reqPositionDetail(String^ accountID, int nRequestId,String^ accountKey);
        void reqPositionStatics(String^ accountID, int nRequestId,String^ accountKey);
        void reqStkcompacts(String^ accountID, int nRequestId,String^ accountKey);
        void reqCoveredStockPosition(String^ accountID, int nRequestId,String^ accountKey);
        void reqStkOptCombPositionDetail(String^ accountID, int nRequestId,String^ accountKey);
        void reqAccountDetail(String^ accountID, int nRequestId);
        void reqOrderDetail(String^ accountID, int nRequestId);
        void reqOrderDetail(String^ accountID, int nRequestId, int nOrderID);
        void reqDealDetail(String^ accountID, int nRequestId);
        void reqDealDetail(String^ accountID, int nRequestId, int nOrderID);
        void reqPositionDetail(String^ accountID, int nRequestId);
        void reqPositionStatics(String^ accountID, int nRequestId);
        void reqStkcompacts(String^ accountID, int nRequestId);
        void reqCoveredStockPosition(String^ accountID, int nRequestId);
        void reqStkOptCombPositionDetail(String^ accountID, int nRequestId);
        void reqPriceData(String^ exchangeId, String^ instrumentId, int nRequestId);
        void reqPriceDataByMarket(String^ exchangeId, int nRequestId);
        void reqInstrumentInfoByMarket(String^ exchangeId, int nRequestId);
        void reqInstrumentDetail(String^ accountID, int nRequestId,String^ accountKey);
        void order(NetApi::COrdinaryOrder^ orderInfo, int nRequestId,String^ accountKey);
        void order(NetApi::CGroupOrder^ orderInfo, int nRequestId,String^ accountKey);
        void order(NetApi::CAlgorithmOrder^ orderInfo, int nRequestId,String^ accountKey);
        void order(NetApi::COrdinaryGroupOrder^ orderInfo, int nRequestId,String^ accountKey);
        void reqInstrumentDetail(String^ accountID, int nRequestId);
        void order(NetApi::COrdinaryOrder^ orderInfo, int nRequestId);
        void directOrder(NetApi::COrdinaryOrder^ orderInfo, int nRequestId);
        void order(NetApi::CGroupOrder^ orderInfo, int nRequestId);
        void order(NetApi::CAlgorithmOrder^ orderInfo, int nRequestId);
        void order(NetApi::COrdinaryGroupOrder^ orderInfo, int nRequestId);
        void order(NetApi::CIntelligentAlgorithmOrder^ orderInfo, int nRequestId, String^ accountKey);
        void order(NetApi::CExternAlgorithmOrder^ orderInfo, int nRequestId, String^ accountKey);
        void order(NetApi::CHuaChuangAlgorithmOrder^ orderInfo, int nRequestId, String^ accountKey);
        void order(NetApi::CHuaChuangAlgoGroupOrder^ orderInfo, int nRequestId, String^ accountKey);
        void order(NetApi::CAlgGroupOrder^ orderInfo, int nRequestId, String^ accountKey);
        void order(NetApi::CExternAlgGroupOrder^ orderInfo, int nRequestId, String^ accountKey);
        void cancel(int orderID, int nRequestId);
        void cancelOrder(String^ accountID, String^ orderSyeId, String^ exchangeId, String^ instrumentId, int nRequestId);
        void cancelOrder(String^ accountID, String^ orderSyeId, String^ exchangeId, String^ instrumentId, int nRequestId, String^ accountKey);
        void registerUserSystemInfo(String^ accountID, String^ IpPortAddr, int len, String^ CTPSystemInfo, int nRequestId, String^ accountKey);
        void startTimer(int millsec);
        void stopTimer();
        void subscribQuote(NetApi::CSubscribData^ data, int nRequestId);
        void unSubscribQuote(NetApi::CSubscribData^ data, int nRequestId);
        void setCmdFrzCheckOption(int nCmdFrzCheckOption);
        void reqGGTReferenceRate(String^ accountID, int nRequestId,String^ accountKey);
        void reqCreditDetail(String^ accountID, int nRequestId,String^ accountKey);
        void operateTask(NetApi::CTaskOpRecord^ op, String^ accountID, int nRequestId, String^ accountKey);
        void modifyAlgoCommands(NetApi::CAlgorithmOrder^ orderInfo, int nOrderID, int nRequestId, String^ accountKey);
        void enableOrderStat(bool flag);
        void enableCmdCancelOrder();
        void reqSubscribeInfo(String^ accountID, int nRequestId,String^ accountKey);
        void reqStkUnCloseCompacts(String^ accountID, int nRequestId,String^ accountKey);
        void reqStkClosedCompacts(String^ accountID, int nRequestId,String^ accountKey);
        void reqOrderDetailNew(String^ accountID, int nRequestId,String^ accountKey);
        void reqDealDetailNew(String^ accountID, int nRequestId,String^ accountKey);
        void reqAccountKeys(int nRequestId);
        void reqDealDetailBySysID(String^ accountID, int nRequestId, String^ orderSyeId, String^ exchangeId, String^ accountKey);
        void reqDeliveryDetail(String^ accountID, String^ startDate, String^ endDate, int nRequestId, String^ accountKey);
        void reqSingleInstrumentInfo(String^ exchangeId, String^ instrumentId, int nRequestId);
        void reqOpVolume(NetApi::COpVolumeReq^ opVolumeReq, int nRequestId, String^ accountKey);
        void reqCreditSloCode(String^ accountID, int nRequestId, String^ accountKey);
        void reqCreditSubjects(String^ accountID, int nRequestId, String^ accountKey);
        void reqCreditAssure(String^ accountID, int nRequestId, String^ accountKey);
        void reqTransferBank(String^ accountID, int nRequestId, String^ accountKey);
        void reqTransferSerial(String^ accountID, String^ startDate, String^ endDate, int nRequestId, String^ accountKey);
        void reqBankAmount(NetApi::CQueryBankInfo^ bankInfo, int nRequestId, String^ accountKey);
        void transfer(NetApi::CTransferReq^ transferReq, int nRequestId, String^ accountKey);
        void reqCanCancelOrderDetail(String^ accountID, int nRequestId, String^ accountKey);
        void reqCommandsInfo(int nRequestId);
        void fundTransfer(NetApi::CSecuFundTransferReq^ fundTransferReq, int nRequestId, String^ accountKey);
        void secuTransfer(NetApi::CSecuFundTransferReq^ secuTransferReq, int nRequestId, String^ accountKey);
        void reqComFund(String^ accountID, int nRequestId, String^ accountKey);
        void reqComPosition(String^ accountID, int nRequestId, String^ accountKey);
        void reqTradeDay(int nRequestId);
        void reqHistoryOrderDetail(String^ accountID, String^ startDate, String^ endDate, int nRequestId, String^ accountKey);
        void reqHistoryDealDetail(String^ accountID, String^ startDate, String^ endDate, int nRequestId, String^ accountKey);
        void reqHistoryPositionStatics(String^ accountID, String^ startDate, String^ endDate, int nRequestId, String^ accountKey);
        void reqFtAccCommissionRateDetail(String^ accountID, String^ exchangeId, String^ instrumentId, int nRequestId, String^ accountKey);
        void reqFtAccMarginRateDetail(String^ accountID, String^ exchangeId, String^ instrumentId, int nRequestId, String^ accountKey);
        void reqProductIds(int nRequestId);
        void createPortfolio(NetApi::CNewPortfolioReq^ newPortfolioReq, int nRequestId);
        void reqProductPortfolio(int nProductID, int nRequestId);
        void reqPortfolioOrder(int nPortfolioID, int nDate, int nRequestId);
        void reqPortfolioMultiOrder(int nPortfolioID, int nFromDate, int nToDate, int nRequestId);
        void reqPortfolioDeal(int nPortfolioID, int nDate, int nRequestId);
        void reqPortfolioMultiDeal(int nPortfolioID, int nFromDate, int nToDate, int nRequestId);
        void reqPortfolioPosition(int nPortfolioID, int nDate, int nRequestId);
        void reqStrategyInfo(String^ accountID, int nRequestId, String^ accountKey);
        void reqSecuAccount(String^ accountID, int nRequestId, String^ accountKey);

    private:
        xti::XtTraderApi * m_traderApi;
        xti::XtTraderApiCallback * m_traderApiCallback;
    };
}
#endif
