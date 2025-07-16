/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JOrderInfo.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EXTOfferStatus;

/**
* JOrderInfo类
* 指令信息数据
*/
public class JSubscribData{
    /**
    * 平台ID
    */
    public int m_nPlatformID;
    /**
    * 市场代码
    */
    public String m_strExchangeID;
    /**
    * 合约代码,当其值为allCode时，订阅整个市场
    */
    public String m_strInstrumentID;
    /**
    * 报盘状态
    */
    public EXTOfferStatus m_eOfferStatus;

    /**
    * 设置报盘状态
    * @param m_eOfferStatus 报盘状态
    */
    public void setM_eOfferStatus(EXTOfferStatus m_eOfferStatus) {
        this.m_eOfferStatus = m_eOfferStatus;
    }
}
