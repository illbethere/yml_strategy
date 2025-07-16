/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JStkCompacts.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EXTCompactType;
import xti.XtDataType.EXTCompactStatus;
import xti.XtDataType.EBrokerPriceType;
import xti.XtDataType.EOffsetFlagType;

/**
* JStkCompacts类
* 两融账号负债信息数据
*/
public class JStkCompacts{
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
    * 合约开仓日期
    */
    public int m_nOpenDate;
    /**
    * 合约编号
    */
    public String m_strCompactId;
    /**
    * 融资融券保证金比例
    */
    public double m_dCrdtRatio;
    /**
    * 委托编号
    */
    public String m_strEntrustNo;
    /**
    * 委托价格
    */
    public double m_dEntrustPrice;
    /**
    * 委托数量
    */
    public int m_nEntrustVol;
    /**
    * 合约开仓数量
    */
    public int m_nBusinessVol;
    /**
    * 合约开仓金额
    */
    public double m_dBusinessBalance;
    /**
    * 合约开仓费用
    */
    public double m_dBusinessFare;
    /**
    * 合约类型
    */
    public EXTCompactType m_eCompactType;
    /**
    * 合约状态
    */
    public EXTCompactStatus m_eCompactStatus;
    /**
    * 未还合约金额
    */
    public double m_dRealCompactBalance;
    /**
    * 未还合约数量
    */
    public int m_nRealCompactVol;
    /**
    * 未还合约费用
    */
    public double m_dRealCompactFare;
    /**
    * 未还合约利息
    */
    public double m_dRealCompactInterest;
    /**
    * 已还利息
    */
    public double m_dRepaidInterest;
    /**
    * 已还数量
    */
    public int m_nRepaidVol;
    /**
    * 已还金额
    */
    public double m_dRepaidBalance;
    /**
    * 合约总利息
    */
    public double m_dCompactInterest;
    /**
    * 占用保证金
    */
    public double m_dUsedBailBalance;
    /**
    * 合约年利率
    */
    public double m_dYearRate;
    /**
    * 归还截止日
    */
    public int m_nRetEndDate;
    /**
    * 了结日期
    */
    public String m_strDateClear;
    /**
    * 最新价
    */
    public double m_dPrice;
    /**
    * 开仓的时间
    */
    public int m_nOpenTime;
    /**
    * 合约对应的委托的撤单数量
    */
    public int m_nCancelVol;
    /**
    * 价格类型，例如市价单 限价单
    */
    public EBrokerPriceType m_nOrderPriceType;
    /**
    * 操作,开平,买卖,操作
    */
    public EOffsetFlagType m_nOffsetFlag;       //操作,开平,买卖,操作

    /**
    * 设置合约状态
    * @param m_eCompactType 合约状态
    */
    public void setM_eCompactType(EXTCompactType m_eCompactType) {
        this.m_eCompactType = m_eCompactType;
    }

    /**
    * 设置合约类型
    * @param m_eCompactStatus 合约类型
    */
    public void setM_eCompactStatus(EXTCompactStatus m_eCompactStatus) {
        this.m_eCompactStatus = m_eCompactStatus;
    }

    /**
    * 设置操作类型
    * @param m_nOrderPriceType 操作类型
    */
    public void setM_nOrderPriceType(EBrokerPriceType m_nOrderPriceType) {
        this.m_nOrderPriceType = m_nOrderPriceType;
    }

    /**
    * 设置价格类型
    * @param m_nOffsetFlag 价格类型
    */
    public void setM_nOffsetFlag(EOffsetFlagType m_nOffsetFlag) {
        this.m_nOffsetFlag = m_nOffsetFlag;
    }
}
