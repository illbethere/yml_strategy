/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   CStkUnClosedCompacts.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EXTCompactType;
import xti.XtDataType.EXTCompactBrushSource;

/**
* CStkUnClosedCompacts
* 两融账号未了结负债数据
*/
public class JStkUnClosedCompacts{
    /**
    * 资金账号ID
    */
    public String m_strAccountID;
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
    * 未还合约数量
    */
    public int m_nRealCompactVol;
    /**
    * 到期日
    */
    public int m_nRetEndDate;
    /**
    * 合约金额
    */
    public double m_dBusinessBalance;
    /**
    * 合约息费
    */
    public double m_dBusinessFare;
    /**
    * 未还合约金额
    */
    public double m_dRealCompactBalance;
    /**
    * 未还合约息费
    */
    public double m_dRealCompactFare;
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
    * 偿还优先级
    */
    public int m_nRepayPriority;
    /**
    * 定位串
    */
    public String m_strPositionStr;

    /**
    * 设置合约类型
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
