/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JSecuFundTransferReq.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.ETransTypeCreditFlag;
import xti.XtDataType.ESecuFundTransDirection;

/**
* JSecuFundTransferReq类
* 账号资金股份划拨请求数据
*/
public class JSecuFundTransferReq{
    /**
    * 资金账号ID
    */
    public String m_strAccountID;
    /**
    * 股份划拨市场
    */
    public String m_strExchangeID;
    /**
    * 股份划拨合约
    */
    public String m_strInstrumentID;
    /**
    * 股份划拨数量
    */
    public int m_nOccurAmount;
    /**
    * 股份划拨信用调拨类别
    */
    public ETransTypeCreditFlag m_eCredttransType;
    /**
    * 划拨方向
    */
    public ESecuFundTransDirection m_eTransDirection;
    /**
    * 资金划拨金额
    */
    public double m_dOccurBalance;

    /**
    * 设置股份划拨信用调拨类别
    * @param m_eCredttransType 股份划拨信用调拨类别
    */
    public void setM_eCredttransType(ETransTypeCreditFlag m_eCredttransType) {
        this.m_eCredttransType = m_eCredttransType;
    }
    
    /**
    * 设置划拨方向
    * @param m_eTransDirection 划拨方向
    */
    public void setM_eTransDirection(ESecuFundTransDirection m_eTransDirection) {
        this.m_eTransDirection = m_eTransDirection;
    }
}
