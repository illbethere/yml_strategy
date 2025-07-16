/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JReferenceRate.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EMoneyType;

/**
* JReferenceRate类
* 港股账号汇率数据
*/
public class JReferenceRate{
    /**
    * 资金账号ID
    */
    public String m_strAccountID;
    /**
    * 交易所
    */
    public String m_strExchangeID;
    /**
    * 市场名字
    */
    public String m_strExchangeName;
    /**
    * 币种
    */
    public EMoneyType m_eMoneyType;
    /**
    * 买入参考汇率
    */
    public double m_bBidReferenceRate;
    /**
    * 卖出参考汇率
    */
    public double m_bAskReferenceRate;
    /**
    * 买入结算汇率
    */
    public double m_bBidSettlementRate;
    /**
    * 卖出结算汇率
    */
    public double m_bAskSettlementRate;
    /**
    * 日间买入参考汇率浮动比例
    */
    public double m_dDayBuyRiseRate;
    /**
    * 夜市买入参考汇率浮动比例
    */
    public double m_dNightBuyRiseRate;
    /**
    * 日间卖出参考汇率浮动比例
    */
    public double m_dDaySaleRiseRate;
    /**
    * 夜间卖出参考汇率浮动比例
    */
    public double m_dNightSaleRiseRate;
    /**
    * 参考汇率中间汇率
    */
    public double m_bMidReferenceRate;

    /**
    * 设置币种
    * @param m_eMoneyType 币种
    */
    public void setM_eMoneyType(EMoneyType m_eMoneyType) {
        this.m_eMoneyType = m_eMoneyType;
    }

}
