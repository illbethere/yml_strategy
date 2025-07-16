/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JAlgorithmOrder.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EOperationType;
import xti.XtDataType.EVolumeType;
import xti.XtDataType.EPriceType;
import xti.XtDataType.EHedgeFlagType;
import xti.XtDataType.EXtOverFreqOrderMode;
import xti.XtDataType.ETimeCondition;
import xti.XtDataType.EVolumeCondition;
import xti.XtDataType.EOpTriggerType;
import xti.XtDataType.EAlgoPriceType;
import xti.XtDataType.EXTCommandDateLimit;
import xti.XtDataType.EStopTradeForOwnHiLow;

/**
* JAlgorithmOrder类
* 算法单下单请求数据
*/
public class JAlgorithmOrder{
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
    * 价格
    */
    public double m_dPrice;
    /**
    * 单笔超价比率
    */
    public double m_dSuperPriceRate;
    /**
    * 超价起始笔数
    */
    public int m_nSuperPriceStart;
    /**
    * 下单量
    */
    public int m_nVolume;
    /**
    * 单笔下单比率
    */
    public double m_dSingleVolumeRate;
    /**
    * 单笔下单量最小值
    */
    public int m_nSingleNumMin;
    /**
    * 单笔下单量最大值
    */
    public int m_nSingleNumMax;
    /**
    * 尾单最小量
    */
    public int m_nLastVolumeMin;
    /**
    * 下单间隔
    */
    public double m_dPlaceOrderInterval;
    /**
    * 撤单间隔
    */
    public double m_dWithdrawOrderInterval;
    /**
    * 最大下单次数，与下单间隔相对应
    */
    public int m_nMaxOrderCount;
    /**
    * 有效开始时间 来自股票，待定
    */
    public int m_nValidTimeStart;
    /**
    * 有效结束时间 来自股票，待定
    */
    public int m_nValidTimeEnd;
    /**
    * 下单操作：开平、多空……
    */
    public EOperationType m_eOperationType;
    /**
    * 单笔下单基准
    */
    public EVolumeType m_eSingleVolumeType;
    /**
    * 报价方式：对手、最新……
    */
    public EPriceType m_ePriceType;
    /**
    * 套利标志
    */
    public EHedgeFlagType m_eHedgeFlag;
    /**
    * 委托频率过快时的处理方式
    */
    public EXtOverFreqOrderMode m_eOverFreqOrderMode;
    /**
    * 期货条件单时间条件
    */
    public ETimeCondition m_eTimeCondition;
    /**
    * 期货条件单数量条件
    */
    public EVolumeCondition m_eVolumeCondition;
    /**
    * 投资备注
    */
    public String m_strRemark;
    /**
    * 触价类型
    */
    public EOpTriggerType m_eTriggerType;
    /**
    * 触价价格
    */
    public double m_dTriggerPrice;
    /**
    * 单笔超价,和m_dSuperPriceRate只用设置一个，优先使用m_dSuperPriceRa
    */
    public double m_dSuperPrice;
    /**
    * 订单类型
    */
    public EAlgoPriceType m_eAlgoPriceType;
    /**
    * 扩展限价类型
    */
    public int m_nExtraLimitType;
    /**
    * 扩展限价
    */
    public double m_dExtraLimitValue;
	
	/**
    * 未成委托处理
    */
    public EPriceType m_eUndealtEntrustRule;
	
	/**
    * 指令跨日开关
    */
    public EXTCommandDateLimit m_eCmdDateLimit;
	
	/**
    * 价格限制类型
    */
	
    public int m_nLimitedPriceType;
	/**
    * 波动区间下限
    */
    public double m_dPriceRangeMin;
	/**
    * 波动区间上限
    */
    public double m_dPriceRangeMax;
	
    /**
    * 涨跌停控制 仅开盘+算法有用
    */
    public EStopTradeForOwnHiLow m_nStopTradeForOwnHiLow;
	
    /**
	
    * JAlgorithmOrder构造函数
    */
    public JAlgorithmOrder()
    {
        m_strAccountID = "";
        m_strMarket = "";
        m_strInstrument = "";
        m_dPrice = Double.MAX_VALUE;
        m_dSuperPriceRate = 0.0;
        m_nSuperPriceStart = 0;
        m_nLastVolumeMin = Integer.MAX_VALUE;
        m_dPlaceOrderInterval = 30.0;  // 单位：秒
        m_dWithdrawOrderInterval = 30.0;  // 单位：秒
        m_nMaxOrderCount = 100;
        m_nValidTimeStart = (int) (System.currentTimeMillis()/1000); // 单位：秒
        m_nValidTimeEnd = m_nValidTimeStart + 1800;  // 单位：秒，有效时间默认为 30min
        m_eSingleVolumeType = EVolumeType.VOLUME_INVALID;
        m_ePriceType = EPriceType.PRTP_INVALID;
        m_eOperationType = EOperationType.OPT_INVALID;
        m_eHedgeFlag = EHedgeFlagType.HEDGE_FLAG_SPECULATION;
        m_eTimeCondition = ETimeCondition.TIME_CONDITION_GFD;
        m_eVolumeCondition = EVolumeCondition.VOLUME_CONDITION_ANY;
        m_strRemark = "";
        m_eTriggerType = EOpTriggerType.OTT_NONE;
        m_dTriggerPrice = 0.0;
        m_dSuperPrice = 0.0;
        m_eAlgoPriceType = EAlgoPriceType.EALGO_PRT_MARKET;
        m_nExtraLimitType = 0;
        m_dExtraLimitValue = 0.0;
		m_eUndealtEntrustRule = EPriceType.PRTP_INVALID;
		m_eCmdDateLimit = EXTCommandDateLimit.XT_COMMAND_LIMIT_NO_OVER_DAY;
		m_nLimitedPriceType = 0;
		m_dPriceRangeMin = 0.0;
        m_dPriceRangeMax = 0.0;
		m_nStopTradeForOwnHiLow = EStopTradeForOwnHiLow.STOPTRADE_NONE;
    }

    /**
    * 设置下单操作类型
    * @param m_eOperationType 下单操作类型
    */
    public void setM_eOperationType(EOperationType m_eOperationType) {
        this.m_eOperationType = m_eOperationType;
    }

    /**
    * 设置单笔下单基准
    * @param m_eSingleVolumeType 单笔下单基准
    */
    public void setM_eSingleVolumeType(EVolumeType m_eSingleVolumeType) {
        this.m_eSingleVolumeType = m_eSingleVolumeType;
    }

    /**
    * 设置报价方式
    * @param m_ePriceType 报价方式
    */
    public void setM_ePriceType(EPriceType m_ePriceType) {
        this.m_ePriceType = m_ePriceType;
    }

    /**
    * 设置套利标志
    * @param m_eHedgeFlag 套利标志
    */
    public void setM_eHedgeFlag(EHedgeFlagType m_eHedgeFlag) {
        this.m_eHedgeFlag = m_eHedgeFlag;
    }

    /**
    * 设置委托频率过快时的处理方式
    * @param m_eOverFreqOrderMode 委托频率过快时的处理方式
    */
    public void setM_eOverFreqOrderMode(EXtOverFreqOrderMode m_eOverFreqOrderMode) {
        this.m_eOverFreqOrderMode = m_eOverFreqOrderMode;
    }

    /**
    * 设置期货条件单时间条件
    * @param m_eTimeCondition 期货条件单时间条件
    */
    public void setM_eTimeCondition(ETimeCondition m_eTimeCondition) {
        this.m_eTimeCondition = m_eTimeCondition;
    }

    /**
    * 设置期货条件单数量条件
    * @param m_eVolumeCondition 期货条件单数量条件
    */
    public void setM_eVolumeCondition(EVolumeCondition m_eVolumeCondition) {
        this.m_eVolumeCondition = m_eVolumeCondition;
    }

    /**
    * 设置触价类型
    * @param m_eTriggerType 设置触价类型
    */
    public void setM_eTriggerType(EOpTriggerType m_eTriggerType) {
        this.m_eTriggerType = m_eTriggerType;
    }

    /**
    * 设置订单类型
    * @param m_eAlgoPriceType 设置订单类型
    */
    public void setM_eAlgoPriceType(EAlgoPriceType m_eAlgoPriceType) {
        this.m_eAlgoPriceType = m_eAlgoPriceType;
    }
	
	/**
    * 设置未成委托处理方式
    * @param m_eUndealtEntrustRule 未成委托处理
    */
    public void setM_eUndealtEntrustRule(EPriceType m_eUndealtEntrustRule) {
        this.m_eUndealtEntrustRule = m_eUndealtEntrustRule;
    }
	
	/**
    * 设置指令跨日开关
    * @param m_eCmdDateLimit 指令跨日开关
    */
    public void setM_eCmdDateLimit(EXTCommandDateLimit m_eCmdDateLimit) {
        this.m_eCmdDateLimit = m_eCmdDateLimit;
    }
	
	/**
    * 设置涨跌停控制
    * @param m_nStopTradeForOwnHiLow 涨跌停控制
    */
    public void setM_nStopTradeForOwnHiLow(EStopTradeForOwnHiLow m_nStopTradeForOwnHiLow) {
        this.m_nStopTradeForOwnHiLow = m_nStopTradeForOwnHiLow;
    }
}
