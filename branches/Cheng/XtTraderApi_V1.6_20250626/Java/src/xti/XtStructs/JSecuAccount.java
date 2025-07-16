/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JSecuAccount.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EMainFlag;

/**
* JSecuAccount类
* 框架号信息
*/
public class JSecuAccount{
    /**
    * 市场代码
    */
    public String m_strExchangeID;
    /**
    * 股东号
    */
    public String m_strSecuAccount;
    /**
    * 主副标记
    */
    public EMainFlag m_eMainFlag;  

    /**
    * 设置主副标记
    * @param m_eMainFlag 主副标记
    */
    public void setM_eMainFlag(EMainFlag m_eMainFlag) {
        this.m_eMainFlag = m_eMainFlag;
    }
}
