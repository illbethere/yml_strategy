/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JPositionDetail.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EHedgeFlagType;
import xti.XtDataType.EEntrustBS;

/**
* JPositionDetail类
* 账号持仓明细数据
*/
public class JPositionDetail{
    /**
    * 资金账号ID
    */
    public String m_strAccountID;
    /**
    * 市场代码
    */
    public String m_strExchangeID;
    /**
    * 合约品种
    */
    public String m_strProductID;
    /**
    * 合约代码
    */
    public String m_strInstrumentID;
    /**
    * 合约名称
    */
    public String m_strInstrumentName;
    /**
    * 开仓日期
    */
    public String m_strOpenDate;
    /**
    * 最初开仓位的成交编号
    */
    public String m_strTradeID;
    /**
    * 持仓量 当前拥股
    */
    public int m_nVolume;
    /**
    * 开仓价
    */
    public double m_dOpenPrice;
    /**
    * 交易日
    */
    public String m_strTradingDay;
    /**
    * 使用的保证金 历史的直接用ctp的，新的自己用成本价*存量*系数算  股票不需要
    */
    public double m_dMargin;
    /**
    * 开仓成本 等于股票的成本价*第一次建仓的量，后续减持不影响，不算手续费 股票不需要
    */
    public double m_dOpenCost;
    /**
    * 结算价 对于股票的当前价
    */
    public double m_dSettlementPrice;
    /**
    * 平仓量 等于股票已经卖掉的 股票不需要
    */
    public int m_nCloseVolume;
    /**
    * 平仓额 等于股票每次卖出的量*卖出价*合约乘数（股票为1）的累加 股票不需要
    */
    public double m_dCloseAmount;
    /**
    * 浮动盈亏 当前量*（当前价-开仓价）*合约乘数（股票为1）
    */
    public double m_dFloatProfit;
    /**
    * 平仓盈亏 平仓额 - 开仓价*平仓量*合约乘数（股票为1） 股票不需要
    */
    public double m_dCloseProfit;
    /**
    * 市值 合约价值
    */
    public double m_dMarketValue;
    /**
    * 持仓成本 股票不需要
    */
    public double m_dPositionCost;
    /**
    * 持仓盈亏 股票不需要
    */
    public double m_dPositionProfit;
    /**
    * 最新结算价 股票不需要
    */
    public double m_dLastSettlementPrice;
    /**
    * 合约价值 股票不需要
    */
    public double m_dInstrumentValue;
    /**
    * 是否今仓
    */
    public boolean m_bIsToday;
    /**
    * 指令ID
    */
    public int m_nOrderID;
    /**
    * 期货不用这个字段，冻结数量
    */
    public int m_nFrozenVolume;
    /**
    * 期货不用这个字段，股票的可用数量
    */
    public int m_nCanUseVolume;
    /**
    * 期货不用这个字段，股票的在途数量
    */
    public int m_nOnRoadVolume;
    /**
    * 期货不用这个字段，股票的股份余额
    */
    public int m_nYesterdayVolume;
    /**
    * 结算价 对于股票的当前价
    */
    public double m_dLastPrice;
    /**
    * 投机 套利 套保
    */
    public EHedgeFlagType m_nHedgeFlag;
    /**
    * 期货多空，该字段与m_eOffsetFlag一起判断期货的报单类型。股票无用
    */
    public EEntrustBS m_nDirection;
    /**
    * 备兑数量
    */
    public int m_nCoveredAmount;
    /**
    * 账号类型
    */
    public int m_nAccountType;
    /**
    * 持仓盈亏比例
    */
    public double m_dProfitRate;

    /**
    *账号key
    */
    public String m_strAccountKey;
    
    /**
    * 收益互换策略ID
    */
    public String m_strStrategyID;
    /**
    * 股东号
    */
    public String m_strSecuAccount;
    
    /**
    * 设置投保标志
    * @param m_nHedgeFlag 投保标志
    */
    public void setM_nHedgeFlag(EHedgeFlagType m_nHedgeFlag) {
        this.m_nHedgeFlag = m_nHedgeFlag;
    }

    /**
    * 设置多空方向
    * @param m_nDirection 多空方向
    */
    public void setM_nDirection(EEntrustBS m_nDirection) {
        this.m_nDirection = m_nDirection;
    }

}
