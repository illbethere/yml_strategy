/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   CMarginRateDetail.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

/**
* CMarginRateDetail类
* 保证金率
*/
public class JMarginRateDetail{
    /**
    * 市场代码
    */
    public String m_strExchangeID;
    /**
    * 合约代码
    */
    public String m_strInstrumentID;
    /**
    * 投机套保标志
    */
    public int m_nHedgeFlag;
    /**
    * 按金额多头保证金率
    */
    public double m_dLongMarginRatioByMoney;
    /**
    * 按数量多头保证金费
    */
    public double m_dLongMarginRatioByVolume;
    /**
    * 按金额空头保证金率
    */
    public double m_dShortMarginRatioByMoney;
    /**
    * 按数量空头保证金费
    */
    public double m_dShortMarginRatioByVolume;
    /**
    * 是否相对交易所收取
    */
    public int m_nIsRelative;
    /**
    * 交易日
    */
    public String m_strTradeDate;
}