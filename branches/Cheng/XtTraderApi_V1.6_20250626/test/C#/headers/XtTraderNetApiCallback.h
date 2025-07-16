/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   XtTraderNetApiCallback.h
      author:     jianxin
      purpose:    CLR派生Cpp基类，CLR向C#提供基类
*********************************************************************/
#ifndef _Included_XtTraderNetApiCallback
#define _Included_XtTraderNetApiCallback
#include "XtTraderApi/XtTraderApi.h"
#include "XtTraderNetApi/XtNetStructs.h"
#include "XtTraderNetApi/XtNetDataType.h"
#include "XtTraderNetApi/XtNetError.h"
#include "vcclr.h"

using namespace NetApi;
using namespace System;

namespace NetApi{
    ref class XtTraderApi;
    public ref class XtTraderApiCallback abstract
    {
    public:
        XtTraderApiCallback(){};
        virtual ~XtTraderApiCallback(){}

        virtual void onConnected(bool success, String^ errorMsg) {};
        virtual void onUserLogin(String^ userName, String^ password, int nRequestId, XtError^ error) {};
        virtual void onUserLogout(String^ userName, String^ password, int nRequestId, XtError^ error) {};
        virtual void onReqAccountDetail(String^ accountID, int nRequestId, NetApi::CAccountDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqAccountDetailWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::CAccountDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqCreditAccountDetail(String^ accountID, int nRequestId, NetApi::CCreditAccountDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqCreditAccountDetailWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::CCreditAccountDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqOrderDetail(String^ accountID, int nRequestId, NetApi::COrderDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqOrderDetailWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::COrderDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqDealDetail(String^ accountID, int nRequestId, NetApi::CDealDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqDealDetailWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::CDealDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqPositionDetail(String^ accountID, int nRequestId, NetApi::CPositionDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqPositionDetailWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::CPositionDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqPositionStatics(String^ accountID, int nRequestId, NetApi::CPositionStatics^ data, bool isLast, XtError^ error) {};
        virtual void onReqPositionStaticsWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::CPositionStatics^ data, bool isLast, XtError^ error) {};
        virtual void onReqStkcompacts(String^ accountID, int nRequestId, NetApi::CStkCompacts^ data, bool isLast, XtError^ error) {};
        virtual void onReqStkcompactsWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::CStkCompacts^ data, bool isLast, XtError^ error) {};
        virtual void onReqCoveredStockPosition(String^ accountID, int nRequestId, NetApi::CCoveredStockPosition^ data, bool isLast, XtError^ error) {};
        virtual void onReqCoveredStockPositionWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::CCoveredStockPosition^ data, bool isLast, XtError^ error) {};
        virtual void onReqStkOptCombPositionDetail(String^ accountID, int nRequestId, NetApi::CStockOptionCombPositionDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqStkOptCombPositionDetailWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::CStockOptionCombPositionDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqPriceData(int nRequestId, NetApi::CPriceData^ data, XtError^ error) {};
        virtual void onReqCInstrumentDetail(String^ accountID, int nRequestId, NetApi::CInstrumentDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqCInstrumentDetailWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::CInstrumentDetail^ data, bool isLast, XtError^ error) {};
        virtual void onRtnOrder(NetApi::COrderInfo^ data) {};
        virtual void onRtnOrderDetail(NetApi::COrderDetail^ data) {};
        virtual void onRtnDealDetail(NetApi::CDealDetail^ data) {};
        virtual void onRtnOrderError(NetApi::COrderError^ data) {};
        virtual void onRtnCancelError(NetApi::CCancelError^ data) {};
        virtual void onRtnLoginStatus(String^ accountID, NetApi::EBrokerLoginStatus status,int brokerType, String^ errorMsg) {};
        virtual void onRtnDeliveryStatus(String^ accountID, bool status, String^ errorMsg) {};
        virtual void onRtnAccountDetail(String^ accountID, NetApi::CAccountDetail^ data) {};
        virtual void onRtnCreditAccountDetail(String^ accountID, NetApi::CCreditAccountDetail^ data) {};
        virtual void onRtnNetValue(NetApi::CNetValue^ data) {};
        virtual void onOrder(int nRequestId, int orderID, String^ strRemark, XtError^ error) {};
        virtual void onDirectOrder(int nRequestId, String^ strOrderSysID, String^ strRemark, XtError^ error) {};
        virtual void onCancel(int nRequestId, XtError^ error) {};
        virtual void onCancelWithRemark(int nRequestId, String^ strRemark, XtError^ error) {};
        virtual void onCancelOrder(int nRequestId, XtError^ error) {};
        virtual void onCustomTimer() {};
        virtual void onRtnLoginStatusWithActKey(String^ accountID, NetApi::EBrokerLoginStatus status,int brokerType, String^ accountKey, String^ errorMsg) {};
        virtual void onRtnLoginStatusCustom(String^ accountID, NetApi::EBrokerLoginStatus status,int brokerType, String^ accountKey, String^ userName, String^ errorMsg) {};
        virtual void onRtnPriceData(NetApi::CPriceData^ data) {};
        virtual void onSubscribQuote(int nRequestId, NetApi::CSubscribData^ data, XtError^ error) {}
        virtual void onUnSubscribQuote(int nRequestId, NetApi::CSubscribData^ data, XtError^ error) {}
        virtual void onReqReferenceRate(String^ accountID, int nRequestId, NetApi::CReferenceRate^ data, bool isLast, XtError^ error) {};
        virtual void onReqReferenceRateWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::CReferenceRate^ data, bool isLast, XtError^ error) {};
        virtual void onReqCreditDetail(String^ accountID, int nRequestId, NetApi::CCreditDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqCreditDetailWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::CCreditDetail^ data, bool isLast, XtError^ error) {};
        virtual void onOperateTask(String^ accountID, int nRequestId, String^ accountKey, XtError^ error) {};
        virtual void onModifyAlgoCommands(int nRequestId, int orderID, String^ strRemark, XtError^ error) {};
        virtual void onReqSubscribeInfo(String^ accountID, int nRequestId, NetApi::CSubscribeInfo^ data, bool isLast, XtError^ error) {};
        virtual void onReqSubscribeInfoWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::CSubscribeInfo^ data, bool isLast, XtError^ error) {};
        virtual void onReqStkUnCloseCompact(String^ accountID, int nRequestId, NetApi::CStkUnClosedCompacts^ data, bool isLast, XtError^ error) {};
        virtual void onReqStkUnCloseCompactWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::CStkUnClosedCompacts^ data, bool isLast, XtError^ error) {};
        virtual void onReqStkClosedCompact(String^ accountID, int nRequestId, NetApi::CStkClosedCompacts^ data, bool isLast, XtError^ error) {};
        virtual void onReqStkClosedCompactWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::CStkClosedCompacts^ data, bool isLast, XtError^ error) {};
        virtual void onReqAccountKey(int nRequestId, NetApi::CAccountKey^ data, bool isLast, XtError^ error) {};
        virtual void onReqDealDetailBySysID(String^ accountID, int nRequestId, String^ orderSyeId, String^ exchangeId, NetApi::CDealDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqDealDetailBySysIDWithAccKey(String^ accountID, int nRequestId, String^ accountKey, String^ orderSyeId, String^ exchangeId, NetApi::CDealDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqDeliveryDetail(String^ accountID, int nRequestId, NetApi::CDeliveryDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqDeliveryDetailWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::CDeliveryDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqSingleInstrumentInfo(int nRequestId, NetApi::CInstrumentInfo^ data, XtError^ error) {};
        virtual void onRtnExchangeStatus(NetApi::CExchangeStatus^ data) {};
        virtual void onRtnCreditDetail(NetApi::CCreditDetail^ data) {};
        virtual void onReqOpVolume(String^ accountID, int nRequestId, String^ dataKey, int nVolume, bool isLast, XtError^ error) {};
        virtual void onReqOpVolumeWithAccKey(String^ accountID, int nRequestId, String^ accountKey, String^ dataKey, int nVolume, bool isLast, XtError^ error) {};
        virtual void onReqCreditSloCode(String^ accountID, int nRequestId, NetApi::CCreditSloCode^ data, bool isLast, XtError^ error) {};
        virtual void onReqCreditSloCodeWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::CCreditSloCode^ data, bool isLast, XtError^ error) {};
        virtual void onReqCreditSubjects(String^ accountID, int nRequestId, NetApi::CCreditSubjects^ data, bool isLast, XtError^ error) {};
        virtual void onReqCreditSubjectsWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::CCreditSubjects^ data, bool isLast, XtError^ error) {};
        virtual void onReqCreditAssure(String^ accountID, int nRequestId, NetApi::CCreditAssure^ data, bool isLast, XtError^ error) {};
        virtual void onReqCreditAssureWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::CCreditAssure^ data, bool isLast, XtError^ error) {};
        virtual void onReqTransferBank(String^ accountID, int nRequestId, NetApi::CQueryBankInfo^ data, bool isLast, XtError^ error) {};
        virtual void onReqTransferBankWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::CQueryBankInfo^ data, bool isLast, XtError^ error) {};
        virtual void onReqTransferSerial(String^ accountID, int nRequestId, NetApi::CTransferSerial^ data, bool isLast, XtError^ error) {};
        virtual void onReqTransferSerialWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::CTransferSerial^ data, bool isLast, XtError^ error) {};
        virtual void onReqBankAmount(String^ accountID, int nRequestId, NetApi::CQueryBankAmount^ data, XtError^ error) {};
        virtual void onReqBankAmountWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::CQueryBankAmount^ data, XtError^ error) {};
        virtual void onTransfer(int nRequestId, XtError^ error) {};
        virtual void onReqInstrumentInfoByMarket(int nRequestId, NetApi::CInstrumentInfo^ data, bool isLast, XtError^ error) {};
        virtual void onReqInstrumentInfoByMarketWithMkt(int nRequestId, String^ exchangeId, NetApi::CInstrumentInfo^ data, bool isLast, XtError^ error) {};
        virtual void onReqCanCancelOrderDetail(String^ accountID, int nRequestId, NetApi::COrderDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqCanCancelOrderDetailWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::COrderDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqCommandsInfo(int nRequestId, NetApi::COrderInfo^ data,bool isLast, XtError^ error) {};
        virtual void onFundTransfer(int nRequestId, XtError^ error) {};
        virtual void onSecuTransfer(int nRequestId, XtError^ error) {};
        virtual void onReqComFund(String^ accountID, int nRequestId, NetApi::CStockComFund^ data, bool isLast, XtError^ error) {};
        virtual void onReqComFundWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::CStockComFund^ data, bool isLast, XtError^ error) {};
        virtual void onReqComPosition(String^ accountID, int nRequestId, NetApi::CStockComPosition^ data, bool isLast, XtError^ error) {};
        virtual void onReqComPositionWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::CStockComPosition^ data, bool isLast, XtError^ error) {};
        virtual void onRtnAlgoError(int nOrderID, String^ strRemark, XtError^ error) {};
        virtual void onReqTradeDay(String^ tradeDay, int nRequestId, XtError^ error) {};
        virtual void onReqHistoryOrderDetail(String^ accountID, int nRequestId, NetApi::COrderDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqHistoryOrderDetailWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::COrderDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqHistoryDealDetail(String^ accountID, int nRequestId, NetApi::CDealDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqHistoryDealDetailWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::CDealDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqHistoryPositionStatics(String^ accountID, int nRequestId, NetApi::CPositionStatics^ data, bool isLast, XtError^ error) {};
        virtual void onReqHistoryPositionStaticsWithAccKey(String^ accountID, int nRequestId, String^ accountKey, NetApi::CPositionStatics^ data, bool isLast, XtError^ error) {};
        virtual void onReqFtAccCommissionRateDetail(String^ accountID, int nRequestId, String^ accountKey, NetApi::CCommissionRateDetail^ data, XtError^ error) {};
        virtual void onReqFtAccMarginRateDetail(String^ accountID, int nRequestId, String^ accountKey, NetApi::CMarginRateDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqProductIds(int nRequestId, int nProductID, String^ accountKey, bool isLast) {};
        virtual void onCreatePortfolio(int nRequestId, int nPortfolioID, String^ strRemark, XtError^ error) {};
        virtual void onReqProductPortfolio(int nProductID, int nRequestId, NetApi::CPortfolioInfo^ data, bool isLast, XtError^ error) {};
        virtual void onReqPortfolioOrder(int nPortfolioID, int nRequestId, NetApi::COrderDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqPortfolioMultiOrder(int nPortfolioID, int nRequestId, NetApi::COrderDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqPortfolioDeal(int nPortfolioID, int nRequestId, NetApi::CDealDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqPortfolioMultiDeal(int nPortfolioID, int nRequestId, NetApi::CDealDetail^ data, bool isLast, XtError^ error) {};
        virtual void onReqPortfolioPosition(int nPortfolioID, int nRequestId, NetApi::CPositionStatics^ data, bool isLast, XtError^ error) {};
        virtual void onReqStrategyInfo(String^ accountID, int nRequestId, String^ accountKey, NetApi::CStrategyInfo^ data, bool isLast, XtError^ error) {};
        virtual void onReqSecuAccount(String^ accountID, int nRequestId, String^ accountKey, NetApi::CSecuAccount^ data, bool isLast, XtError^ error) {};

        NetApi::XtTraderApi^ m_TraderApi;

    protected:
    private:
    };

    class Callback : public xti::XtTraderApiCallback
    {
    public:
        Callback(){};
        virtual ~Callback(){};

        void onConnected(bool success, const char* errorMsg);
        void onUserLogin(const char* userName, const char* password, int nRequestId, const xti::XtError& error);
        void onUserLogout(const char* userName, const char* password, int nRequestId, const xti::XtError& error);
        void onReqAccountDetail(const char* accountID, int nRequestId, const xti::CAccountDetail* data, bool isLast, const xti::XtError& error);
        void onReqAccountDetailWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::CAccountDetail* data, bool isLast, const xti::XtError& error);
        void onReqCreditAccountDetail(const char* accountID, int nRequestId, const xti::CCreditAccountDetail* data, bool isLast, const xti::XtError& error);
        void onReqCreditAccountDetailWithAccKey(const char* accountID, int nRequestId, const char* acountKey, const xti::CCreditAccountDetail* data, bool isLast, const xti::XtError& error);
        void onReqOrderDetail(const char* accountID, int nRequestId, const xti::COrderDetail* data, bool isLast, const xti::XtError& error);
        void onReqOrderDetailWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::COrderDetail* data, bool isLast, const xti::XtError& error);
        void onReqDealDetail(const char* accountID, int nRequestId, const xti::CDealDetail* data, bool isLast, const xti::XtError& error);
        void onReqDealDetailWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::CDealDetail* data, bool isLast, const xti::XtError& error);
        void onReqPositionDetail(const char* accountID, int nRequestId, const xti::CPositionDetail* data, bool isLast, const xti::XtError& error);
        void onReqPositionDetailWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::CPositionDetail* data, bool isLast, const xti::XtError& error);
        void onReqPositionStatics(const char* accountID, int nRequestId, const xti::CPositionStatics* data, bool isLast, const xti::XtError& error);
        void onReqPositionStaticsWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::CPositionStatics* data, bool isLast, const xti::XtError& error);
        void onReqStkcompacts(const char* accountID, int nRequestId, const xti::CStkCompacts* data, bool isLast, const xti::XtError& error);
        void onReqStkcompactsWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::CStkCompacts* data, bool isLast, const xti::XtError& error);
        void onReqCoveredStockPosition(const char* accountID, int nRequestId, const xti::CCoveredStockPosition* data, bool isLast, const xti::XtError& error);
        void onReqCoveredStockPositionWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::CCoveredStockPosition* data, bool isLast, const xti::XtError& error);
        void onReqStkOptCombPositionDetail(const char* accountID, int nRequestId, const xti::CStockOptionCombPositionDetail* data, bool isLast, const xti::XtError& error);
        void onReqStkOptCombPositionDetailWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::CStockOptionCombPositionDetail* data, bool isLast, const xti::XtError& error);
        void onReqCInstrumentDetail(const char* accountID, int nRequestId, const xti::CInstrumentDetail* data, bool isLast, const xti::XtError& error);
        void onReqCInstrumentDetailWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::CInstrumentDetail* data, bool isLast, const xti::XtError& error);
        void onReqPriceData(int nRequestId, const xti::CPriceData* data, const xti::XtError& error);
        void onRtnOrder(const xti::COrderInfo* data);
        void onRtnOrderDetail(const xti::COrderDetail* data);
        void onRtnDealDetail(const xti::CDealDetail* data);
        void onRtnOrderError(const xti::COrderError* data);
        void onRtnCancelError(const xti::CCancelError* data);
        void onRtnLoginStatus(const char* accountID, xti::EBrokerLoginStatus status,int brokerType, const char* errorMsg);
        void onRtnAccountDetail(const char* accountID, const xti::CAccountDetail* data);
        void onRtnCreditAccountDetail(const char* accountID, const xti::CCreditAccountDetail* data);
        void onRtnNetValue(const xti::CNetValue* data);
        void onOrder(int nRequestId, int orderID, const char* strRemark, const xti::XtError& error);
        void onDirectOrder(int nRequestId, const char* strOrderSysID, const char* strRemark, const xti::XtError& error);
        void onCancel(int nRequestId, const xti::XtError& error);
        void onCancelWithRemark(int nRequestId, const char* strRemark, const xti::XtError& error);
        void onCancelOrder(int nRequestId, const xti::XtError& error);
        void onCustomTimer();
        void onRtnLoginStatusWithActKey(const char* accountID, xti::EBrokerLoginStatus status, int brokerType, const char* accountKey, const char* errorMsg);
        void onRtnLoginStatusCustom(const char* accountID, xti::EBrokerLoginStatus status, int brokerType, const char* accountKey, const char* userName, const char* errorMsg);
        void setCallBack(NetApi::XtTraderApiCallback^);
        void onRtnPriceData(const xti::CPriceData& data);
        void onSubscribQuote(int nRequestId, const xti::CSubscribData* data, const xti::XtError& error);
        void onUnSubscribQuote(int nRequestId, const xti::CSubscribData* data, const xti::XtError& error);
        void onReqReferenceRate(const char* accountID, int nRequestId, const xti::CReferenceRate* data, bool isLast, const xti::XtError& error);
        void onReqReferenceRateWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::CReferenceRate* data, bool isLast, const xti::XtError& error);
        void onReqCreditDetail(const char* accountID, int nRequestId, const xti::CCreditDetail* data, bool isLast, const xti::XtError& error);
        void onReqCreditDetailWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::CCreditDetail* data, bool isLast, const xti::XtError& error);
        void onOperateTask(const char* accountID, int nRequestId, const char* accountKey, const xti::XtError& error);
        void onModifyAlgoCommands(int nRequestId, int orderID, const char* strRemark, const xti::XtError& error);
        void onReqSubscribeInfo(const char* accountID, int nRequestId, const xti::CSubscribeInfo* data, bool isLast, const xti::XtError& error);
        void onReqSubscribeInfoWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::CSubscribeInfo* data, bool isLast, const xti::XtError& error);
        void onReqStkUnCloseCompact(const char* accountID, int nRequestId, const xti::CStkUnClosedCompacts* data, bool isLast, const xti::XtError& error);
        void onReqStkUnCloseCompactWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::CStkUnClosedCompacts* data, bool isLast, const xti::XtError& error);
        void onReqStkClosedCompact(const char* accountID, int nRequestId, const xti::CStkClosedCompacts* data, bool isLast, const xti::XtError& error);
        void onReqStkClosedCompactWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::CStkClosedCompacts* data, bool isLast, const xti::XtError& error);
        void onReqAccountKey(int nRequestId, const xti::CAccountKey* data, bool isLast, const xti::XtError& error);
        void onReqDealDetailBySysID(const char* accountID, int nRequestId, const char* orderSyeId, const char* exchangeId, const xti::CDealDetail* data, bool isLast, const xti::XtError& error);
        void onReqDealDetailBySysIDWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const char* orderSyeId, const char* exchangeId, const xti::CDealDetail* data, bool isLast, const xti::XtError& error);
        void onReqDeliveryDetail(const char* accountID, int nRequestId, const xti::CDeliveryDetail* data, bool isLast, const xti::XtError& error);
        void onReqDeliveryDetailWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::CDeliveryDetail* data, bool isLast, const xti::XtError& error);
        void onReqSingleInstrumentInfo(int nRequestId, const xti::CInstrumentInfo* data, const xti::XtError& error);
        void onRtnExchangeStatus(const xti::CExchangeStatus* data);
        void onRtnCreditDetail(const xti::CCreditDetail* data);
        void onReqOpVolume(const char* accountID, int nRequestId, const char* dataKey, int nVolume, bool isLast, const xti::XtError& error);
        void onReqOpVolumeWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const char* dataKey, int nVolume, bool isLast, const xti::XtError& error);
        void onReqCreditSloCode(const char* accountID, int nRequestId, const xti::CCreditSloCode* data, bool isLast, const xti::XtError& error);
        void onReqCreditSloCodeWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::CCreditSloCode* data, bool isLast, const xti::XtError& error);
        void onReqCreditSubjects(const char* accountID, int nRequestId, const xti::CCreditSubjects* data, bool isLast, const xti::XtError& error);
        void onReqCreditSubjectsWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::CCreditSubjects* data, bool isLast, const xti::XtError& error);
        void onReqCreditAssure(const char* accountID, int nRequestId, const xti::CCreditAssure* data, bool isLast, const xti::XtError& error);
        void onReqCreditAssureWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::CCreditAssure* data, bool isLast, const xti::XtError& error);
        void onReqTransferBank(const char* accountID, int nRequestId, const xti::CQueryBankInfo* data, bool isLast, const xti::XtError& error);
        void onReqTransferBankWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::CQueryBankInfo* data, bool isLast, const xti::XtError& error);
        void onReqTransferSerial(const char* accountID, int nRequestId, const xti::CTransferSerial* data, bool isLast, const xti::XtError& error);
        void onReqTransferSerialWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::CTransferSerial* data, bool isLast, const xti::XtError& error);
        void onReqBankAmount(const char* accountID, int nRequestId, const xti::CQueryBankAmount* data, const xti::XtError& error);
        void onReqBankAmountWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::CQueryBankAmount* data, const xti::XtError& error);
        void onTransfer(int nRequestId, const xti::XtError& error);
        void onReqInstrumentInfoByMarket(int nRequestId, const xti::CInstrumentInfo* data, bool isLast, const xti::XtError& error);
        void onReqInstrumentInfoByMarketWithMkt(int nRequestId, const char* exchangeId, const xti::CInstrumentInfo* data, bool isLast, const xti::XtError& error);
        void onReqCanCancelOrderDetail(const char* accountID, int nRequestId, const xti::COrderDetail* data, bool isLast, const xti::XtError& error);
        void onReqCanCancelOrderDetailWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::COrderDetail* data, bool isLast, const xti::XtError& error);
        void onReqCommandsInfo(int nRequestId,  const xti::COrderInfo* data, bool isLast, const xti::XtError& error);
        void onFundTransfer(int nRequestId, const xti::XtError& error);
        void onSecuTransfer(int nRequestId, const xti::XtError& error);
        void onReqComFund(const char* accountID, int nRequestId, const xti::CStockComFund* data, bool isLast, const xti::XtError& error);
        void onReqComFundWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::CStockComFund* data, bool isLast, const xti::XtError& error);
        void onReqComPosition(const char* accountID, int nRequestId, const xti::CStockComPosition* data, bool isLast, const xti::XtError& error);
        void onReqComPositionWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::CStockComPosition* data, bool isLast, const xti::XtError& error);
        void onRtnAlgoError(int nOrderID, const char* strRemark, const xti::XtError& error);
        void onReqTradeDay(const char* tradeDay, int nRequestId, const xti::XtError& error);
        void onReqHistoryOrderDetail(const char* accountID, int nRequestId, const xti::COrderDetail* data, bool isLast, const xti::XtError& error);
        void onReqHistoryOrderDetailWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::COrderDetail* data, bool isLast, const xti::XtError& error);
        void onReqHistoryDealDetail(const char* accountID, int nRequestId, const xti::CDealDetail* data, bool isLast, const xti::XtError& error);
        void onReqHistoryDealDetailWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::CDealDetail* data, bool isLast, const xti::XtError& error);
        void onReqHistoryPositionStatics(const char* accountID, int nRequestId, const xti::CPositionStatics* data, bool isLast, const xti::XtError& error);
        void onReqHistoryPositionStaticsWithAccKey(const char* accountID, int nRequestId, const char* accountKey, const xti::CPositionStatics* data, bool isLast, const xti::XtError& error);
        void onReqFtAccCommissionRateDetail(const char* accountID, int nRequestId, const char* accountKey, const xti::CCommissionRateDetail* data, const xti::XtError& error);
        void onReqFtAccMarginRateDetail(const char* accountID, int nRequestId, const char* accountKey, const xti::CMarginRateDetail* data, bool isLast, const xti::XtError& error);
        void onReqProductIds(int nRequestId, int nProductID, const char* accountKey, bool isLast);
        void onCreatePortfolio(int nRequestId, int nPortfolioID, const char* strRemark, const xti::XtError& error);
        void onReqProductPortfolio(int nProductID, int nRequestId, const xti::CPortfolioInfo* data, bool isLast, const xti::XtError& error);
        void onReqPortfolioOrder(int nPortfolioID, int nRequestId, const xti::COrderDetail* data, bool isLast, const xti::XtError& error);
        void onReqPortfolioMultiOrder(int nPortfolioID, int nRequestId, const xti::COrderDetail* data, bool isLast, const xti::XtError& error);
        void onReqPortfolioDeal(int nPortfolioID, int nRequestId, const xti::CDealDetail* data, bool isLast, const xti::XtError& error);
        void onReqPortfolioMultiDeal(int nPortfolioID, int nRequestId, const xti::CDealDetail* data, bool isLast, const xti::XtError& error);
        void onReqPortfolioPosition(int nPortfolioID, int nRequestId, const xti::CPositionStatics* data, bool isLast, const xti::XtError& error);
        void onReqStrategyInfo(const char* accountID, int nRequestId, const char* accountKey, const xti::CStrategyInfo* data, bool isLast, const xti::XtError& error);
        void onReqSecuAccount(const char* accountID, int nRequestId, const char* accountKey, const xti::CSecuAccount* data, bool isLast, const xti::XtError& error);

    protected:

    private:
        gcroot<NetApi::XtTraderApiCallback^ > m_XtTraderApiCallback;
    };

}

#endif
