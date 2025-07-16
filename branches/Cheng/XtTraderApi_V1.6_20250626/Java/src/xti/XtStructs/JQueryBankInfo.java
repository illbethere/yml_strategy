/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JQueryBankInfo.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EMoneyType;

/**
* JQueryBankInfo类
* 银证转账银行信息数据
*/
public class JQueryBankInfo{
    /**
    * 资金账号ID
    */
    public String m_strAccountID;
    /**
    * 资金账号key
    */
    public String m_strAccountKey;
    /**
    * 银行代码
    */
    public String m_strBankNo;
    /**
    * 银行账号
    */
    public String m_strBankAccount;
    /**
    * 币种
    */
    public EMoneyType m_eMoneyType;
    /**
    * 银行名称，查询时可不送
    */
    public String m_strBankName;

    /**
    * 设置币种
    * @param m_eMoneyType 币种
    */
    public void setM_eMoneyType(EMoneyType m_eMoneyType) {
        this.m_eMoneyType = m_eMoneyType;
    }

}
