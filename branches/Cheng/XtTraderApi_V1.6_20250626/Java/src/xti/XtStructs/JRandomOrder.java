/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JRandomOrder.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/
package xti.XtStructs;

import xti.XtDataType.EHedgeFlagType;
import xti.XtDataType.EOperationType;
import xti.XtDataType.EPriceType;

/**
* JAlgorithmOrder类
* 算法单下单请求数据
*/
public class JRandomOrder{
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
    * 下单间隔
    */
    public int m_nValidTimeElapse;
    /**
    * 单比下单量最小值
    */
    public int m_nSingleNumMin;
    /**
    * 单比下单量最大值
    */
    public int m_nSingleNumMax;
    /**
    * 下单操作：开平、多空……
    */
    public EOperationType m_eOperationType;
    /**
    * 报价方式：对手、最新……
    */
    public EPriceType m_ePriceType;
    /**
    * 套利标志
    */
    public EHedgeFlagType m_eHedgeFlag;
    /**
    * 投资备注
    */
    public String m_strRemark;

    /**
    * JRandomOrder构造函数
    */
    public JRandomOrder()
    {
        m_strAccountID = "";
        m_strMarket = "";
        m_strInstrument = "";
        m_strOrderType = "";
        m_dPrice = Double.MAX_VALUE;
        m_nVolume = 0;
        m_nValidTimeElapse = 0;
        m_nSingleNumMin = 0;
        m_nSingleNumMax = 0;
        m_ePriceType = EPriceType.PRTP_INVALID;
        m_eOperationType = EOperationType.OPT_INVALID;
        m_strRemark = "";
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
}
