/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JCommissionRateDetail.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

/**
* JCommissionRateDetail类
* 手续费率
*/
public class JCommissionRateDetail{
    /**
    * 市场代码
    */
    public String m_strExchangeID;
    /**
    * 合约代码
    */
    public String m_strInstrumentID;
    /**
    * 开仓手续费率(按金额)
    */
    public double m_dOpenRatioByMoney;
    /**
    * 开仓手续费率(按手)
    */
    public double m_dOpenRatioByVolume;
    /**
    * 平仓手续费率(按金额)
    */
    public double m_dCloseRatioByMoney;
    /**
    * 平仓手续费率(按手)
    */
    public double m_dCloseRatioByVolume;
    /**
    * 平今手续费率(按金额)
    */
    public double m_dCloseTodayRatioByMoney;
    /**
    * 平今手续费率(按手)
    */
    public double m_dCloseTodayRatioByVolume;
    /**
    * 交易日
    */
    public String m_strTradeDate;
}