/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JCreditSloCode.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EXTCompactBrushSource;

/**
* JCreditSloCode类
* 两融账号可融券数量数据
*/
public class JCreditSloCode{
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
    * 融券可融数量
    */
    public int m_nEnableAmount;
    /**
    * 头寸来源
    */
    public EXTCompactBrushSource m_eCashgroupProp;
    
    /**
    * 设置头寸来源
    * @param m_eCashgroupProp 头寸来源
    */
    public void setM_eCashgroupProp(EXTCompactBrushSource m_eCashgroupProp) {
        this.m_eCashgroupProp = m_eCashgroupProp;
    }
}
