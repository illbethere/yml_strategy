/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   CStkClosedCompacts.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EXTBrokerType;

/**
* CStkClosedCompacts
* 两融账号已了结负债数据
*/
public class JAccountKey{
    /**
    * 资金账号ID
    */
    public String m_strAccountID;
    /**
    * 账号类型
    */
    public String m_strSubAccount;
    /**
    * 资金账号对应唯一主键
    */
    public String m_strAccountKey;
    /**
    * 经纪公司类别
    */
    public EXTBrokerType m_eBrokerType;
    /**
    * 经纪公司编号
    */
    public int m_nPlatformID;
    /**
    * 账号类型编号
    */
    public int m_nAccountType;
    
    /**
    * 经纪公司类别
    * @param m_eBrokerType 经纪公司类别
    */
    public void setM_eBrokerType(EXTBrokerType m_eBrokerType) {
        this.m_eBrokerType = m_eBrokerType;
    }
}
