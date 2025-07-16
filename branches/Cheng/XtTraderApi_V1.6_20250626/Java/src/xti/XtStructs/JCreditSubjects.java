/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JCreditSubjects.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EXTSubjectsStatus;

/**
* JCreditSubjects类
* 两融融资融券标的数据
*/
public class JCreditSubjects{
    /**
    * 资金账号ID
    */
    public String m_strAccountID;
    /**
    * 市场
    */
    public String m_strExchangeID;
    /**
    * 合约
    */
    public String m_strInstrumentID;
    /**
    * 融资融券保证金比例
    */
    public double m_dSloRatio;
    /**
    * 融券状态
    */
    public EXTSubjectsStatus m_eSloStatus;
    /**
    * 融资保证金比例
    */
    public double m_dFinRatio;
    /**
    * 融资状态
    */
    public EXTSubjectsStatus m_eFinStatus;


    /**
    * 设置融券状态
    * @param m_eSloStatus 融券状态
    */
    public void setM_eSloStatus(EXTSubjectsStatus m_eSloStatus) {
        this.m_eSloStatus = m_eSloStatus;
    }

    /**
    * 设置融资状态
    * @param m_eFinStatus 融资状态
    */
    public void setM_eFinStatus(EXTSubjectsStatus m_eFinStatus) {
        this.m_eFinStatus = m_eFinStatus;
    }
}
