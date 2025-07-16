/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JQueryBankAmount.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EMoneyType;

/**
* JQueryBankAmount类
* 账号银证转账银行余额数据
*/
public class JQueryBankAmount{
    /**
    * 资金账号ID
    */
    public String m_strAccountID;
    /**
    * 资金账号key
    */
    public String m_strAccountKey;
    /**
    * 银行账号
    */
    public String m_strBankAccount;
    /**
    * 币种
    */
    public EMoneyType m_eMoneyType;
    /**
    * 银行余额
    */
    public double m_dBalance;
    /**
    * 可转金额
    */
    public double m_dEnableBalance;

    /**
    * 设置币种
    * @param m_eMoneyType 币种
    */
    public void setM_eMoneyType(EMoneyType m_eMoneyType) {
        this.m_eMoneyType = m_eMoneyType;
    }

}
