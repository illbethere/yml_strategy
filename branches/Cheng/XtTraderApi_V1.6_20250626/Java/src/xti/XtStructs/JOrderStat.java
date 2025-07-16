/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JOrderStat.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import java.util.Map;
import xti.XtDataType.EOrderCommandStatus;

/**
* 指令级成交统计
*/
public class JOrderStat{
    /**
    * 指令ID
    */
    public int m_nOrderID;
    /**
    * 交易所代码
    */
    public String m_strExchangeID;
    /**
    * 合约代码
    */
    public String m_strInstrumentID;
    /**
	* 成交均价
	*/
    public double m_dAveragePrice;
    /**
    * 已成交量
    */
    public int m_nTradedVolume;
    /**
    * 成交笔数
    */
    public int m_nTradeNum;
    /**
    * 投资备注
    */
    public String m_strRemark;
}
