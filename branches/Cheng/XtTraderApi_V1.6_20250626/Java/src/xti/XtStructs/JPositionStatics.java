/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JPositionStatics.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EEntrustBS;
import xti.XtDataType.EHedgeFlagType;
import xti.XtDataType.ESideFlag;

/**
* JPositionStatics类
* 账号持仓统计数据
*/
public class JPositionStatics{
    /**
    * 资金账号ID
    */
    public String m_strAccountID;
    /**
    * 市场代码
    */
    public String m_strExchangeID;
    /**
    * 合约品种
    */
    public String m_strProductID;
    /**
    * 合约代码
    */
    public String m_strInstrumentID;
    /**
    * 合约名称
    */
    public String m_strInstrumentName;
    /**
    * 是否今仓
    */
    public boolean m_bIsToday;
    /**
    * 持仓量
    */
    public int m_nPosition;
    /**
    * 非任务平冻结
    */
    public double m_dOpenCost;
    /**
    * 持仓成本 detail的汇总
    */
    public double m_dPositionCost;
    /**
    * 持仓均价
    */
    public double m_dAveragePrice;
    /**
    * 持仓盈亏 detail的汇总
    */
    public double m_dPositionProfit;
    /**
    * 浮动盈亏 detail的汇总
    */
    public double m_dFloatProfit;
    /**
    * 开仓均价 股票不需要
    */
    public double m_dOpenPrice;
    /**
    * 可平量
    */
    public int m_nCanCloseVolume;
    /**
    * 已使用保证金
    */
    public double m_dUsedMargin;
    /**
    * 已使用的手续费
    */
    public double m_dUsedCommission;
    /**
    * 冻结保证金
    */
    public double m_dFrozenMargin;
    /**
    * 冻结手续费
    */
    public double m_dFrozenCommission;
    /**
    * 合约价值
    */
    public double m_dInstrumentValue;
    /**
    * 开仓次数
    */
    public int m_nOpenTimes;
    /**
    * 总开仓量 中间平仓不减
    */
    public int m_nOpenVolume;
    /**
    * 撤单次数
    */
    public int m_nCancelTimes;
    /**
    * 期货不用这个字段，冻结数量
    */
    public int m_nFrozenVolume;
    /**
    * 期货不用这个字段，股票的可用数量
    */
    public int m_nCanUseVolume;
    /**
    * 期货不用这个字段，股票的在途数量
    */
    public int m_nOnRoadVolume;
    /**
    * 期货不用这个字段，股票的股份余额
    */
    public int m_nYesterdayVolume;
    /**
    * 前收盘价
    */
    public double m_dSettlementPrice;
    /**
    * 持仓盈亏比例
    */
    public double m_dProfitRate;
    /**
    * 期货多空，该字段与m_eOffsetFlag一起判断期货的报单类型。股票无用
    */
    public EEntrustBS m_nDirection;
    /**
    * 投机 套利 套保
    */
    public EHedgeFlagType m_nHedgeFlag;
    /**
    * 备兑数量
    */
    public int m_nCoveredAmount;
    /**
    * 账号类型
    */
    public int m_nAccountType;
    /**
    * 最新价
    */
    public double m_dLastPrice;

    /**
    * 收益互换策略ID
    */
    public String m_strStrategyID;

    /**
    *账号key
    */
    public String m_strAccountKey;
    /**
    * 股东号
    */
    public String m_strSecuAccount;
	/**
    * 期权合约持仓类型
    */
    public ESideFlag m_eSideFlag;
	/**
    * 汇率
    */
    public double m_dReferenceRate;  
    /**
    * 单股成本
    */
    public double m_dSingleCost;

    /**
    * 设置多空方向
    * @param m_nDirection 多空方向
    */
    public void setM_nDirection(EEntrustBS m_nDirection) {
        this.m_nDirection = m_nDirection;
    }

    /**
    * 设置投保标志
    * @param m_nHedgeFlag 投保标志
    */
    public void setM_nHedgeFlag(EHedgeFlagType m_nHedgeFlag) {
        this.m_nHedgeFlag = m_nHedgeFlag;
    }

    /**
     * 期权合约持仓类型
     * @param m_eSideFlag 期权合约持仓类型
     */
    public void setM_eSideFlag(ESideFlag m_eSideFlag) {
        this.m_eSideFlag = m_eSideFlag;
    }


}
