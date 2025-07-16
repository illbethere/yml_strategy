/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JOpVolumeReq.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EOperationType;

/**
* JOpVolumeReq类
* 查询可下单量请求数据
*/
public class JOpVolumeReq{
    /**
    * 资金账号ID
    */
    public String m_strAccountID;
    /**
    * 指定价
    */
    public double m_dPrice;
    /**
    * 合约市场
    */
    public String m_strMarket;
    /**
    * 合约代码
    */
    public String m_strInstrument;
    /**
    * 下单类型，开、平、买、卖…
    */
    public EOperationType m_eOperationType;
 
    /**
    * JOpVolumeReq构造函数
    */
    public JOpVolumeReq(){
        m_strAccountID = "";
        m_dPrice = Double.MAX_VALUE;
        m_strMarket = "";
        m_strInstrument = "";
        m_eOperationType = EOperationType.OPT_INVALID;
    }

    /**
    * 设置下单类型
    * @param m_eOperationType 下单类型
    */
    public void setM_eOperationType(EOperationType m_eOperationType) {
        this.m_eOperationType = m_eOperationType;
    }
}
