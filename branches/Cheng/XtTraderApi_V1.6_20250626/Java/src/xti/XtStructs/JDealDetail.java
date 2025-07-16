/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JDealDetail.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EEntrustBS;
import xti.XtDataType.EOffsetFlagType;
import xti.XtDataType.EHedgeFlagType;
import xti.XtDataType.EBrokerPriceType;
import xti.XtDataType.ECoveredFlag;
import xti.XtDataType.EEntrustTypes;

/**
* JDealDetail类
* 账号成交数据
*/
public class JDealDetail{
    /**
    * 资金账号ID
    */
    public String m_strAccountID;
    /**
    * 账号类型
    */
    public int m_nAccountType;
    /**
    * 交易所代码
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
    * 成交编号
    */
    public String m_strTradeID;
    /**
    * 委托
    */
    public String m_strOrderSysID;
    /**
    * 成交均价
    */
    public double m_dAveragePrice;
    /**
    * 成交量 期货单位手 股票做到股
    */
    public int m_nVolume;
    /**
    * 成交日期
    */
    public String m_strTradeDate;
    /**
    * 成交时间
    */
    public String m_strTradeTime;
    /**
    * 手续费
    */
    public double m_dComssion;
    /**
    * 成交额 期货=均价*量*合约乘数
    */
    public double m_dAmount;
    /**
    * 指令ID
    */
    public int m_nOrderID;
    /**
    * 期货多空，该字段与m_eOffsetFlag一起判断期货的报单类型。股票无用
    */
    public EEntrustBS m_nDirection;
    /**
    * 期货开平 股票买卖
    */
    public EOffsetFlagType m_nOffsetFlag;
    /**
    * 投机 套利 套保
    */
    public EHedgeFlagType m_nHedgeFlag;
    /**
    * 价格类型，例如市价单 限价单
    */
    public EBrokerPriceType m_nOrderPriceType;
    /**
    * 委托类别
    */
    public EEntrustTypes m_eEntrustType;
    /**
    * 备兑标记
    */
    public ECoveredFlag m_eCoveredFlag;
    /**
    * 投资备注
    */
    public String m_strRemark;

    /**
    *账号key
    */
    public String m_strAccountKey;
    
    /**
    * 收益互换策略ID
    */
    public String m_strStrategyID;
    /**
    * 股东号
    */
    public String m_strSecuAccount;
    
	/**
    * 迅投产品ID
    */
    public int m_nProductId;
    /**
    * 迅投产品名称
    */
    public String m_strProductName;
	
	/**
    * 组合持仓编号，用于解除组合策略
    */
    public String m_strCombID;	
	/**
    * 占用保证金
    */
    public double m_dOccupedMargin;
	/**
    * 汇率
    */
    public double m_dReferenceRate;   
    /**
    * 设置期货多空方向
    * @param m_nDirection 期货多空
    */
    public void setM_nDirection(EEntrustBS m_nDirection) {
        this.m_nDirection = m_nDirection;
    }

    /**
    * 设置期货开平 股票买卖方向
    * @param m_nOffsetFlag 期货开平 股票买卖
    */
    public void setM_nOffsetFlag(EOffsetFlagType m_nOffsetFlag) {
        this.m_nOffsetFlag = m_nOffsetFlag;
    }

    /**
    * 设置投保标志
    * @param m_nHedgeFlag 投保标志
    */
    public void setM_nHedgeFlag(EHedgeFlagType m_nHedgeFlag) {
        this.m_nHedgeFlag = m_nHedgeFlag;
    }

    /**
    * 设置价格类型
    * @param m_nOrderPriceType 价格类型
    */
    public void setM_nOrderPriceType(EBrokerPriceType m_nOrderPriceType) {
        this.m_nOrderPriceType = m_nOrderPriceType;
    }

    /**
    * 设置委托类别
    * @param m_eEntrustType 委托类别
    */
    public void setM_eEntrustType(EEntrustTypes m_eEntrustType) {
        this.m_eEntrustType = m_eEntrustType;
    }

    /**
    * 设置备兑标记
    * @param m_eCoveredFlag 备兑标记
    */
    public void setM_eCoveredFlag(ECoveredFlag m_eCoveredFlag) {
        this.m_eCoveredFlag = m_eCoveredFlag;
    }

}
