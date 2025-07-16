/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JExternAlgorithmOrder.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EOperationType;
import xti.XtDataType.EStopTradeForOwnHiLow;
import xti.XtDataType.EOrderStrategyType;

/**
* JAlgorithmOrder类
* 算法单下单请求数据
*/
public class JExternAlgorithmOrder{
    /**
    * 资金账号ID
    */
    public String m_strAccountID;
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
    * 下单价格
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
    * 下单操作：开平、多空……
    */
    public EOperationType m_eOperationType;
    /**
    * 投资备注
    */
    public String m_strRemark;
    /**
    * 涨跌停控制
    */
    public EStopTradeForOwnHiLow m_nStopTradeForOwnHiLow;
    /**
    * 算法下单方式
    */
    public EOrderStrategyType m_eOrderStrategyType;
    /**
    * t0策略最大可用资金
    */
    public double m_dAvailable;
    /**
    * 收盘后是否继续执行， 0不继续，非0继续
    */
    public int m_nMaxTradeDurationAfterET;
	/**
    * 投资备注1
    */
	public String m_strRemark1;

    /**
    * JExternAlgorithmOrder构造函数
    */
    public JExternAlgorithmOrder()
    {
        m_strAccountID = "";
        m_strMarket = "";
        m_strInstrument = "";
        m_strOrderType = "";
        m_dPrice = Double.MAX_VALUE;
        m_nVolume = 0;
        m_dMaxPartRate = 0.0;
        m_dMinAmountPerOrder = 0.0;
        m_nValidTimeStart = (int) (System.currentTimeMillis()/1000); // 单位：秒
        m_nValidTimeEnd = m_nValidTimeStart + 1800;  // 单位：秒，有效时间默认为 30min
        m_eOperationType = EOperationType.OPT_INVALID;
        m_strRemark = "";
        m_nStopTradeForOwnHiLow = EStopTradeForOwnHiLow.STOPTRADE_NONE;
        m_eOrderStrategyType = EOrderStrategyType.E_ORDER_STRATEGY_TYPE_NORMAL;
    }

    /**
    * 设置下单操作类型
    * @param m_eOperationType 下单操作类型
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

    /**
    * 设置算法下单方式
    * @param m_eOrderStrategyType 算法下单方式
    */
    public void setM_eOrderStrategyType(EOrderStrategyType m_eOrderStrategyType) {
        this.m_eOrderStrategyType = m_eOrderStrategyType;
    }
}
