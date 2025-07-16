/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JOrderInfo.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EOrderCommandStatus;
import xti.XtDataType.EOperationType;
import xti.XtDataType.EStopTradeForOwnHiLow;

/**
* JOrderInfo类
* 指令信息数据
*/
public class JOrderInfo{
    /**
    * 资金账号
    */
    public String m_strAccountID;	
    /**
	* 账号类型
    */
    public int m_nAccountType;
    /**
    * 指令ID
    */
    public int m_nOrderID;
    /**
    * 下达时间
    */
    public int m_startTime;
    /**
    * 结束时间
    */
    public int m_endTime;
    /**
    * 指令状态
    */
    public EOrderCommandStatus m_eStatus;
    /**
    * 成交量
    */
    public double m_dTradedVolume;
	/**
    * 成交均价
    */
    public double m_dTradedPrice;
    /**
    * 成交金额
    */
    public double m_dTradedAmount;
    /**
    * 指令执行信息
    */
    public String m_strMsg;
    /**
    * 撤销者
    */
    public String m_canceler;
    /**
    * 账号类型
    */
    public int m_eBrokerType;
    /**
    * 投资备注
    */
    public String m_strRemark;
    /**
    * 市场
    */
    public String m_strMarket;
    /**
    * 合约
    */
    public String m_strInstrument;
    /**
    * 算法名称
    */
    public String m_strOrderType;
    /**
    * 基准价
    */
    public double m_dPrice;
    /**
    * 下单总量
    */
    public int m_nVolume;
    /**
    * 有效开始时间
    */
    public int m_nValidTimeStart;
    /**
    * 有效结束时间
    */
    public int m_nValidTimeEnd;
    /**
    * 量比比例
    */
    public double m_dMaxPartRate;
    /**
    * 委托最小金额
    */
    public double m_dMinAmountPerOrder;
    /**
    * 下单操作
    */
    public EOperationType m_eOperationType;
    /**
    * 涨跌停控制
    */
    public EStopTradeForOwnHiLow m_nStopTradeForOwnHiLow;
	/**
    * 账号key
    */
    public String m_strAccountKey;
	/**
    * 条件单价格限制类型
    */
    public int m_nLimitedPriceType;
	/**
    * 条件单其他参数
    */
    public String m_strOtherParam;
	/**
    * 指令来源，比如普通客户端类型、API等
    */
    public int m_nCmdSource;
    /**
    * 设置指令状态
    * @param m_eStatus 指令状态
    */
    public void setM_eStatus(EOrderCommandStatus m_eStatus) {
        this.m_eStatus = m_eStatus;
    }

    /**
    * 设置下单操作
    * @param m_eOperationType 下单操作
    */
    public void setM_eOperationType(EOperationType m_eOperationType) {
        this.m_eOperationType = m_eOperationType;
    }

    /**
    * 设置涨跌停控制
    * @param m_nStopTradeForOwnHiLow 涨跌停控制
    */
    public void setM_nStopTradeForOwnHiLow(EStopTradeForOwnHiLow m_nStopTradeForOwnHiLow) {
        this.m_nStopTradeForOwnHiLow = m_nStopTradeForOwnHiLow;
    }
}
