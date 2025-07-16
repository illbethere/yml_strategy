/********************************************************************
    company:    北京睿智融科控股有限公司
    fileName:     XtNetStructs.h
    author:    jianxin
    purpose:    结构定义
*********************************************************************/
#ifndef XTNETSTRUCT_2015_02_25_H
#define XTNETSTRUCT_2015_02_25_H

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#include "XtNetDataType.h"

using namespace System;

namespace NetApi
{

    public ref struct CPriceData
    {
        String^  m_strTradingDay;         //交易日
        String^  m_strExchangeID;         //交易所代码
        String^  m_strInstrumentID;       //合约代码
        String^  m_strInstrumentName;     //合约名称
        String^  m_strExchangeInstID;     //合约在交易所的代码
        double  m_dLastPrice;                //最新价
        double  m_dUpDown;                   //涨跌
        double  m_dUpDownRate;               //涨跌幅
        double  m_dAveragePrice;             //当日均价
        int  m_nVolume;                   //数量
        double  m_dTurnover;                 //成交金额
        double  m_dPreClosePrice;            //昨收盘
        double  m_dPreSettlementPrice;       //上次结算价
        double  m_dPreOpenInterest;          //昨持仓量
        double  m_dOpenInterest;             //持仓量
        double  m_dSettlementPrice;          //本次结算价
        double  m_dOpenPrice;                //今开盘
        double  m_dHighestPrice;             //最高价
        double  m_dLowestPrice;              //最低价
        double  m_dClosePrice;               //今收盘
        double  m_dUpperLimitPrice;          //涨停板价
        double  m_dLowerLimitPrice;          //跌停板价
        double  m_dPreDelta;                 //昨虚实度
        double  m_dCurrDelta;                //今虚实度
        String^  m_strUpdateTime;         //最后修改时间
        int  m_nUpdateMillisec;           //最后修改毫秒
        double  m_dBidPrice1;                //申买价一
        int  m_nBidVolume1;               //申买量一
        double  m_dAskPrice1;                //申卖价一
        int  m_nAskVolume1;               //申卖量一
        double  m_dBidPrice2;                //申买价二
        int  m_nBidVolume2;               //申买量二
        double  m_dAskPrice2;                //申卖价二
        int  m_nAskVolume2;               //申卖量二
        double  m_dBidPrice3;                //申买价三
        int  m_nBidVolume3;               //申买量三
        double  m_dAskPrice3;                //申卖价三
        int  m_nAskVolume3;               //申卖量三
        double  m_dBidPrice4;                //申买价四
        int  m_nBidVolume4;               //申买量四
        double  m_dAskPrice4;                //申卖价四
        int  m_nAskVolume4;               //申卖量四
        double  m_dBidPrice5;                //申买价五
        int  m_nBidVolume5;               //申买量五
        double  m_dAskPrice5;                //申卖价五
        int  m_nAskVolume5;               //申卖量五
        double  m_dPrePrice;                 //前一次的价格
    };

    public ref struct CStkSubjects
    {
        String^  m_strAccountID;          //账号
        String^  m_strExchangeID;         //市场
        String^  m_strInstrumentID;       //合约
        double  m_dSloRatio;                 //融资融券保证金比例
        EXTSubjectsStatus  m_eSloStatus;                //融券状态
        int  m_nEnableAmount;             //融券可融数量
        double  m_dFinRatio;                 //融资保证金比例
        EXTSubjectsStatus  m_eFinStatus;                //融资状态
        double  m_dAssureRatio;              //担保品折算比例
        EXTSubjectsStatus  m_eAssureStatus;             //是否可做担保
        double  m_dFinRate;                  //融资日利率
        double  m_dSloRate;                  //融券日利率
        double  m_dFinPenaltyRate;           //融资日罚息利率
        double  m_dSloPenaltyRate;           //融券日罚息利率
    };

    public ref struct COrderDetail
    {
        String^  m_strAccountID; 
        int  m_nAccountType;         //账号类型
        String^  m_strExchangeID;     //交易所代码
        String^  m_strProductID;      //合约品种
        String^  m_strInstrumentID;   //合约代码
        double  m_dLimitPrice;           //限价单的限价，就是报价
        String^  m_strOrderSysID;     //委托号
        int  m_nTradedVolume;         //已成交量
        int  m_nTotalVolume;          //当前总委托量
        double  m_dFrozenMargin;         //冻结保证金
        double  m_dFrozenCommission;     //冻结手续费
        double  m_dAveragePrice;         //成交均价
        double  m_dTradeAmount;          //成交额 期货=均价*量*合约乘数
        int  m_nErrorID; 
        String^  m_strErrorMsg; 
        String^  m_strInsertDate;     //日期
        String^  m_strInsertTime;     //时间
        int  m_nOrderID;              //指令ID
        EBrokerPriceType  m_nOrderPriceType;       //类型，例如市价单 限价单
        EEntrustBS  m_nDirection;            //期货多空，该字段与m_eOffsetFlag一起判断期货的报单类型。股票无用
        EOffsetFlagType  m_eOffsetFlag;           //期货开平，股票买卖
        EHedgeFlagType  m_eHedgeFlag;            //投机 套利 套保
        EEntrustSubmitStatus  m_eOrderSubmitStatus;    //提交状态，股票里面不需要报单状态
        EEntrustStatus  m_eOrderStatus;          //委托状态
        EEntrustTypes  m_eEntrustType;          //委托类别
        ECoveredFlag  m_eCoveredFlag;         //备兑标记 '0' - 非备兑，'1' - 备兑
        String^  m_strRemark;       //投资备注
        String^  m_strCancelInfo;       //废单信息
        String^  m_strInstrumentName;   //合约名称
        String^  m_strAccountKey;       //账户key
        String^  m_strStrategyID;       //收益互换策略ID
        String^  m_strSecuAccount;       //股东号
    };

    public ref struct CStkCompacts
    {
        String^  m_strAccountID;          //账号
        String^  m_strExchangeID;         //交易所
        String^  m_strInstrumentID;       //证券代码
        int  m_nOpenDate;                 //合约开仓日期
        String^  m_strCompactId;          //合约编号
        double  m_dCrdtRatio;                //融资融券保证金比例
        String^  m_strEntrustNo;          //委托编号
        double  m_dEntrustPrice;             //委托价格
        int  m_nEntrustVol;               //委托数量
        int  m_nBusinessVol;              //合约开仓数量
        double  m_dBusinessBalance;          //合约开仓金额
        double  m_dBusinessFare;             //合约开仓费用
        EXTCompactType  m_eCompactType;              //合约类型
        EXTCompactStatus  m_eCompactStatus;        //合约状态
        double  m_dRealCompactBalance;       //未还合约金额
        int  m_nRealCompactVol;           //未还合约数量
        double  m_dRealCompactFare;          //未还合约费用
        double  m_dRealCompactInterest;      //未还合约利息
        double  m_dRepaidInterest;           //已还利息
        int  m_nRepaidVol;                //已还数量
        double  m_dRepaidBalance;            //已还金额
        double  m_dCompactInterest;          //合约总利息
        double  m_dUsedBailBalance;          //占用保证金
        double  m_dYearRate;                 //合约年利率
        int  m_nRetEndDate;               //归还截止日
        String^  m_strDateClear;          //了结日期
        double  m_dPrice;                    //最新价
        int  m_nOpenTime;                 //开仓的时间，不展示，部分券商可能用的上
        int  m_nCancelVol;                //合约对应的委托的撤单数量
        EBrokerPriceType  m_nOrderPriceType;       //类型，例如市价单 限价单
        EOffsetFlagType  m_nOffsetFlag;             //操作,开平,买卖,操作
    };

    public ref struct CPositionDetail
    {
        String^  m_strAccountID; 
        String^  m_strExchangeID;     //市场代码
        String^  m_strProductID;      //合约品种
        String^  m_strInstrumentID;   //合约代码
        String^  m_strInstrumentName; //合约名称
        String^  m_strOpenDate; 
        String^  m_strTradeID;        //最初开仓位的成交
        int  m_nVolume;               //持仓量 当前拥股
        double  m_dOpenPrice;            //开仓价
        String^  m_strTradingDay;     //交易日
        double  m_dMargin;               //使用的保证金 历史的直接用ctp的，新的自己用成本价*存量*系数算  股票不需要
        double  m_dOpenCost;             //开仓成本 等于股票的成本价*第一次建仓的量，后续减持不影响，不算手续费 股票不需要
        double  m_dSettlementPrice;      //结算价 对于股票的当前价
        int  m_nCloseVolume;          //平仓量 等于股票已经卖掉的 股票不需要
        double  m_dCloseAmount;          //平仓额 等于股票每次卖出的量*卖出价*合约乘数（股票为1）的累加 股票不需要
        double  m_dFloatProfit;          //浮动盈亏 当前量*（当前价-开仓价）*合约乘数（股票为1）
        double  m_dCloseProfit;          //平仓盈亏 平仓额 - 开仓价*平仓量*合约乘数（股票为1） 股票不需要
        double  m_dMarketValue;          //市值 合约价值
        double  m_dPositionCost;         //持仓成本 股票不需要
        double  m_dPositionProfit;       //持仓盈亏 股票不需要
        double  m_dLastSettlementPrice;  //最新结算价 股票不需要
        double  m_dInstrumentValue;      //合约价值 股票不需要
        bool  m_bIsToday;              //是否今仓
        int  m_nOrderID;              //指令ID
        int  m_nFrozenVolume;         //期货不用这个字段，冻结数量
        int  m_nCanUseVolume;         //期货不用这个字段，股票的可用数量
        int  m_nOnRoadVolume;         //期货不用这个字段，股票的在途数量
        int  m_nYesterdayVolume;      //期货不用这个字段，股票的股份余额
        double  m_dLastPrice;            //结算价 对于股票的当前价
        EHedgeFlagType  m_nHedgeFlag;    //投机 套利 套保
        EEntrustBS  m_nDirection;    //期货多空，该字段与m_eOffsetFlag一起判断期货的报单类型。股票无用
        int  m_nCoveredAmount;            //备兑数量
        int         m_nAccountType;         // 账号类型
        double      m_dProfitRate;          // 持仓盈亏比例
        String^  m_strAccountKey;           //账户key
        String^  m_strStrategyID;       //收益互换策略ID
        String^  m_strSecuAccount;       //股东号
    };

    public ref struct CCoveredStockPosition
    {
        String^  m_strAccountID;          //账号
        String^  m_strExchangeID;         //交易类别
        String^  m_strExchangeName;       //市场名字
        String^  m_strInstrumentID;       //合约代码
        String^  m_strInstrumentName;     //合约名称
        int  m_nTotalAmount;              //总持仓量
        int  m_nLockAmount;               //锁定量
        int  m_nUnlockAmount;             //未锁定量
        int  m_nCoveredAmount;            //备兑数量
    };

    public ref struct CCreditAccountDetail
    {
        double  m_dPerAssurescaleValue;      //个人维持担保比例
        double  m_dEnableBailBalance;        //可用保证金
        double  m_dUsedBailBalance;          //已用保证金
        double  m_dAssureEnbuyBalance;       //可买担保品资金
        double  m_dFinEnbuyBalance;          //可买标的券资金
        double  m_dSloEnrepaidBalance;       //可还券资金
        double  m_dFinEnrepaidBalance;       //可还款资金
        double  m_dFinMaxQuota;              //融资授信额度
        double  m_dFinEnableQuota;           //融资可用额度
        double  m_dFinUsedQuota;             //融资已用额度
        double  m_dFinUsedBail;              //融资已用保证金额
        double  m_dFinCompactBalance;        //融资合约金额
        double  m_dFinCompactFare;           //融资合约费用
        double  m_dFinCompactInterest;       //融资合约利息
        double  m_dFinMarketValue;           //融资市值
        double  m_dFinIncome;                //融资合约盈亏
        double  m_dSloMaxQuota;              //融券授信额度
        double  m_dSloEnableQuota;           //融券可用额度
        double  m_dSloUsedQuota;             //融券已用额度
        double  m_dSloUsedBail;              //融券已用保证金额
        double  m_dSloCompactBalance;        //融券合约金额
        double  m_dSloCompactFare;           //融券合约费用
        double  m_dSloCompactInterest;       //融券合约利息
        double  m_dSloMarketValue;           //融券市值
        double  m_dSloIncome;                //融券合约盈亏
        double  m_dOtherFare;                //其它费用
        double  m_dUnderlyMarketValue;       //标的证券市值
        double  m_dFinEnableBalance;         //可融资金额
        double  m_dDiffEnableBailBalance;    //可用保证金调整值
        double  m_dBuySecuRepayFrozenMargin; //买券还券冻结资金
        double  m_dBuySecuRepayFrozenCommission;  //买券还券冻结手续费
    };

    public ref struct CNetValue
    {
        int  m_nProductId;        //迅投产品ID
        int  m_nTypes;            //产品类型 1-普通基金 2-分级基金
        double  m_dTotalNetValue;    //产品净资产, 产品净值
        double  m_dNetValue;         //母基金单位净值
        double  m_dBNetValue;        //B级基金单位净值
        int  m_nUpdateTime;       //更新时间
    };

    public ref struct COrderInfo
    {
        String^  m_strAccountID;   //资金账号
        int  m_nAccountType;  //账号类型
        int  m_nOrderID;           //指令ID
        int  m_startTime;          //下达时间
        int  m_endTime;            //结束时间
        EOrderCommandStatus  m_eStatus;            //状态
        double  m_dTradedVolume;      //成交量
        String^  m_strMsg;        //指令执行信息
        String^  m_canceler;       //撤销者
        EXTBrokerType  m_eBrokerType;       //账号类型
        String^  m_strRemark;       //投资备注
        String^ m_strMarket;                                //市场
        String^ m_strInstrument;                            //合约
        String^ m_strOrderType;                             //算法名称
        double  m_dPrice;                                   //基准价
        int     m_nVolume;                                  //下单总量
        int     m_nValidTimeStart;                          //有效开始时间
        int     m_nValidTimeEnd;                            //有效结束时间
        double  m_dMaxPartRate;                             //量比比例
        double  m_dMinAmountPerOrder;                       //委托最小金额
        EOperationType  m_eOperationType;                   //下单操作
        EStopTradeForOwnHiLow  m_nStopTradeForOwnHiLow;     //涨跌停控制
    };

    public ref struct CCancelError
    {
        String^  m_strAccountID;   //资金账号
        int  m_nErrorID;          //错误号
        String^  m_strErrorMsg;   //错误信息
        int  m_nOrderID;          //指令ID
        int  m_nRequestID;        //请求ID
        String^  m_strRemark; //投资备注
        String^  m_strAccountKey; //账号key
    };

    public ref struct CDealDetail
    {
        String^  m_strAccountID; 
        int  m_nAccountType;         //账号类型
        String^  m_strExchangeID;    //交易所代码
        String^  m_strProductID;     //合约品种
        String^  m_strInstrumentID;  //合约代码
        String^  m_strTradeID;       //成交编号
        String^  m_strOrderSysID;    //委托
        double  m_dAveragePrice;        //成交均价
        int  m_nVolume;              //成交量 期货单位手 股票做到股
        String^  m_strTradeDate;     //成交日期
        String^  m_strTradeTime;     //成交时间
        double  m_dComssion;            //手续费
        double  m_dAmount;              //成交额 期货=均价*量*合约乘数
        int  m_nOrderID;             //指令ID
        EEntrustBS  m_nDirection;           //期货多空，该字段与m_eOffsetFlag一起判断期货的报单类型。股票无用
        EOffsetFlagType  m_nOffsetFlag;          //期货开平 股票买卖
        EHedgeFlagType  m_nHedgeFlag;           //投机 套利 套保
        EBrokerPriceType  m_nOrderPriceType;      //类型，例如市价单 限价单
        EEntrustTypes  m_eEntrustType;         //委托类别
        ECoveredFlag  m_eCoveredFlag;        //备兑标记 '0' - 非备兑，'1' - 备兑
        String^  m_strRemark;       //投资备注
        String^  m_strInstrumentName;       //合约名称
        String^  m_strAccountKey;           //账户key
        String^  m_strStrategyID;       //收益互换策略ID
        String^  m_strSecuAccount;       //股东号
    };

    public ref struct COrderError
    {
        String^  m_strAccountID; //资金账号
        int  m_nErrorID;         //错误号
        String^  m_strErrorMsg;  //错误信息
        int  m_nOrderID;          //指令ID
        int  m_nRequestID;         //请求ID
        String^  m_strRemark; //投资备注
        String^  m_strAccountKey; //账号key
    };

    public ref struct CPositionStatics
    {
        String^  m_strAccountID; 
        String^  m_strExchangeID; 
        String^  m_strProductID;      //合约品种
        String^  m_strInstrumentID;   //合约代码
        String^  m_strInstrumentName; //合约名称
        bool  m_bIsToday;              //是否今仓
        int  m_nPosition;             //持仓 需要
        double  m_dOpenCost;             //非任务平冻结
        double  m_dPositionCost;         //持仓成本 detail的汇总
        double  m_dAveragePrice;             //算法待找
        double  m_dPositionProfit;       //持仓盈亏 detail的汇总
        double  m_dFloatProfit;          //浮动盈亏 detail的汇总
        double  m_dOpenPrice;            //开仓均价 股票不需要
        int  m_nCanCloseVolume;          //可平
        double  m_dUsedMargin;           //已使用保证金
        double  m_dUsedCommission;       //已使用的手续费
        double  m_dFrozenMargin;         //冻结保证金
        double  m_dFrozenCommission;     //冻结手续费
        double  m_dInstrumentValue;      //合约价值
        int  m_nOpenTimes;            //开仓次数
        int  m_nOpenVolume;           //总开仓量 中间平仓不减
        int  m_nCancelTimes;          //撤单次数
        int  m_nFrozenVolume;         //期货不用这个字段，冻结数量
        int  m_nCanUseVolume;         //期货不用这个字段，股票的可用数量
        int  m_nOnRoadVolume;         //期货不用这个字段，股票的在途数量
        int  m_nYesterdayVolume;      //期货不用这个字段，股票的股份余额
        double  m_dSettlementPrice;      //前收盘价
        double  m_dProfitRate;           //持仓盈亏比例
        EEntrustBS  m_nDirection;    //期货多空，该字段与m_eOffsetFlag一起判断期货的报单类型。股票无用
        EHedgeFlagType  m_nHedgeFlag;    //投机 套利 套保
        int      m_nCoveredAmount;   //备兑数量
        int         m_nAccountType;         // 账号类型
        double  m_dLastPrice;      //最新价
        String^  m_strStrategyID;       //收益互换策略ID
        String^  m_strAccountKey; //账号key
        String^  m_strSecuAccount;       //股东号
    };

    public ref struct CAccountDetail
    {
        String^  m_strAccountID; 
        int      m_nAccountType;           ///< 账号类型
        String^  m_strStatus;             // 状态
        String^  m_strTradingDate; 
        double  m_dFrozenMargin;             // 外源性 股票的保证金就是冻结资金 股票不需要
        double  m_dFrozenCash;               // 内外源冻结保证金和手续费四个的和
        double  m_dFrozenCommission;         // 外源性冻结资金源
        double  m_dRisk;                     // 风险度
        double  m_dNav;                      // 单位净值
        double  m_dPreBalance;               // 期初权益
        double  m_dBalance;                  // 动态权益, 总资产
        double  m_dAvailable;                // 可用资金
        double  m_dCommission;               // 已用手续费
        double  m_dPositionProfit;           // 持仓盈亏
        double  m_dCloseProfit;              // 平仓盈亏
        double  m_dCashIn;                   // 出入金净值
        double  m_dCurrMargin;               // 当前占用保证金
        double  m_dInstrumentValue;          // 合约价值
        double  m_dDeposit;                  // 入金
        double  m_dWithdraw;                 // 出金
        double  m_dCredit;                   // 信用额度
        double  m_dMortgage;                 // 质押
        double  m_dStockValue;               // 股票总市值，期货没有
        double  m_dLoanValue;                // 债券总市值，期货没有
        double  m_dFundValue;                // 基金总市值，包括ETF和封闭式基金，期货没有
        double  m_dRepurchaseValue;          // 回购总市值，所有回购，期货没有
        double  m_dLongValue;                // 多单总市值，现货没有
        double  m_dShortValue;               // 空单总市值，现货没有
        double  m_dNetValue;                 // 净持仓总市值，净持仓市值=多-空
        double  m_dAssureAsset;              // 净资产
        double  m_dTotalDebit;               // 总负债
        double  m_dPremiumNetExpense;       // 权利金净支出 用于股票期权
        double  m_dEnableMargin;            // 可用保证金 用于股票期权
        double  m_dFetchBalance;            // 可取金额
        EDualStatus m_eDualStatus;          // 双中心状态
        double      m_dAvailableSH;         // 双中心上海可用
        double      m_dAvailableSZ;         // 双中心深圳可用      
        String^  m_strAccountKey;           //账户key
        int         m_nProductId;           // 迅投产品ID
        double  m_dUsedMargin;            // 占用保证金 用于股票期权
        double  m_dRoyalty;            // 权利金支出 用于股票期权
    };

    public ref struct CCommissionRateDetail
    {
        String^           m_strExchangeID;
        String^           m_strInstrumentID;
        double            m_dOpenRatioByMoney;
        double            m_dOpenRatioByVolume;
        double            m_dCloseRatioByMoney;
        double            m_dCloseRatioByVolume;
        double            m_dCloseTodayRatioByMoney;
        double            m_dCloseTodayRatioByVolume;
        String^           m_strTradeDate;
    };

    public ref struct CMarginRateDetail
    {
        String^           m_strExchangeID;
        String^           m_strInstrumentID;
        int               m_nHedgeFlag;
        double            m_dLongMarginRatioByMoney;
        double            m_dLongMarginRatioByVolume;
        double            m_dShortMarginRatioByMoney;
        double            m_dShortMarginRatioByVolume;
        int               m_nIsRelative;
        String^           m_strTradeDate;
    };

    public ref struct COrdinaryOrder
    {
        COrdinaryOrder()
        {
            m_strAccountID = "";
            m_strMarket = "";
            m_strInstrument = "";
            m_dPrice = Double::MaxValue;
            m_dSuperPriceRate = 0.0;
            m_eOperationType = EOperationType::OPT_INVALID;
            m_nVolume = INT_MAX;
            m_ePriceType = EPriceType::PRTP_INVALID;
            m_eHedgeFlag = EHedgeFlagType::HEDGE_FLAG_SPECULATION;
            m_eTimeCondition = ETimeCondition::TIME_CONDITION_GFD;
            m_eVolumeCondition = EVolumeCondition::VOLUME_CONDITION_ANY;
            m_strSecondInstrument = "";
            m_dSecondPrice = 0.0;
            m_eFirstSideFlag = ESideFlag::SIDE_FLAG_RIGHT;
            m_eSecondSideFlag = ESideFlag::SIDE_FLAG_RIGHT;
            m_strCombID = "";
            m_strRemark = "";
            m_eTriggerType = EOpTriggerType::OTT_NONE;
            m_dTriggerPrice = 0.0;
            m_dSuperPrice = 0.0;
            m_nPortfolioID = -1;
            m_eAbroadDurationType = EAbroadDurationType::TYPE_DURATION_MKT;
            m_strStrategyID = "";
            m_strSecuAccount = "";
        }
        ~COrdinaryOrder(){};
        String^  m_strAccountID;      // 资金账户ID，如果为子账户，则为子账户ID
        double  m_dPrice;                // 指定价，仅在报价方式为PRTP_FIX(指定价)时有效;
        double  m_dSuperPriceRate;       // 单笔超价百分比
        int  m_nVolume;               // 委托量, 直接还券的数量
        String^  m_strMarket;         // 合约市场
        String^  m_strInstrument;     // 委托合约.
        EPriceType  m_ePriceType;            // 报价方式： 指定价，最新价 对手价……
        EOperationType  m_eOperationType;        // 下单类型，开、平、买、卖…
        EHedgeFlagType  m_eHedgeFlag;            // 套利标志
        double  m_dOccurBalance;         //直接还款的金额 //仅直接还款用
        ETimeCondition m_eTimeCondition; //期货条件单时间条件
        EVolumeCondition m_eVolumeCondition; //期货条件单数量条件
        String^            m_strSecondInstrument;    // 期权组合委托合约
        double        m_dSecondPrice;    // 期权组合委托价
        ESideFlag    m_eFirstSideFlag; //第一腿合约持仓类型
        ESideFlag    m_eSecondSideFlag; //第二腿合约持仓类型
        String^             m_strCombID;    // 组合持仓编号，用于解除组合策略
        String^      m_strRemark;       //投资备注
        EOpTriggerType      m_eTriggerType;             ///< 触价类型
        double              m_dTriggerPrice;            ///< 触价价格
        double              m_dSuperPrice;              ///< 单笔超价,和m_dSuperPriceRate只用设置一个，优先使用m_dSuperPriceRat
        int                 m_nPortfolioID;             ///< 投组类型编号
        EAbroadDurationType m_eAbroadDurationType;      ///< 外盘期货报价类型
        String^  m_strStrategyID;       //收益互换策略ID
        String^  m_strSecuAccount;       //多股东时指定下单的股东号
    };

    public ref struct CAlgorithmOrder
    {

        CAlgorithmOrder()
        {
            m_strAccountID = "";
            m_strMarket= "";
            m_strInstrument = "";
            m_dPrice = Double::MaxValue;
            m_dSuperPriceRate = 0.0;
            m_nSuperPriceStart = 1;
            m_nVolume = INT_MAX;
            m_dSingleVolumeRate = Double::MaxValue;
            m_nSingleNumMin = INT_MAX;
            m_nSingleNumMax = INT_MAX;
            m_dPlaceOrderInterval = 30;
            m_dWithdrawOrderInterval = 30;
            m_nMaxOrderCount = 100;
            m_eOperationType = EOperationType::OPT_INVALID;
            m_ePriceType = EPriceType::PRTP_INVALID;
            m_eSingleVolumeType = EVolumeType::VOLUME_FIX;
            m_eHedgeFlag = EHedgeFlagType::HEDGE_FLAG_SPECULATION;
            m_eTimeCondition = ETimeCondition::TIME_CONDITION_GFD;
            m_eVolumeCondition = EVolumeCondition::VOLUME_CONDITION_ANY;
            m_strRemark = "";
            m_eTriggerType = EOpTriggerType::OTT_NONE;
            m_dTriggerPrice = 0.0;
            m_dSuperPrice = 0.0;
            m_eAlgoPriceType = EAlgoPriceType::EALGO_PRT_MARKET;
            m_nExtraLimitType = 0;
            m_dExtraLimitValue = 0.0;

            m_strStrategyID = "";
            m_eUndealtEntrustRule = EPriceType::PRTP_INVALID;
            m_eCmdDateLimit = EXTCommandDateLimit::XT_COMMAND_LIMIT_NO_OVER_DAY;
            m_nLimitedPriceType = 0;
            m_dPriceRangeMin = 0.0;
            m_dPriceRangeMax = 0.0;
            m_nStopTradeForOwnHiLow = EStopTradeForOwnHiLow::STOPTRADE_NONE;
        };
        ~CAlgorithmOrder(){};
        String^  m_strAccountID;                        //账号
        String^  m_strMarket;                           //市场
        String^  m_strInstrument;                       //合约
        double  m_dPrice; 
        double  m_dSuperPriceRate;                      //单笔超价比率
        int  m_nSuperPriceStart;                        //超价起始笔数
        int  m_nVolume;                                 //量
        double  m_dSingleVolumeRate;                    //单比下单比率
        int  m_nSingleNumMin;                           //单比下单量最小值
        int  m_nSingleNumMax;                           //单比下单量最大值
        int  m_nLastVolumeMin;                          //尾单最小量
        double  m_dPlaceOrderInterval;                  //下单间隔
        double  m_dWithdrawOrderInterval;               //撤单间隔
        int  m_nMaxOrderCount;                          //最大下单次数，与下单间隔相对应
        int  m_nValidTimeStart;                         //有效开始时间 来自股票，待定
        int  m_nValidTimeEnd;                           //有效结束时间 来自股票，待定
        EOperationType  m_eOperationType;               //下单操作：开平、多空……
        EVolumeType  m_eSingleVolumeType;               //单笔下单基准
        EPriceType  m_ePriceType;                       //报价方式：对手、最新……
        EHedgeFlagType  m_eHedgeFlag;                   // 套利标志
        EXtOverFreqOrderMode  m_eOverFreqOrderMode;     //委托频率过快时的处理方式
        ETimeCondition m_eTimeCondition;                //期货条件单时间条件
        EVolumeCondition m_eVolumeCondition;            //期货条件单数量条件
        String^      m_strRemark;                       //投资备注
        EOpTriggerType      m_eTriggerType;             // 触价类型
        double              m_dTriggerPrice;            // 触价价格
        double              m_dSuperPrice;              // 单笔超价,和m_dSuperPriceRate只用设置一个，优先使用m_dSuperPriceRate
        EAlgoPriceType      m_eAlgoPriceType;           // 订单类型
        int                 m_nExtraLimitType;          // 扩展限价类型
        double              m_dExtraLimitValue;         // 扩展限价

        String^             m_strStrategyID;            ///< 收益互换策略ID
        EPriceType          m_eUndealtEntrustRule;      ///< 未成委托处理
        EXTCommandDateLimit m_eCmdDateLimit;            ///< 指令跨日开关
        int                 m_nLimitedPriceType;        ///< 价格限制类型
        double              m_dPriceRangeMin;           ///< 波动区间下限
        double              m_dPriceRangeMax;           ///< 波动区间上限
        EStopTradeForOwnHiLow   m_nStopTradeForOwnHiLow;        ///< 涨跌停控制
    };

    public ref struct CGroupOrder
    {
        CGroupOrder()
        {
            m_orderParam = gcnew CAlgorithmOrder();
            m_strMarket = gcnew array<String^>(1000);
            m_strInstrument = gcnew array<String^>(1000);
            m_nVolume = gcnew array<int>(1000);
            m_strRemark = "";
        };
        ~CGroupOrder(){};

        CAlgorithmOrder^   m_orderParam;     //下单配置
        array<String^>^    m_strMarket;      //市场列表
        array<String^>^    m_strInstrument;  //证券代码
        array<int>^                m_nVolume;        //每只股票的下单量
        int                m_nOrderNum;      //股票只数
        String^      m_strRemark;       //投资备注
    };

    public ref struct COrdinaryGroupOrder
    {
        COrdinaryGroupOrder()
        {
            m_strAccountID = "";
            m_dSuperPriceRate = 0.0;
            m_ePriceType = EPriceType::PRTP_INVALID;
            m_eHedgeFlag = EHedgeFlagType::HEDGE_FLAG_SPECULATION;
            m_eOverFreqOrderMode = EXtOverFreqOrderMode::OFQ_FORBID;
            m_eTimeCondition = ETimeCondition::TIME_CONDITION_GFD;
            m_eVolumeCondition = EVolumeCondition::VOLUME_CONDITION_ANY;
            m_strMarket = gcnew array<String^>(1000);
            m_strInstrument = gcnew array<String^>(1000);
            m_nVolume = gcnew array<int>(1000);
            m_dPrice = gcnew array<double>(1000);
            m_eOperationType = gcnew array<EOperationType>(1000);
            m_nOrderNum = 0;
            m_strRemark = "";
            m_dSuperPrice = 0.0;
        }
        ~COrdinaryGroupOrder(){};
        String^  m_strAccountID;      // 资金账户ID，如果为子账户，则为子账户ID
        double  m_dSuperPriceRate;       // 单笔超价百分比
        EPriceType  m_ePriceType;            // 报价方式： 指定价，最新价 对手价……
        EHedgeFlagType  m_eHedgeFlag;            // 套利标志
        EXtOverFreqOrderMode  m_eOverFreqOrderMode;  //委托频率过快时的处理方式
        ETimeCondition m_eTimeCondition; //期货条件单时间条件
        EVolumeCondition m_eVolumeCondition; //期货条件单数量条件
        array<String^>^  m_strMarket;         // 合约市场
        array<String^>^  m_strInstrument;     // 委托合约.
        array<int>^  m_nVolume;               // 委托量, 直接还券的数量
        array<double>^  m_dPrice;                // 指定价，仅在报价方式为PRTP_FIX(指定价)时有效;
        array<EOperationType>^  m_eOperationType;        // 下单类型，开、平、买、卖…
        int  m_nOrderNum;               // 股票只数
        String^      m_strRemark;       //投资备注
        double  m_dSuperPrice;       // 单笔超价,和m_dSuperPriceRate只用设置一个，优先使用m_dSuperPriceRate
    };

    ///< 智能算法单下单参数
    public ref struct CIntelligentAlgorithmOrder
    {

        CIntelligentAlgorithmOrder()
        {
            m_strAccountID = "";
            m_strMarket = "";
            m_strInstrument = "";
            m_strOrderType = "";                             //算法名称
            m_dPrice = 0;
            m_nVolume = 0;
            m_nValidTimeStart = INT_MAX;
            m_nValidTimeEnd = INT_MAX;
            m_dMaxPartRate = 1;
            m_dMinAmountPerOrder = 0;
            m_eOperationType = EOperationType::OPT_INVALID;
            m_ePriceType = EPriceType::PRTP_INVALID;
            m_strRemark = "";
            m_dOrderRateInOpenAcution = 0;
            m_dPriceOffsetBpsForAuction = 0;
            m_nStopTradeForOwnHiLow = EStopTradeForOwnHiLow::STOPTRADE_NONE;
            m_bOnlySellAmountUsed = 0;
            m_dBuySellAmountDeltaPct = 1;
            m_nMaxTradeDurationAfterET = 0;
            m_eOrderStrategyType = EOrderStrategyType::E_ORDER_STRATEGY_TYPE_NORMAL;
            m_strStrategyID = "";
            m_eHedgeFlag = EHedgeFlagType::HEDGE_FLAG_SPECULATION;
            m_eTriggerType = EOpTriggerType::OTT_NONE;
            m_dTriggerPrice = 0.0;
            m_eUndealtEntrustRule = EPriceType::PRTP_INVALID;

            m_nLimitedPriceType = 0;
            m_strOtherParam = "";
            m_eCmdDateLimit = EXTCommandDateLimit::XT_COMMAND_LIMIT_NO_OVER_DAY;
            m_nTimeType = 0;
            m_nTimeValue = 0;
            m_strRemark1 = "";
            m_nOpenTrade = 0;
            m_dCancelRateThreshold = 1;
        };
        ~CIntelligentAlgorithmOrder() {};
        String^ m_strAccountID;                                 ///< 账号
        String^ m_strMarket;                                    ///< 市场
        String^ m_strInstrument;                                ///< 合约
        String^ m_strOrderType;                                 ///< 算法名称，VWAP，TWAP，VP，PINLINE，DMA，FLOAT，MSO，SWITCH，ICEBERG，MOC，GRID，VWAPPLUS，MOO，IS，STWAP，SLOS，VPPLUS，XTFAST，SLOH，MOOPLUS，IVWAP，VWAPPLUS2
        double                  m_dPrice;                       ///< 基准价
        int                     m_nVolume;                      ///< 下单总量
        int                     m_nValidTimeStart;              ///< 有效开始时间 
        int                     m_nValidTimeEnd;                ///< 有效结束时间 
        double                  m_dMaxPartRate;                 ///< 量比比例, 用户设定, 当MaxPartRate==100%, 表示没有限制
        double                  m_dMinAmountPerOrder;           ///< 委托最小金额
        EOperationType          m_eOperationType;               ///< 下单操作：买入卖出
        EPriceType              m_ePriceType;                   ///< 报价方式：市价和指定价
        String^ m_strRemark;               ///< 投资备注
        double                  m_dOrderRateInOpenAcution;      ///< 开盘集合竞价参与比例(取值0-1) 仅开盘+算法有用
        int                     m_dPriceOffsetBpsForAuction;    ///< 开盘集合竞价价格偏移量(取值0-10000) 仅开盘+算法有用
        EStopTradeForOwnHiLow   m_nStopTradeForOwnHiLow;        ///< 涨跌停控制
        bool                    m_bOnlySellAmountUsed;          ///< 仅用卖出金额  0,1  换仓特有
        double                  m_dBuySellAmountDeltaPct;       ///< 买卖偏差上限0.03-1  换仓特有
        int                     m_nMaxTradeDurationAfterET;     ///< 过期后是否继续执行， 0不继续，非0继续
        EOrderStrategyType      m_eOrderStrategyType;           ///< 算法下单方式
        String^ m_strStrategyID;                                ///< 收益互换策略ID
        EHedgeFlagType          m_eHedgeFlag;                   ///< 套利标志
        EOpTriggerType          m_eTriggerType;                 ///< 触价类型
        double                  m_dTriggerPrice;                ///< 触价价格

        int                     m_nLimitedPriceType;            ///< 条件单价格限制类型
        String^ m_strOtherParam;                                ///< 条件单其他参数
        EXTCommandDateLimit     m_eCmdDateLimit;                ///< 指令跨日开关
        int                     m_nTimeType;                    ///< 时间类型，0，按区间，1，按执行时间， 默认0
        int                     m_nTimeValue;                   ///< 执行时间
        String^ m_strRemark1;                                   ///< 投资备注1
        int                     m_nOpenTrade;                   ///< 开盘集合竞价, 0，不参与，1，参与， 默认0
        EPriceType              m_eUndealtEntrustRule;          ///< 未成委托处理
        double                  m_dCancelRateThreshold;         ///< 撤单率(取值0-1) 

    };

    ///< 外部算法单下单参数
    public ref struct CExternAlgorithmOrder
    {

        CExternAlgorithmOrder()
        {
            m_strAccountID = "";
            m_strMarket = "";
            m_strInstrument = "";
            m_strOrderType = "";                             //算法名称
            m_dPrice = 0;
            m_nVolume = 0;
            m_nValidTimeStart = 0;
            m_nValidTimeEnd = 0;
            m_dMaxPartRate = 1;
            m_dMinAmountPerOrder = 0;
            m_eOperationType = EOperationType::OPT_INVALID;
            m_strRemark = "";
            m_nStopTradeForOwnHiLow = EStopTradeForOwnHiLow::STOPTRADE_NONE;
            m_eOrderStrategyType = EOrderStrategyType::E_ORDER_STRATEGY_TYPE_NORMAL;
            m_dAvailable = Double::MaxValue;
            m_nMaxTradeDurationAfterET = 0;
            m_strStrategyID = "";
        };

        ~CExternAlgorithmOrder() {};
        String^                 m_strAccountID;             ///< 账号
        String^                 m_strMarket;                ///< 市场
        String^                 m_strInstrument;            ///< 合约
        String^                 m_strOrderType;             ///< 算法名称，FTAIWAP，ALGOINTERFACE, ZEUS....
        double                  m_dPrice;                   ///< 基准价
        int                     m_nVolume;                  ///< 下单总量
        int                     m_nValidTimeStart;          ///< 有效开始时间 
        int                     m_nValidTimeEnd;            ///< 有效结束时间 
        double                  m_dMaxPartRate;             ///< 量比比例, 用户设定, 当MaxPartRate==100%, 表示没有限制
        double                  m_dMinAmountPerOrder;       ///< 委托最小金额
        EOperationType          m_eOperationType;           ///< 下单操作：买入卖出
        String^                 m_strRemark;                ///< 投资备注
        EStopTradeForOwnHiLow   m_nStopTradeForOwnHiLow;    ///< 涨跌停控制
        EOrderStrategyType      m_eOrderStrategyType;       ///< 算法下单方式
        double                  m_dAvailable;               ///< t0策略最大可用资金
        int                     m_nMaxTradeDurationAfterET; ///< 过期后是否继续执行， 0不继续，非0继续
        String^                 m_strStrategyID;            ///< 收益互换策略ID
    };


    ///< 华创算法单下单参数
    public ref struct CHuaChuangAlgorithmOrder
    {

        CHuaChuangAlgorithmOrder()
        {
            m_strAccountID = "";
            m_strMarket = "";
            m_strInstrument = "";
            m_strOrderType = "";                             //算法名称
            m_dPrice = 0;
            m_nVolume = INT_MAX;
            m_eOperationType = EOperationType::OPT_INVALID;
            m_eOrderStrategyType = EOrderStrategyType::E_ORDER_STRATEGY_TYPE_NORMAL;
            m_strTimeStart = "";
            m_strTimeEnd = "";
            m_dMaxMarketRate = 0.0;
            m_nFixRate = 0;
            m_nExecuteOffset = 2;
            m_dMinQuantityRate = 0.0;
            m_nReferencePrice = 0;
            m_nInOpenAcution = 0;
            m_dInCloseAcution = 0;
            m_nSingleVolume = 0;
            m_strRemark = "";
            m_strRemark1 = "";
            m_nLimitedPriceType = 0;
            m_ePriceType = EPriceType::PRTP_FIX;
            m_dMaxPartRate = 1;
            m_dMinAmountPerOrder = 0;
            m_strOtherParam = "";
        };

        ~CHuaChuangAlgorithmOrder() {};
        String^                 m_strAccountID;         ///< 账号
        String^                 m_strMarket;            ///< 市场
        String^                 m_strInstrument;        ///< 合约
        String^                 m_strOrderType;         ///< 算法名称，FTAIWAP，ALGOINTERFACE, ZEUS....
        double                  m_dPrice;                   ///< 基准价
        int                     m_nVolume;                  ///< 下单总量
        EOperationType          m_eOperationType;           ///< 下单操作：买入卖出
        EOrderStrategyType      m_eOrderStrategyType;       ///< 算法下单方式
        String^ m_strTimeStart;       ///< 开始时间，格式yyyyMMdd-HH:mm:ss.fff  默认当日开盘时间
        String^ m_strTimeEnd;       ///< 结束时间，格式yyyyMMdd-HH:mm:ss.fff  默认当日收盘时间
        double                  m_dMaxMarketRate;           ///< 最大市场占比  0.00-100.00
        int                     m_nFixRate;                 ///< 限价内占比  1 是， 0 否，默认0
        int                     m_nExecuteOffset;           ///< 执行偏移量  1 低,2 中,3 高，默认2
        double                  m_dMinQuantityRate;         ///< 最小跟量比例 ，默认0
        int                     m_nReferencePrice;          ///< 参考价格 1日内均价,2交易时段均价,3最新价,4开盘价,5昨日收盘价，默认1
        int                     m_nInOpenAcution;           ///< 参与开盘竞价 1 是， 0 否，默认0
        int                     m_dInCloseAcution;          ///< 参与收盘竞价 1 是， 0 否，默认0
        int                     m_nSingleVolume;            ///< 单次委托量 0-1000000，默认0
        String^ m_strRemark;           ///< 投资备注
        String^ m_strRemark1;          ///< 投资备注1
        int                     m_nLimitedPriceType;        ///< 价格限制类型
        EPriceType  m_ePriceType;            // 报价方式： 指定价，最新价 对手价……
        double                  m_dMaxPartRate;             ///< 量比比例, 用户设定, 当MaxPartRate==100%, 表示没有限制
        double                  m_dMinAmountPerOrder;       ///< 委托最小金额
        String^                 m_strOtherParam;            ///< 华创算法额外扩展参数

    };

    ///< 华创算法组合单下单参数
    public ref struct CHuaChuangAlgoGroupOrder
    {
        CHuaChuangAlgoGroupOrder()
        {
            m_orderParam = gcnew CHuaChuangAlgorithmOrder();
            m_strMarket = gcnew array<String^>(1000);
            m_strInstrument = gcnew array<String^>(1000);
            m_nVolume = gcnew array<int>(1000);
            m_dPrice = gcnew array<double>(1000);
            m_eOperationType = gcnew array<EOperationType>(1000);
            m_nOrderNum = INT_MAX;
        };
        ~CHuaChuangAlgoGroupOrder() {};

        CHuaChuangAlgorithmOrder^ m_orderParam;        ///< 下单配置
        array<String^>^ m_strMarket;                ///< 市场列表
        array<String^>^ m_strInstrument;            ///< 证券代码
        array<int>^ m_nVolume;                      ///< 每只股票的下单量
        array<double>^ m_dPrice;                    ///< 每只股票的基准价，限价必填，市价不填
        array<EOperationType>^ m_eOperationType;    ///< 每只股票的下单类型
        int m_nOrderNum;                            ///< 股票只数
    };


    ///< 智能算法组合单下单参数
    public ref struct CAlgGroupOrder
    {
        CAlgGroupOrder()
        {
            m_orderParam = gcnew CIntelligentAlgorithmOrder();
            m_strMarket = gcnew array<String^>(1000);
            m_strInstrument = gcnew array<String^>(1000);
            m_nVolume = gcnew array<int>(1000);
            m_eOperationType = gcnew array<EOperationType>(1000);
            m_strAccountKey = gcnew array<String^>(1000);
            m_dMaxPartRate = gcnew array<double>(1000);
            m_nOrderNum = INT_MAX;
            m_strRemark = "";
        };
        ~CAlgGroupOrder() {};

        CIntelligentAlgorithmOrder^ m_orderParam;   ///< 下单配置
        array<String^>^ m_strMarket;                ///< 市场列表
        array<String^>^ m_strInstrument;            ///< 证券代码
        array<int>^ m_nVolume;                      ///< 每只股票的下单量
        array<EOperationType>^ m_eOperationType;    ///< 每只股票的下单类型
        //组合单兼容多资金账号组合下单功能，如果是单账号组合单，m_strAccountKey可不填，如果是多账号下单，m_strAccountKey必填，否则会导致下单异常
        array<String^>^ m_strAccountKey;            ///< 每个合约的下单资金账号Key
        array<double>^ m_dMaxPartRate;              ///< 量比比例, 用户设定, 当MaxPartRate==100%, 表示没有限制，如果量比比例全都相同可以只填写CIntelligentAlgorithmOrder里面的m_dMaxPartRate
        int m_nOrderNum;                            ///< 股票只数
        String^ m_strRemark;                        ///< 投资备注
    };

    ///< 外部算法组合单下单参数
    public ref struct CExternAlgGroupOrder
    {
        CExternAlgGroupOrder()
        {
            m_orderParam = gcnew CExternAlgorithmOrder();
            m_strMarket = gcnew array<String^>(1000);
            m_strInstrument = gcnew array<String^>(1000);
            m_nVolume = gcnew array<int>(1000);
            m_eOperationType = gcnew array<EOperationType>(1000);
            m_nOrderNum = INT_MAX;
            m_strRemark = "";
        };
        ~CExternAlgGroupOrder() {};

        CExternAlgorithmOrder^ m_orderParam;        ///< 下单配置
        array<String^>^ m_strMarket;                ///< 市场列表
        array<String^>^ m_strInstrument;            ///< 证券代码
        array<int>^ m_nVolume;                      ///< 每只股票的下单量
        array<EOperationType>^ m_eOperationType;    ///< 每只股票的下单类型
        int m_nOrderNum;                            ///< 股票只数
        String^ m_strRemark;                        ///< 投资备注
    };

    public ref struct CInstrumentDetail
    {
        String^          m_strInstrumentID;      //合约代码
        String^          m_strInstrumentName;    //合约名称
        String^          m_strProductID;         //品种代码
        String^          m_strExchangeID;        //交易所代码
        String^          m_strOptUndlCode;       //期权标的代码
        String^          m_strOptUndlName;       //期权标的证券名称
        String^          m_strEndDelivDate;      //最后日期
        double          m_dPriceTick;      //价格波动
        int          m_nOptUnit;      //期权合约单位
        double          m_dMarginUnit;      //保证金单位
        double          m_dUpStopPrice;      //涨停价
        double          m_dDownStopPrice;      //跌停价
        double          m_dSettlementPrice;      //前结算
        double          m_dOptExercisePrice;      //期权行权价格
        int          m_nVolumeMultiple;      //合约乘数
        EXtSuspendedType          m_eSuspendedType;      //停牌状态
        int      m_nCallOrPut;            //合约种类(个股期权：0认购，1认沽)
    };

    public ref struct  CStockOptionCombPositionDetail
    {
        String^        m_strAccountID;         //账号
        String^        m_strExchangeID;        //交易类别
        String^        m_strExchangeName;      //市场名字
        String^        m_strContractAccount;      //合约账号
        String^        m_strCombID;    //组合编号
        String^        m_strCombCode;    //组合策略编码
        String^        m_strCombCodeName;    //组合策略名称
        int           m_nVolume;             //总持仓量
        int           m_nFrozenVolume;              //冻结数量
        int           m_nCanUseVolume;            //可用数量
        String^        m_strFirstCode;      //合约一
        EOptionType   m_eFirstCodeType;      //合约一类型
        String^        m_strFirstCodeName;      //合约一名称
        ESideFlag   m_eFirstCodePosType;      //合约一持仓类型
        int           m_nFirstCodeAmt;            //合约一数量
        String^        m_strSecondCode;      //合约二
        EOptionType   m_eSecondCodeType;      //合约二类型
        String^        m_strSecondCodeName;      //合约二名称
        ESideFlag   m_eSecondCodePosType;    //合约二持仓类型
        int           m_nSecondCodeAmt;            //合约二数量
        double   m_dCombBailBalance; //占用保证金
    };

    public ref struct CSubscribData
    {
        CSubscribData()
        {
            m_nPlatformID = 10001;
            m_strExchangeID = "";
            m_strInstrumentID = "";
            m_eOfferStatus = EXTOfferStatus::XT_OFFER_STATUS_SP;
        };
        ~CSubscribData(){};

        int                   m_nPlatformID;                     //平台ID
        String^           m_strExchangeID;         //市场代码
        String^           m_strInstrumentID;        //合约代码,当其值为allCode时，订阅整个市场
        EXTOfferStatus                m_eOfferStatus;        //报盘状态
    };

    public ref struct CReferenceRate
    {
        CReferenceRate()
        {
            m_strAccountID = "";
            m_strExchangeID = "";
            m_strExchangeName = "";
            m_eMoneyType = EMoneyType::MONEY_TYPE_RMB;
            m_bBidReferenceRate = 0;
            m_bAskReferenceRate = 0;
            m_bBidSettlementRate = 0;
            m_bAskSettlementRate = 0;
            m_dDayBuyRiseRate = 0;
            m_dNightBuyRiseRate = 0;
            m_dDaySaleRiseRate = 0;
            m_dNightSaleRiseRate = 0;
            m_bMidReferenceRate = 0;
        };
        ~CReferenceRate(){};

        String^        m_strAccountID; //账号
        String^        m_strExchangeID; //市场代码
        String^        m_strExchangeName;      //市场名字
        EMoneyType  m_eMoneyType;    //币种
        double      m_bBidReferenceRate;  // 买入参考汇率
        double      m_bAskReferenceRate;  //卖出参考汇率
        double      m_bBidSettlementRate; //买入结算汇率
        double      m_bAskSettlementRate; //卖出结算汇率
        double      m_dDayBuyRiseRate; //日间买入参考汇率浮动比例
        double      m_dNightBuyRiseRate; //夜市买入参考汇率浮动比例
        double      m_dDaySaleRiseRate; //日间卖出参考汇率浮动比例
        double      m_dNightSaleRiseRate; //日间卖出参考汇率浮动比例
        double      m_bMidReferenceRate; //参考汇率中间价
    };

    public ref struct CCreditDetail
    {
        CCreditDetail()
        {
            m_strAccountID = "";
            m_dPerAssurescaleValue = 0.0;
            m_dBalance = 0.0;
            m_dTotalDebt = 0.0;
            m_dAssureAsset = 0.0;
            m_dMarketValue = 0.0;
            m_dEnableBailBalance = 0.0;
            m_dAvailable = 0.0;
            m_dFinDebt = 0.0;
            m_dFinDealAvl = 0.0;
            m_dFinFee = 0.0;
            m_dSloDebt = 0.0;
            m_dSloMarketValue = 0.0;
            m_dSloFee = 0.0;
            m_dOtherFare = 0.0;
            m_dFinMaxQuota = 0.0;
            m_dFinEnableQuota = 0.0;
            m_dFinUsedQuota = 0.0;
            m_dSloMaxQuota = 0.0;
            m_dSloEnableQuota = 0.0;
            m_dSloUsedQuota = 0.0;
            m_dSloSellBalance = 0.0;
            m_dUsedSloSellBalance = 0.0;
            m_dSurplusSloSellBalance = 0.0;
            m_dStockValue = 0.0;
            m_dFundValue = 0.0;
            m_dMaxQuota = 0.0;
            m_dAssureEnbuyBalance = 0.0;
            m_dFetchBalance = 0.0;
            m_dEquityCompensation = 0.0;
            m_dSpecialNetRatio = 0.0;
            m_dStibGemNetRatio = 0.0;
            m_dEnableQuota = 0.0;
        };
        ~CCreditDetail(){};

        String^ m_strAccountID; //账号
        double m_dPerAssurescaleValue; //维持担保比例
        double m_dBalance; //动态权益 即市值
        double m_dTotalDebt; //总负债
        double m_dAssureAsset; //净资产
        double m_dMarketValue; //合约价值
        double m_dEnableBailBalance; //可用保证金
        double m_dAvailable; //可用资金
        double m_dFinDebt; //融资负债
        double m_dFinDealAvl; //融资本金
        double m_dFinFee; //融资息费
        double m_dSloDebt; //融券负债
        double m_dSloMarketValue; //融券市值
        double m_dSloFee; //融券息费
        double m_dOtherFare; //其它费用
        double m_dFinMaxQuota; //融资授信额度
        double m_dFinEnableQuota; //融资可用额度
        double m_dFinUsedQuota; //融资冻结额度
        double m_dSloMaxQuota; //融券授信额度
        double m_dSloEnableQuota; //融券可用额度
        double m_dSloUsedQuota; //融券冻结额度
        double m_dSloSellBalance; //融券卖出资金
        double m_dUsedSloSellBalance; //已用融券卖出资金
        double m_dSurplusSloSellBalance; //剩余融券卖出资金
        double m_dStockValue; //股票总市值，期货没有
        double m_dFundValue; //基金总市值，包括ETF和封闭式基金，期货没有
        double m_dMaxQuota; //总授信额度
        double m_dAssureEnbuyBalance;       ///< 可买担保品资金
        double m_dFetchBalance;             ///< 可取资金
        double m_dEquityCompensation;       ///< 权益补偿资金
        double m_dSpecialNetRatio;          ///< D与E类证券净持仓集中度
        double m_dStibGemNetRatio;          ///< 双创板净持仓集中度
        double m_dEnableQuota;              ///< 可用授信额度
    };

    public ref struct CTaskOpRecord
    {
        CTaskOpRecord()
        {
            m_nCmdId = 10001;
            m_eOperator = ETaskFlowOperation::TFO_RESUME;
            m_strReason = "";
        };
        ~CTaskOpRecord(){};

        int                   m_nCmdId;                     //指令ID
        ETaskFlowOperation                m_eOperator;        //任务操作
        String^           m_strReason;        //操作原因
    };

    public ref struct CSubscribeInfo
    {
        CSubscribeInfo()
        {
            m_strAccountID = "";
            m_strAccountKey = "";
            m_strExchangeID = "";
            m_strInstrumentID = "";
            m_dPurchaseAmount = 0;
            m_dTechPurchaseAmount = 0;
        };
        ~CSubscribeInfo(){};

        String^   m_strAccountID;          ///< 账号
        String^   m_strAccountKey;         ///< 账号key
        String^   m_strExchangeID;         ///< 交易所代码
        String^   m_strInstrumentID;       ///< 合约代码
        int    m_dPurchaseAmount;           ///<可申购额度
        int    m_dTechPurchaseAmount;       ///<科创板可申购额度
    };

    public ref struct CStkUnClosedCompacts
    {
        CStkUnClosedCompacts()
        {
            m_strAccountID = "";
            m_strAccountKey = "";
            m_strExchangeID = "";
            m_strInstrumentID = "";
            m_strCompactId = "";
            m_strEntrustNo = "";
            m_strPositionStr = "";
            m_eCompactType = EXTCompactType::COMPACT_TYPE_ALL;
            m_eCashgroupProp = EXTCompactBrushSource::COMPACT_BRUSH_SOURCE_NORMAL;
            m_nOpenDate = 0;
            m_nBusinessVol = 0;
            m_nRealCompactVol = 0;
            m_nRetEndDate = 0;
            m_dBusinessBalance = 0;
            m_dBusinessFare = 0;
            m_dRealCompactBalance = 0;
            m_dRealCompactFare = 0;
            m_dRepaidFare = 0;
            m_dRepaidBalance = 0;
            m_nRepayPriority = 0;
        };
        ~CStkUnClosedCompacts(){};

        String^                m_strAccountID;          ///< 账号ID
        String^                m_strAccountKey;         ///< 账号key
        String^                m_strExchangeID;         ///< 交易所代码
        String^                m_strInstrumentID;       ///< 合约代码
        EXTCompactType         m_eCompactType;          ///< 合约类型
        EXTCompactBrushSource  m_eCashgroupProp;        ///< 头寸来源
        int                    m_nOpenDate;             ///< 开仓日期
        int                    m_nBusinessVol;          ///< 合约证券数量
        int                    m_nRealCompactVol;       ///< 未还合约数量
        int                    m_nRetEndDate;           ///< 到期日
        double                 m_dBusinessBalance;      ///< 合约金额
        double                 m_dBusinessFare;         ///< 合约息费
        double                 m_dRealCompactBalance;   ///< 未还合约金额
        double                 m_dRealCompactFare;      ///< 未还合约息费
        double                 m_dRepaidFare;           ///< 已还息费
        double                 m_dRepaidBalance;        ///< 已还金额
        String^                m_strCompactId;          ///< 合约编号
        String^                m_strEntrustNo;          ///< 委托编号
        int                    m_nRepayPriority;        ///< 偿还优先级
        String^                m_strPositionStr;        ///< 定位串
    };

    public ref struct CStkClosedCompacts
    {
        CStkClosedCompacts()
        {
            m_strAccountID = "";
            m_strAccountKey = "";
            m_strExchangeID = "";
            m_strInstrumentID = "";
            m_strCompactId = "";
            m_strEntrustNo = "";
            m_strPositionStr = "";
            m_eCompactType = EXTCompactType::COMPACT_TYPE_ALL;
            m_eCashgroupProp = EXTCompactBrushSource::COMPACT_BRUSH_SOURCE_NORMAL;
            m_nOpenDate = 0;
            m_nBusinessVol = 0;
            m_nRetEndDate = 0;
            m_nDateClear = 0;
            m_nEntrustVol = 0;
            m_dEntrustBalance = 0;
            m_dBusinessBalance = 0;
            m_dBusinessFare = 0;
            m_dRepaidFare = 0;
            m_dRepaidBalance = 0;
        };
        ~CStkClosedCompacts(){};

        String^                   m_strAccountID;      ///< 账号ID
        String^                   m_strAccountKey;     ///< 账号key
        String^                   m_strExchangeID;     ///< 交易所代码
        String^                   m_strInstrumentID;   ///< 合约代码
        EXTCompactType         m_eCompactType;          ///< 合约类型
        EXTCompactBrushSource  m_eCashgroupProp;        ///< 头寸来源
        int                    m_nOpenDate;             ///< 开仓日期
        int                    m_nBusinessVol;          ///< 合约证券数量
        int                    m_nRetEndDate;           ///< 到期日
        int                    m_nDateClear;            ///< 了结日期
        int                    m_nEntrustVol;           ///< 委托数量
        double                 m_dEntrustBalance;       ///< 委托金额
        double                 m_dBusinessBalance;      ///< 合约金额
        double                 m_dBusinessFare;         ///< 合约息费
        double                 m_dRepaidFare;           ///< 已还息费
        double                 m_dRepaidBalance;        ///< 已还金额
        String^                   m_strCompactId;      ///< 合约编号
        String^                   m_strEntrustNo;      ///< 委托编号
        String^                   m_strPositionStr;    ///< 定位串
    };

    public ref struct CAccountKey
    {
        CAccountKey()
        {
            m_nPlatformID = 10001;
            m_eBrokerType = EXTBrokerType::AT_STOCK;
            m_nAccountType = 49;
            m_strAccountID = "";
            m_strSubAccount = "";
            m_strAccountKey = "";
        };
        ~CAccountKey(){};

        int                 m_nPlatformID;              ///< 目前主要用于区别不同的行情, 根据此来选择对应行情
        EXTBrokerType       m_eBrokerType;              ///< 券商,经纪公司类别,经纪公司类别,券商
        int                 m_nAccountType;             ///< 账号类型编号
        String^             m_strAccountID;             ///< 资金账号
        String^             m_strSubAccount;            ///< 账号类型
        String^             m_strAccountKey;            ///< 资金账号对应唯一主键
    };

    public ref struct CDeliveryDetail
    {
        CDeliveryDetail()
        {
            m_strAccountID = "";
            m_strAccountKey = "";
            m_nAccountType = 0;
            m_nBizDate = 0;
            m_nBizTime = 0;
            m_strExchangeID = "";
            m_strInstrumentName = "";
            m_strInstrumentID = "";
            m_strInstrumentName = "";
            m_strEntrustBS = "";
            m_strEntrustBSName = "";
            m_dBizAmount = 0.0;
            m_dBizPrice = 0.0;
            m_dBizBalance = 0.0;
            m_strEntrustNo = "";
            m_strBizNo = "";
            m_dCommission = 0.0;
            m_dStampTax = 0.0;
            m_nEntrustDate = 0;
            m_nEntrustTime = 0;
            m_strPositionStr = "";
            m_strMoneyType = "";
            m_strBizName = "";
            m_dTransFee = 0.0;
            m_strStockAccount = "";
            m_dPostBalance = 0.0;
            m_dPostAmount = 0.0;
            m_strContractAccount = "";
            m_strMoneyName = "";
            m_strOpenFlag = "";
            m_strOpenFlagName = "";
            m_strCoveredFlag = "";
            m_strCoveredFlagName = "";
            m_strBizType = "";
            m_strRemark = "";
            m_nClearDate = 0;
            m_nBizFlag = 0;
            m_strCustName = "";
            m_strOrderId = "";
            m_nEntrustAmount = 0;
            m_dEntrustPrice = 0.0;
            m_nbizTimes = 0;
            m_strBizStatus = "";
            m_dFundEffect = 0.0;
            m_dStandardCommission = 0.0;
            m_dShareFee = 0.0;
            m_dTradeFee = 0.0;
            m_dFrontFee = 0.0;
            m_dSysUsageFee = 0.0;
            m_dLevyFee = 0.0;
            m_dSettRate = 0.0;
            m_strDate = "";
            m_StrSettlementInfo = "";
        };
        ~CDeliveryDetail() {};

        String^             m_strAccountID;             ///< 账号ID
        String^             m_strAccountKey;             ///< 账号key
        int                 m_nAccountType;              ///< 账号类型
        int                 m_nBizDate;             ///< 成交日期
        int                 m_nBizTime;             ///< 成交时间
        String^             m_strExchangeID;            ///< 交易所代码
        String^             m_strExchangeName;            ///< 交易所名称
        String^             m_strInstrumentID;            ///< 合约代码
        String^             m_strInstrumentName;            ///< 合约名称
        String^             m_strEntrustBS;            ///< 操作
        String^             m_strEntrustBSName;            ///< 操作名称
        double              m_dBizAmount;       ///< 成交数量
        double              m_dBizPrice;       ///< 成交价格
        double              m_dBizBalance;       ///< 成交金额
        String^             m_strEntrustNo;            ///< 委托号
        String^             m_strBizNo;            ///< 成交序号
        double              m_dCommission;       ///< 手续费
        double              m_dStampTax;       ///< 印花税
        int                 m_nEntrustDate;             ///< 委托日期  股票期权和港股特有
        int                 m_nEntrustTime;             ///< 委托时间  股票期权和港股特有
        String^             m_strPositionStr;            ///< 记录序列号  股票期权和港股特有
        String^             m_strMoneyType;            ///< 币种类型  股票期权和港股特有
        String^             m_strBizName;            ///< 业务类型  股票期权和港股特有
        double              m_dTransFee;       ///< 业务类型  股票期权和港股特有
        String^             m_strStockAccount;            ///< 股东账号  股票和港股特有
        double              m_dPostBalance;       ///< 资金余额  股票和港股特有
        double              m_dPostAmount;       ///< 股份余额  股票和港股特有
        String^             m_strContractAccount;            ///< 合约账号  股票期权特有
        String^             m_strMoneyName;            ///< 币种  股票期权特有
        String^             m_strOpenFlag;            ///< 开平标识  股票期权特有
        String^             m_strOpenFlagName;            ///< 开平标识名称  股票期权特有
        String^             m_strCoveredFlag;            ///< 备兑标记  股票期权特有
        String^             m_strCoveredFlagName;            ///< 备兑标记名称  股票期权特有
        String^             m_strBizType;            ///< 成交类型  股票期权特有
        String^             m_strRemark;            ///< 备注  股票期权特有
        int                 m_nClearDate;             ///< 清算日期  港股特有
        int                 m_nBizFlag;             ///< 清算日期  港股特有
        String^             m_strCustName;            ///< 客户姓名  港股特有
        String^             m_strOrderId;            ///< 合同序号  港股特有
        int                 m_nEntrustAmount;             ///< 委托数量  港股特有
        double              m_dEntrustPrice;       ///< 委托价格  港股特有
        int                 m_nbizTimes;             ///< 成交笔数  港股特有
        String^             m_strBizStatus;            ///< 成交状态  港股特有
        double              m_dFundEffect;       ///< 清算金额  港股特有
        double              m_dStandardCommission;       ///< 标准手续费  港股特有
        double              m_dShareFee;       ///< 股份交收费  港股特有
        double              m_dTradeFee;       ///< 交易费  港股特有
        double              m_dFrontFee;       ///< 前台费用  港股特有
        double              m_dSysUsageFee;       ///< 交易系统使用费用  港股特有
        double              m_dLevyFee;       ///< 交易征费  港股特有
        double              m_dSettRate;       ///< 结算汇率  港股特有
        String^             m_strDate;            ///< 结算单日期  期货和期货期权特有
        String^             m_StrSettlementInfo;            ///< 结算单日期  期货和期货期权特有
    };

    public ref struct CExchangeStatus
    {
        CExchangeStatus()
        {
            m_strExchangeId = "";
            m_strProductId = "";
            m_strInstrumentId = "";
            m_strEnterTime = "";
            m_strEnterReason = "";
            m_eInstrumentStatus = EXTExchangeStatus::EXCHANGE_STATUS_INVALID;
            m_nExchangeTimeDelta = 0;
        };
        ~CExchangeStatus() {};

        String^             m_strExchangeId;           ///< 交易所代码
        String^             m_strProductId;            ///< 合约品种
        String^             m_strInstrumentId;         ///< 合约代码
        String^             m_strEnterTime;            ///< 进入本状态时间
        String^             m_strEnterReason;          ///< 进入本状态原因
        EXTExchangeStatus   m_eInstrumentStatus;       ///< 市场状态
        int                 m_nExchangeTimeDelta;      ///< 交易所时间相对于服务器时间的时间差
    };

    public ref struct CInstrumentInfo
    {
        CInstrumentInfo()
        {
            m_strInstrumentID = "";
            m_strInstrumentName = "";
            m_strExchangeID = "";
            m_strExchangeInstID = "";
            m_strProductID = "";
            m_strCreateDate = "";
            m_strOpenDate = "";
            m_strExpireDate = "";
            m_strStartDelivDate = "";
            m_strEndDelivDate = "";
            m_strOptUndlCode = "";
            m_strOptUndlMarket = "";
            m_eProductClass = EProductClass::PRODECT_CLASS_NORMAL;
            m_nDeliveryYear = 0;
            m_nDeliveryMonth = 0;
            m_nMaxMarketOrderVolume = 0;
            m_nMinMarketOrderVolume = 0;
            m_nMaxLimitOrderVolume = 0;
            m_nMinLimitOrderVolume = 0;
            m_nVolumeMultiple = 0;
            m_nIsTrading = 0;
            m_dPriceTick = 0.0;
            m_dLongMarginRatio = 0.0;
            m_dShortMarginRatio = 0.0;
            m_dUpStopPrice = 0.0;
            m_dDownStopPrice = 0.0;
            m_dSettlementPrice = 0.0;
            m_dOptExercisePrice = 0.0;
            m_eMaxMarginSideAlgorithm = EXtMaxMarginSideAlgorithmType::XT_FTDC_MMSA_NO;
            m_eSuspendedType = EXtSuspendedType::XT_NO_SUSPENDED;
            m_nCallOrPut = 0;
        };
        ~CInstrumentInfo() {};

        String^                         m_strInstrumentID;              ///< 合约代码
        String^                         m_strInstrumentName;            ///< 合约名称
        String^                         m_strExchangeID;                ///< 交易所代码
        String^                         m_strExchangeInstID;            ///< 合约在交易所的代码
        String^                         m_strProductID;                 ///< 品种代码
        String^                         m_strCreateDate;                ///< 创建日
        String^                         m_strOpenDate;                  ///< 上市日
        String^                         m_strExpireDate;                ///< 到期日
        String^                         m_strStartDelivDate;            ///< 开始交割日
        String^                         m_strEndDelivDate;              ///< 结束交割日
        String^                         m_strOptUndlCode;               ///< 期权标的代码
        String^                         m_strOptUndlMarket;             ///< 期权标的市场
        EProductClass                   m_eProductClass;                ///< 合约类型
        int                             m_nDeliveryYear;                ///< 交割年份
        int                             m_nDeliveryMonth;               ///< 交割月
        int                             m_nMaxMarketOrderVolume;        ///< 市价单最大下单量
        int                             m_nMinMarketOrderVolume;        ///< 市价单最小下单量
        int                             m_nMaxLimitOrderVolume;         ///< 限价单最大下单量
        int                             m_nMinLimitOrderVolume;         ///< 限价单最小下单量
        int                             m_nVolumeMultiple;              ///< 合约数量乘数
        int                             m_nIsTrading;                   ///< 当前是否交易
        double                          m_dPriceTick;                   ///< 最小变动价位
        double                          m_dLongMarginRatio;             ///< 多头保证金率
        double                          m_dShortMarginRatio;            ///< 空头保证金率
        double                          m_dUpStopPrice;                 ///< 涨停价
        double                          m_dDownStopPrice;               ///< 跌停价
        double                          m_dSettlementPrice;             ///< 前结算
        EXtMaxMarginSideAlgorithmType   m_eMaxMarginSideAlgorithm;      ///< 是否使用大额单边保证金算法
        EXtSuspendedType                m_eSuspendedType;               ///< 停牌状态
        EXtExDivdendType                m_eExDivdendType;               ///< 除权除息标志
        double                          m_dOptExercisePrice;             ///< 期权行权价
        int                             m_nCallOrPut;                   ///< 合约种类(个股期权：0认购，1认沽)
    };

    public ref struct COpVolumeReq
    {
        COpVolumeReq()
        {
            m_strAccountID = "";
            m_strMarket = "";
            m_strInstrument = "";
            m_dPrice = 0.0;
            m_eOperationType = EOperationType::OPT_INVALID;
        };
        ~COpVolumeReq() {};

        String^             m_strAccountID;         ///< 资金账户
        String^             m_strMarket;            ///< 合约市场
        String^             m_strInstrument;        ///< 委托合约
        double              m_dPrice;               ///< 价格
        EOperationType     m_eOperationType;        ///< 下单类型
    };

    public ref struct CCreditAssure
    {
        CCreditAssure()
        {
            m_strAccountID = "";
            m_strExchangeID = "";
            m_strInstrumentID = "";
            m_dAssureRatio = 0.0;
            m_eAssureStatus = EXTSubjectsStatus::SUBJECTS_STATUS_NOT;
        };
        ~CCreditAssure() {};

        String^                 m_strAccountID;             ///< 账号
        String^                 m_strExchangeID;            ///< 市场
        String^                 m_strInstrumentID;          ///< 合约
        double                  m_dAssureRatio;             ///< 担保品折算比例
        EXTSubjectsStatus       m_eAssureStatus;            ///< 是否可做担保
    };

    public ref struct CCreditSubjects
    {
        CCreditSubjects()
        {
            m_strAccountID = "";
            m_strExchangeID = "";
            m_strInstrumentID = "";
            m_dSloRatio = 0.0;
            m_eSloStatus = EXTSubjectsStatus::SUBJECTS_STATUS_NOT;
            m_dFinRatio = 0.0;
            m_eFinStatus = EXTSubjectsStatus::SUBJECTS_STATUS_NOT;
        };
        ~CCreditSubjects() {};

        String^             m_strAccountID;         ///< 账号
        String^             m_strExchangeID;        ///< 市场
        String^             m_strInstrumentID;      ///< 合约
        double              m_dSloRatio;            ///< 融资融券保证金比例
        EXTSubjectsStatus   m_eSloStatus;           ///< 融券状态
        double              m_dFinRatio;            ///< 融资保证金比例
        EXTSubjectsStatus   m_eFinStatus;           ///< 融资状态
    };

    public ref struct CCreditSloCode
    {
        CCreditSloCode()
        {
            m_strAccountID = "";
            m_strExchangeID = "";
            m_strInstrumentID = "";
            m_nEnableAmount = 0;
            m_eCashgroupProp = EXTCompactBrushSource::COMPACT_BRUSH_SOURCE_ALL;
        };
        ~CCreditSloCode() {};

        String^                 m_strAccountID;         ///< 账号
        String^                 m_strExchangeID;        ///< 市场
        String^                 m_strInstrumentID;      ///< 合约
        int                     m_nEnableAmount;        ///< 融券可融数量
        EXTCompactBrushSource   m_eCashgroupProp;       ///< 头寸来源
    };

    public ref struct CQueryBankInfo
    {
        CQueryBankInfo()
        {
            m_strAccountID = "";
            m_strAccountKey = "";
            m_strBankNo = "";
            m_strBankAccount = "";
            m_eMoneyType = EMoneyType::MONEY_TYPE_RMB;
            m_strBankName = "";
        };
        ~CQueryBankInfo() {};

        String^                 m_strAccountID;         ///< 资金账户ID
        String^                 m_strAccountKey;        ///< 账号key
        String^                 m_strBankNo;            ///< 银行代码
        String^                 m_strBankAccount;       ///< 银行账号
        EMoneyType              m_eMoneyType;           ///< 币种
        String^                 m_strBankName;          ///< 银行名称，查询时可不送
    };

    public ref struct CQueryBankAmount
    {
        CQueryBankAmount()
        {
            m_strAccountID = "";
            m_strAccountKey = "";
            m_strBankAccount = "";
            m_eMoneyType = EMoneyType::MONEY_TYPE_RMB;
            m_dBalance = 0.0;
            m_dEnableBalance = 0.0;
        };
        ~CQueryBankAmount() {};

        String^                 m_strAccountID;         ///< 资金账户ID
        String^                 m_strAccountKey;        ///< 账号key
        String^                 m_strBankAccount;       ///< 银行账号
        EMoneyType              m_eMoneyType;           ///< 币种
        double                  m_dBalance;             ///< 银行余额
        double                  m_dEnableBalance;       ///< 可转金额
    };

    public ref struct CTransferReq
    {
        CTransferReq()
        {
            m_strAccountID = "";
            m_strBankNo = "";
            m_strBankAccount = "";
            m_strFundPwd = "";
            m_eMoneyType = EMoneyType::MONEY_TYPE_RMB;
            m_eTransDirection = ETransDirection::TRANS_DIRECTION_QUERY;
            m_dOccurBalance = 0.0;
        };
        ~CTransferReq() {};

        String^                 m_strAccountID;         ///< 资金账户ID
        String^                 m_strBankNo;            ///< 银行代码
        String^                 m_strBankAccount;       ///< 银行账号
        String^                 m_strFundPwd;           ///< 资金密码
        EMoneyType              m_eMoneyType;           ///< 币种
        ETransDirection         m_eTransDirection;      ///< 银证转账方向
        double                  m_dOccurBalance;        ///< 转账金额
    };

    public ref struct CTransferSerial
    {
        CTransferSerial()
        {
            m_strAccountID = "";
            m_strAccountKey = "";
            m_strTransferDate = "";
            m_strTransferTime = "";
            m_eMoneyType = EMoneyType::MONEY_TYPE_RMB;
            m_strTransferNo = "";
            m_eTransDirection = ETransDirection::TRANS_DIRECTION_QUERY;
            m_dTransferBalance = 0.0;
            m_strBankAccount = "";
            m_strBankName = "";
            m_strBankNo = "";
            m_strRemark = "";
        };
        ~CTransferSerial() {};

        String^                 m_strAccountID;         ///< 资金账户ID
        String^                 m_strAccountKey;            ///< 账号key
        String^                 m_strTransferDate;       ///< 转账日期
        String^                 m_strTransferTime;           ///< 转账时间
        EMoneyType              m_eMoneyType;           ///< 币种
        String^                 m_strTransferNo;           ///< 流水号
        ETransDirection         m_eTransDirection;      ///< 银证转账方向
        double                  m_dTransferBalance;        ///< 转账金额
        String^                 m_strBankAccount;           ///< 银行账号
        String^                 m_strBankName;           ///< 银行名称
        String^                 m_strBankNo;           ///< 银行代码
        String^                 m_strRemark;           ///< 备注
    };

    public ref struct CSecuFundTransferReq
    {
        CSecuFundTransferReq()
        {
            m_strAccountID = "";
            m_strExchangeID = "";
            m_strInstrumentID = "";
            m_nOccurAmount = 0;
            m_eCredttransType = ETransTypeCreditFlag::TRANS_TRANSFER_SHARE;
            m_eTransDirection = ESecuFundTransDirection::SECUFUNDTRANS_TRANSFER_NORMAL_TO_FAST;
            m_dOccurBalance = 0.0;
        };
        ~CSecuFundTransferReq() {};

        String^                 m_strAccountID;         ///< 资金账户ID
        String^                 m_strExchangeID;        ///< 股份划拨市场
        String^                 m_strInstrumentID;      ///< 股份划拨合约
        int                     m_nOccurAmount;         ///< 股份划拨数量
        ETransTypeCreditFlag    m_eCredttransType;      ///< 股份划拨信用调拨类别
        ESecuFundTransDirection m_eTransDirection;      ///< 划拨方向
        double                  m_dOccurBalance;        ///< 资金划拨金额
    };

    public ref struct CStockComFund
    {
        CStockComFund()
        {
            m_strAccountID = "";
            m_strAccountKey = "";
            m_dAvailable = 0.0;
        };
        ~CStockComFund() {};

        String^                 m_strAccountID;         ///< 资金账户ID
        String^                 m_strAccountKey;        ///< 账号key
        double                  m_dAvailable;           ///< 可用资金
    };

    public ref struct CStockComPosition
    {
        CStockComPosition()
        {
            m_strAccountID = "";
            m_strAccountKey = "";
            m_strExchangeID = "";
            m_strInstrumentID = "";
            m_strInstrumentName = "";
            m_nVolume = 0;
            m_nCanUseVolume = 0;
            m_dLastPrice = 0.0;
            m_dCostPrice = 0.0;
            m_dIncome = 0.0;
            m_dIncomeRate = 0.0;
            m_strHandFlag = "";
            m_strStockAccount = "";
            m_dInstrumentValue = 0.0;
            m_dCostBalance = 0.0;
            m_nOnRoadVolume = 0;
            m_nPREnableVolume = 0;
            m_bFast = false;
        };
        ~CStockComPosition() {};

        String^                 m_strAccountID;         ///< 资金账户ID
        String^                 m_strAccountKey;        ///< 账号key
        String^                 m_strExchangeID;        ///< 市场代码
        String^                 m_strInstrumentID;      ///< 合约代码
        String^                 m_strInstrumentName;    ///< 合约名称
        int                     m_nVolume;              ///< 持仓量
        int                     m_nCanUseVolume;        ///< 可用数量
        double                  m_dLastPrice;           ///< 最新价
        double                  m_dCostPrice;           ///< 成本价
        double                  m_dIncome;              ///< 盈亏
        double                  m_dIncomeRate;          ///< 盈亏比例
        String^                 m_strHandFlag;          ///< 股手标记
        String^                 m_strStockAccount;      ///< 证券账号
        double                  m_dInstrumentValue;     ///< 市值
        double                  m_dCostBalance;         ///< 成本总额
        int                     m_nOnRoadVolume;        ///< 在途量
        int                     m_nPREnableVolume;      ///< 申赎可用量
        bool                    m_bFast;                ///<是否是从极速接口查到的
    };

    public ref struct CNewPortfolioReq
    {
        CNewPortfolioReq()
        {
            m_strName = "";
            m_strStrategy = "";
            m_strRemark = "";
            m_strAccountKey = "";
            m_nProductID = 0;
            m_dRawBalance = 0.0;
        };
        ~CNewPortfolioReq() {};

        String^                 m_strName;          ///< 投资组合名称
        String^                 m_strStrategy;      ///< 策略名称
        String^                 m_strRemark;        ///< 备注
        String^                 m_strAccountKey;    ///< 账号key
        int                     m_nProductID;       ///< 产品编号
        double                  m_dRawBalance;      ///< 初始资产
    };

    public ref struct CPortfolioInfo
    {
        CPortfolioInfo()
        {
            m_nPortfolioID = -1;
            m_strName = "";
            m_strStrategy = "";
            m_strRemark = "";
            m_strAccountKey = "";
            m_nProductID = 0;
            m_nCreateDate = 0;
            m_nUserId = 0;
            m_nStatus = 0;
            m_dInitBalance = 0.0;
            m_eType = EPortfolioType::PF_TYPE_NORMAL;
        };
        ~CPortfolioInfo() {};

        int                     m_nPortfolioID;     ///< 投组类型编号
        String^                 m_strName;          ///< 投资组合名称
        String^                 m_strStrategy;      ///< 策略名称
        String^                 m_strRemark;        ///< 备注
        String^                 m_strAccountKey;    ///< 账号key
        int                     m_nProductID;       ///< 产品编号
        int                     m_nCreateDate;      ///< 创建日期
        int                     m_nUserId;          ///< 用户编号
        int                     m_nStatus;          ///< 投资组合停用状态
        double                  m_dInitBalance;     ///< 初始资产
        EPortfolioType          m_eType;            ///< 投组类型
    };

    public ref struct CStrategyInfo
    {
        CStrategyInfo()
        {
            m_strStrategyID = "";
            m_strstrategyName = "";
            m_strAccountKey = "";
        };
        ~CStrategyInfo() {};

        String^                 m_strStrategyID;        ///< 收益互换策略ID
        String^                 m_strstrategyName;      ///< 策略名称
        String^                 m_strAccountKey;        ///< 账号key
    };

    public ref struct CSecuAccount
    {
        CSecuAccount()
        {
            m_strExchangeID = "";
            m_strSecuAccount = "";
            m_eMainFlag = EMainFlag::MAIN_FLAG_MAIN;
        };
        ~CSecuAccount() {};

        String^                 m_strExchangeID;        ///< 市场代码
        String^                 m_strSecuAccount;       ///< 股东号
        EMainFlag               m_eMainFlag;            ///< 主副标记
    };
}

#endif
