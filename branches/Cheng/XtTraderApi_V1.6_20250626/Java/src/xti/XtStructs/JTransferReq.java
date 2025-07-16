/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JTransferReq.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EMoneyType;
import xti.XtDataType.ETransDirection;

/**
* JTransferReq类
* 账号银证转账请求数据
*/
public class JTransferReq{
    /**
    * 资金账号ID
    */
    public String m_strAccountID;
    /**
    * 银行代码
    */
    public String m_strBankNo;
    /**
    * 银行账号
    */
    public String m_strBankAccount;
    /**
    * 资金密码
    */
    public String m_strFundPwd;
    /**
    * 币种
    */
    public EMoneyType m_eMoneyType;
    /**
    * 银证转账方向
    */
    public ETransDirection m_eTransDirection;
    /**
    * 转账金额
    */
    public double m_dOccurBalance;

    /**
    * 设置币种
    * @param m_eMoneyType 币种
    */
    public void setM_eMoneyType(EMoneyType m_eMoneyType) {
        this.m_eMoneyType = m_eMoneyType;
    }
    
    /**
    * 设置银证转账方向
    * @param m_eTransDirection 银证转账方向
    */
    public void setM_eTransDirection(ETransDirection m_eTransDirection) {
        this.m_eTransDirection = m_eTransDirection;
    }
}
