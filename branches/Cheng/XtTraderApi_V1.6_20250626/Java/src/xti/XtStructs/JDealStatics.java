/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JDealStatics.java
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
public class JDealStatics{
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
    * 成交均价
    */
    public double m_dAveragePrice;
    /**
    * 成交量 期货单位手 股票做到股
    */
    public int m_nVolume;
    /**
    * 手续费
    */
    public double m_dComssion;
    /**
    * 成交额 期货=均价*量*合约乘数
    */
    public double m_dAmount;
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
    * 相同合约相同方向条数
    */
    public int m_nCount;
	
	/**
    * 迅投产品ID
    */
    public int m_nProductId;
	/**
    * 迅投产品名称
    */
    public String m_strProductName;
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

}
