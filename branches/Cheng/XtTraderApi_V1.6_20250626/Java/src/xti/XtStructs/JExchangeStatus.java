/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JExchangeStatus.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EXTExchangeStatus;

/**
* JExchangeStatus
* 市场状态信息
*/
public class JExchangeStatus{
    /**
    * 交易所代码
    */
    public String m_strExchangeId;
    /**
    * 合约品种
    */
    public String m_strProductId;
    /**
    * 合约代码
    */
    public String m_strInstrumentId;
    /**
    * 进入本状态时间
    */
    public String m_strEnterTime;
    /**
    * 进入本状态原因
    */
    public String m_strEnterReason;
    /**
    * 市场状态
    */
    public EXTExchangeStatus m_eInstrumentStatus;
    /**
    * 交易所时间相对于服务器时间的时间差
    */
    public int m_nExchangeTimeDelta;
 
    /**
    * 设置市场状态
    * @param m_eInstrumentStatus 市场状态
    */
    public void setM_eInstrumentStatus(EXTExchangeStatus m_eInstrumentStatus) {
        this.m_eInstrumentStatus = m_eInstrumentStatus;
    }
}
