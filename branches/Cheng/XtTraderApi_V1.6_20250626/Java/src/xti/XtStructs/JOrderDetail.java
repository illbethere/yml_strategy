/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JOrderDetail.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EBrokerPriceType;
import xti.XtDataType.ECoveredFlag;
import xti.XtDataType.EEntrustBS;
import xti.XtDataType.EOffsetFlagType;
import xti.XtDataType.EHedgeFlagType;
import xti.XtDataType.EEntrustSubmitStatus;
import xti.XtDataType.EEntrustStatus;
import xti.XtDataType.EEntrustTypes;

/**
* JOrderDetail类
* 账号委托数据
*/
public class JOrderDetail{
    /**
    * 资金账号ID
    */
    public String m_strAccountID;
    /**
    * 账号类型
    */
    public int m_nAccountType;
    /**
    * 交易所代码
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
    * 限价单的限价，就是报价
    */
    public double m_dLimitPrice;
    /**
    * 委托号
    */
    public String m_strOrderSysID;
    /**
    * 已成交量
    */
    public int m_nTradedVolume;
    /**
    * 当前总委托量
    */
    public int m_nTotalVolume;
    /**
    * 冻结保证金
    */
    public double m_dFrozenMargin;
    /**
    * 冻结手续费
    */
    public double m_dFrozenCommission;
    /**
    * 成交均价
    */
    public double m_dAveragePrice;
    /**
    * 成交额 期货=均价*量*合约乘数
    */
    public double m_dTradeAmount;
    /**
    * 错误号
    */
    public int m_nErrorID;
    /**
    * 错误信息
    */
    public String m_strErrorMsg;
    /**
    * 日期
    */
    public String m_strInsertDate;
    /**
    * 时间
    */
    public String m_strInsertTime;
    /**
    * 指令ID
    */
    public int m_nOrderID;
    /**
    * 类型，例如市价单 限价单
    */
    public EBrokerPriceType m_nOrderPriceType;
    /**
    * 期货多空，该字段与m_eOffsetFlag一起判断期货的报单类型。股票无用
    */
    public EEntrustBS m_nDirection;
    /**
    * 期货开平，股票买卖
    */
    public EOffsetFlagType m_eOffsetFlag;
    /**
    * 投机 套利 套保
    */
    public EHedgeFlagType m_eHedgeFlag;
    /**
    * 提交状态，股票里面不需要报单状态
    */
    public EEntrustSubmitStatus m_eOrderSubmitStatus;
    /**
    * 委托状态
    */
    public EEntrustStatus m_eOrderStatus;
    /**
    * 委托类别
    */
    public EEntrustTypes m_eEntrustType;
    /**
    * 备兑标记
    */
    public ECoveredFlag m_eCoveredFlag;
    /**
    * 投资备注
    */
    public String m_strRemark;
    /**
    * 废单信息
    */
    public String m_strCancelInfo;

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
    * 组合持仓编号，用于解除组合策略
    */
    public String m_strCombID;
    /**
    * 设置报价类型
    * @param m_nOrderPriceType 报价类型
    */
    public void setM_nOrderPriceType(EBrokerPriceType m_nOrderPriceType) {
        this.m_nOrderPriceType = m_nOrderPriceType;
    }

    /**
    * 设置多空方向
    * @param m_nDirection 多空方向
    */
    public void setM_nDirection(EEntrustBS m_nDirection) {
        this.m_nDirection = m_nDirection;
    }

    /**
    * 设置开平，买卖方向
    * @param m_eOffsetFlag 开平，买卖方向
    */
    public void setM_eOffsetFlag(EOffsetFlagType m_eOffsetFlag) {
        this.m_eOffsetFlag = m_eOffsetFlag;
    }

    /**
    * 设置投保标志
    * @param m_eHedgeFlag 投保标志
    */
    public void setM_eHedgeFlag(EHedgeFlagType m_eHedgeFlag) {
        this.m_eHedgeFlag = m_eHedgeFlag;
    }

    /**
    * 设置提交状态
    * @param m_eOrderSubmitStatus 提交状态
    */
    public void setM_eOrderSubmitStatus(EEntrustSubmitStatus m_eOrderSubmitStatus) {
        this.m_eOrderSubmitStatus = m_eOrderSubmitStatus;
    }

    /**
    * 设置委托状态
    * @param m_eOrderStatus 委托状态
    */
    public void setM_eOrderStatus(EEntrustStatus m_eOrderStatus) {
        this.m_eOrderStatus = m_eOrderStatus;
    }

    /**
    * 设置委托类别
    * @param m_eEntrustType 委托类别
    */
    public void setM_eEntrustType(EEntrustTypes m_eEntrustType) {
        this.m_eEntrustType = m_eEntrustType;
    }

    /**
    * 设置备兑标记
    * @param m_eCoveredFlag 备兑标记
    */
    public void setM_eCoveredFlag(ECoveredFlag m_eCoveredFlag) {
        this.m_eCoveredFlag = m_eCoveredFlag;
    }

}
