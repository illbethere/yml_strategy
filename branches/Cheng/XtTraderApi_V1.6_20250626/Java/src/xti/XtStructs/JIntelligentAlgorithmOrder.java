/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JIntelligentAlgorithmOrder.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/
package xti.XtStructs;

import xti.XtDataType.EHedgeFlagType;
import xti.XtDataType.EOperationType;
import xti.XtDataType.EPriceType;
import xti.XtDataType.EStopTradeForOwnHiLow;
import xti.XtDataType.EOrderStrategyType;
import xti.XtDataType.EOpTriggerType;

/**
* JIntelligentAlgorithmOrder类
* 智能算法单下单请求数据
*/
public class JIntelligentAlgorithmOrder{
    /**
    * 资金账号ID
    */
    public String m_strAccountID;
    /**
    * 市场
    */
    public String m_strMarket;
    /**
    * 合约
    */
    public String m_strInstrument;
    /**
    * 算法名称
    */
    public String m_strOrderType;
    /**
    * 下单价格
    */
    public double m_dPrice;
    /**
    * 下单总量
    */
    public int m_nVolume;
    /**
    * 有效开始时间
    */
    public int m_nValidTimeStart;
    /**
    * 有效结束时间
    */
    public int m_nValidTimeEnd;
    /**
    * 量比比例
    */
    public double m_dMaxPartRate;
    /**
    * 委托最小金额
    */
    public double m_dMinAmountPerOrder;
    /**
    * 下单操作：开平、多空……
    */
    public EOperationType m_eOperationType;
    /**
    * 报价方式：对手、最新……
    */
    public EPriceType m_ePriceType;
    /**
    * 投资备注
    */
    public String m_strRemark;
    /**
    * 开盘集合竞价参与比例(取值0-1) 仅开盘+算法有用
    */
    public double m_dOrderRateInOpenAcution;
    /**
    * 开盘集合竞价价格偏移量(取值0-10000) 仅开盘+算法有用
    */
    public int m_dPriceOffsetBpsForAuction;
    /**
    * 涨跌停控制 仅开盘+算法有用
    */
    public EStopTradeForOwnHiLow m_nStopTradeForOwnHiLow;
    /**
    * 仅用卖出金额  0,1  换仓特有
    */
    public boolean m_bOnlySellAmountUsed;
    /**
    * 买卖偏差上限3-100.00  换仓特有
    */
    public double m_dBuySellAmountDeltaPct;
    /**
    * 收盘后是否继续执行， 0不继续，非0继续
    */
    public int m_nMaxTradeDurationAfterET;
    /**
    * 算法下单方式
    */
    public EOrderStrategyType m_eOrderStrategyType;
	/**
    * 收益互换策略ID
    */
	public String m_strStrategyID;
    /**
    * 投保标志
    */
    public EHedgeFlagType m_eHedgeFlag;
    /**
    * 触价类型
    */
    public EOpTriggerType m_eTriggerType;
    /**
    * 触价价格
    */
    public double m_dTriggerPrice;
	
	/**
    * 投资备注1
    */
	public String m_strRemark1;
	
	/**
    * 开盘集合竞价, 0，不参与，1，参与， 默认0
    */
    public int m_nOpenTrade;
	
	/**
    * 未成委托处理
    */
    public EPriceType m_eUndealtEntrustRule;
	/**
    * 撤单率(取值0-1) 
    */
    public double m_dCancelRateThreshold;
	
    /**
    * JIntelligentAlgorithmOrder构造函数
    */
    public JIntelligentAlgorithmOrder()
    {
        m_strAccountID = "";
        m_strMarket = "";
        m_strInstrument = "";
        m_strOrderType = "";
        m_dPrice = Double.MAX_VALUE;
        m_nVolume = 0;
        m_dMaxPartRate = 0.0;
        m_dMinAmountPerOrder = 0.0;
        m_ePriceType = EPriceType.PRTP_INVALID;
        m_eOperationType = EOperationType.OPT_INVALID;
        m_strRemark = "";
        m_dOrderRateInOpenAcution = 0.2;
        m_dPriceOffsetBpsForAuction = 100;
        m_nStopTradeForOwnHiLow = EStopTradeForOwnHiLow.STOPTRADE_NONE;
        m_bOnlySellAmountUsed = true;
        m_dBuySellAmountDeltaPct = 3.0;
        m_nMaxTradeDurationAfterET = 0;
        m_eOrderStrategyType = EOrderStrategyType.E_ORDER_STRATEGY_TYPE_NORMAL;
		m_strStrategyID = "";
		m_eHedgeFlag = EHedgeFlagType.HEDGE_FLAG_SPECULATION;
		m_eTriggerType = EOpTriggerType.OTT_NONE;
		m_dTriggerPrice = 0.0;
		m_eUndealtEntrustRule = EPriceType.PRTP_INVALID;
		m_dCancelRateThreshold = 0.0;
    }

    /**
    * 设置下单操作类型
    * @param m_eOperationType 下单操作类型
    */
    public void setM_eOperationType(EOperationType m_eOperationType) {
        this.m_eOperationType = m_eOperationType;
    }

    /**
    * 设置报价方式
    * @param m_ePriceType 报价方式
    */
    public void setM_ePriceType(EPriceType m_ePriceType) {
        this.m_ePriceType = m_ePriceType;
    }

    /**
    * 设置涨跌停控制
    * @param m_nStopTradeForOwnHiLow 涨跌停控制
    */
    public void setM_nStopTradeForOwnHiLow(EStopTradeForOwnHiLow m_nStopTradeForOwnHiLow) {
        this.m_nStopTradeForOwnHiLow = m_nStopTradeForOwnHiLow;
    }

    /**
    * 设置算法下单方式
    * @param m_eOrderStrategyType 算法下单方式
    */
    public void setM_eOrderStrategyType(EOrderStrategyType m_eOrderStrategyType) {
        this.m_eOrderStrategyType = m_eOrderStrategyType;
    }

    /**
     * 触价类型
     * @param m_eTriggerType 触价类型
     */
    public void setM_eTriggerType(EOpTriggerType m_eTriggerType) {
        this.m_eTriggerType = m_eTriggerType;
    }
    /**
     * 投保标志
     * @param m_eHedgeFlag 投保标志
     */
    public void setM_eHedgeFlag(EHedgeFlagType m_eHedgeFlag) {
        this.m_eHedgeFlag = m_eHedgeFlag;
    }
	
	/**
    * 设置未成委托处理方式
    * @param m_eUndealtEntrustRule 未成委托处理
    */
    public void setM_eUndealtEntrustRule(EPriceType m_eUndealtEntrustRule) {
        this.m_eUndealtEntrustRule = m_eUndealtEntrustRule;
    }	

}
