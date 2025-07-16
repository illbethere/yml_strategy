/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JOrdinaryOrder.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EPriceType;
import xti.XtDataType.EOperationType;
import xti.XtDataType.EHedgeFlagType;
import xti.XtDataType.ETimeCondition;
import xti.XtDataType.EVolumeCondition;
import xti.XtDataType.ESideFlag;
import xti.XtDataType.EOpTriggerType;
import xti.XtDataType.EAbroadDurationType;

/**
* JOrdinaryOrder类
* 普通单下单请求数据
*/
public class JOrdinaryOrder{
    /**
    * 资金账号ID
    */
    public String m_strAccountID;
    /**
    * 指定价，仅在报价方式为PRTP_FIX(指定价)时有效
    */
    public double m_dPrice;
    /**
    * 单笔超价百分比
    */
    public double m_dSuperPriceRate;
    /**
    * 委托量, 直接还券的数量
    */
    public int m_nVolume;
    /**
    * 合约市场
    */
    public String m_strMarket;
    /**
    * 合约代码
    */
    public String m_strInstrument;
    /**
    * 报价方式： 指定价，最新价 对手价……
    */
    public EPriceType m_ePriceType;
    /**
    * 下单类型，开、平、买、卖…
    */
    public EOperationType m_eOperationType;
    /**
    * 套利标志
    */
    public EHedgeFlagType m_eHedgeFlag;
    /**
    * 直接还款的金额 仅直接还款用
    */
    public double m_dOccurBalance;
    /**
    * 期货条件单时间条件
    */
    public ETimeCondition m_eTimeCondition;
    /**
    * 期货条件单数量条件
    */
    public EVolumeCondition m_eVolumeCondition;
    /**
    * 期权组合委托合约
    */
    public String m_strSecondInstrument;
    /**
    * 期权组合委托价
    */
    public double m_dSecondPrice;
    /**
    * 第一腿合约持仓类型
    */
    public ESideFlag m_eFirstSideFlag;
    /**
    * 第二腿合约持仓类型
    */
    public ESideFlag m_eSecondSideFlag;
    /**
    * 组合持仓编号，用于解除组合策略
    */
    public String m_strCombID;
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
    * 单笔超价,和m_dSuperPriceRate只用设置一个，优先使用m_dSuperPriceRate
    */
    public double m_dSuperPrice;
    /**
    * 投组类型编号
    */
    public int m_nPortfolioID;
    /**
    * 投组策略名称，优先使用m_nPortfolioID
    */
    public String m_strPortfolioStrategyName;
    /**
    * 外盘期货报价类型
    */
    public EAbroadDurationType m_eAbroadDurationType;
    /**
    * 收益互换策略ID
    */
    public String m_strStrategyID;

    /**
     * 股东号
     */
    public String m_strSecuAccount;

    /**
    * JOrdinaryOrder构造函数
    */
    public JOrdinaryOrder(){
        m_strAccountID = "";
        m_dPrice = Double.MAX_VALUE;
        m_dSuperPriceRate = 0.0;
        m_nVolume = Integer.MAX_VALUE;
        m_strMarket = "";
        m_strInstrument = "";
        m_ePriceType = EPriceType.PRTP_INVALID;
        m_eOperationType = EOperationType.OPT_INVALID;
        m_eHedgeFlag = EHedgeFlagType.HEDGE_FLAG_SPECULATION;
        m_dOccurBalance = 0.0;
        m_eTimeCondition = ETimeCondition.TIME_CONDITION_GFD;
        m_eVolumeCondition = EVolumeCondition.VOLUME_CONDITION_ANY;
        m_strSecondInstrument = "";
        m_dSecondPrice = 0.0;
        m_eFirstSideFlag = ESideFlag.SIDE_FLAG_RIGHT;
        m_eSecondSideFlag = ESideFlag.SIDE_FLAG_RIGHT;
        m_strCombID = "";
        m_strRemark = "";
        m_eTriggerType = EOpTriggerType.OTT_NONE;
        m_dTriggerPrice = 0.0;
        m_dSuperPrice = 0.0;
        m_nPortfolioID = -1;
        m_eAbroadDurationType = EAbroadDurationType.TYPE_DURATION_MKT;
        m_strStrategyID = "";
        m_strSecuAccount = "";
    }

    /**
    * 设置报价方式
    * @param m_ePriceType 报价方式
    */
    public void setM_ePriceType(EPriceType m_ePriceType) {
        this.m_ePriceType = m_ePriceType;
    }

    /**
    * 设置下单类型
    * @param m_eOperationType 下单类型
    */
    public void setM_eOperationType(EOperationType m_eOperationType) {
        this.m_eOperationType = m_eOperationType;
    }

    /**
    * 设置投保标志
    * @param m_eHedgeFlag 投保标志
    */
    public void setM_eHedgeFlag(EHedgeFlagType m_eHedgeFlag) {
        this.m_eHedgeFlag = m_eHedgeFlag;
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
    * 设置第一腿合约持仓类型
    * @param m_eFirstSideFlag 第一腿合约持仓类型
    */
    public void setM_eFirstSideFlag(ESideFlag m_eFirstSideFlag) {
    	this.m_eFirstSideFlag = m_eFirstSideFlag;
    }
    
    /**
    * 第二腿合约持仓类型
    * @param m_eSecondSideFlag 第二腿合约持仓类型
    */
    public void setM_eSecondSideFlag(ESideFlag m_eSecondSideFlag) {
    	this.m_eSecondSideFlag = m_eSecondSideFlag;
    }

    /**
    * 设置触价类型
    * @param m_eTriggerType 设置触价类型
    */
    public void setM_eTriggerType(EOpTriggerType m_eTriggerType) {
        this.m_eTriggerType = m_eTriggerType;
    }

    /**
    * 设置外盘期货报价类型
    * @param m_eAbroadDurationType 设置外盘期货报价类型
    */
    public void setM_eAbroadDurationType(EAbroadDurationType m_eAbroadDurationType) {
        this.m_eAbroadDurationType = m_eAbroadDurationType;
    }
}
