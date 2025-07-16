/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   CStkClosedCompacts.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EXTCompactType;
import xti.XtDataType.EXTCompactBrushSource;

/**
* CStkClosedCompacts
* 两融账号已了结负债数据
*/
public class JStkClosedCompacts{
    /**
    * 资金账号ID
    */
    public String m_strAccountID;
    /**
    * 资金账号key
    */
    public String m_strAccountKey;
    /**
    * 交易所
    */
    public String m_strExchangeID;
    /**
    * 证券代码
    */
    public String m_strInstrumentID;
    /**
    * 合约类型
    */
    public EXTCompactType m_eCompactType;
    /**
    * 头寸来源
    */
    public EXTCompactBrushSource m_eCashgroupProp;
    /**
    * 开仓日期
    */
    public int m_nOpenDate;
    /**
    * 合约证券数量
    */
    public int m_nBusinessVol;
    /**
    * 到期日
    */
    public int m_nRetEndDate;
    /**
    * 了结日期
    */
    public int m_nDateClear;
    /**
    * 委托数量
    */
    public int m_nEntrustVol;
    /**
    * 委托金额
    */
    public double m_dEntrustBalance;
    /**
    * 合约金额
    */
    public double m_dBusinessBalance;
    /**
    * 合约息费
    */
    public double m_dBusinessFare;
    /**
    * 已还息费
    */
    public double m_dRepaidFare;
    /**
    * 已还金额
    */
    public double m_dRepaidBalance;
    /**
    * 合约编号
    */
    public String m_strCompactId;
    /**
    * 委托编号
    */
    public String m_strEntrustNo;
    /**
    * 定位串
    */
    public String m_strPositionStr;

    /**
    * 合约类型
    * @param m_eCompactType 合约类型
    */
    public void setM_eCompactType(EXTCompactType m_eCompactType) {
        this.m_eCompactType = m_eCompactType;
    }

    /**
    * 设置头寸来源
    * @param m_eCashgroupProp 头寸来源
    */
    public void setM_eCashgroupProp(EXTCompactBrushSource m_eCashgroupProp) {
        this.m_eCashgroupProp = m_eCashgroupProp;
    }
}
