/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JTransferSerial.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EMoneyType;
import xti.XtDataType.ETransDirection;

/**
* JTransferSerial类
* 银证转账银行流水数据
*/
public class JTransferSerial{
    /**
    * 资金账号ID
    */
    public String m_strAccountID;
    /**
    * 资金账号key
    */
    public String m_strAccountKey;
    /**
    * 转账日期
    */
    public String m_strTransferDate;
    /**
    * 转账时间
    */
    public String m_strTransferTime;
    /**
    * 币种
    */
    public EMoneyType m_eMoneyType;
    /**
    * 流水号
    */
    public String m_strTransferNo;
    /**
    * 转账方向
    */
    public ETransDirection m_eTransDirection;
    /**
    * 转账金额
    */
    public double m_dTransferBalance;
    /**
    * 银行账号
    */
    public String m_strBankAccount;
    /**
    * 银行名称
    */
    public String m_strBankName;
    /**
    * 银行代码
    */
    public String m_strBankNo;
    /**
    * 备注
    */
    public String m_strRemark;

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
