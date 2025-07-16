/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JCreditAssure.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EXTSubjectsStatus;

/**
* JCreditAssure类
* 两融账号担保标的数据
*/
public class JCreditAssure{
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
    * 担保品折算比例
    */
    public double m_dAssureRatio;
    /**
    * 担保状态
    */
    public EXTSubjectsStatus m_eAssureStatus;

    /**
    * 设置担保状态
    * @param m_eAssureStatus 担保状态
    */
    public void setM_eAssureStatus(EXTSubjectsStatus m_eAssureStatus) {
        this.m_eAssureStatus = m_eAssureStatus;
    }
}
