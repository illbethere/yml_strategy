/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JAccountDetail.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EDualStatus;

/**
* JAccountDetail类
* 用户下资金帐号的资金数据
*/
public class JAccountDetail{
    /**
    * 资金账号ID
    */
    public String m_strAccountID;
    /**
    * 账号类型
    */
    public int m_nAccountType;
    /**
    * 账号登陆状态
    */
    public String m_strStatus;
    /**
    * 当前交易日
    */
    public String m_strTradingDate;
    /**
    * 冻结保证金，外源性 股票的保证金就是冻结资金 股票不需要
    */
    public double m_dFrozenMargin;
    /**
    * 冻结资金，内外源冻结保证金和手续费四个的和
    */
    public double m_dFrozenCash;
    /**
    * 冻结手续费
    */
    public double m_dFrozenCommission;
    /**
    * 风险度
    */
    public double m_dRisk;
    /**
    * 单位净值
    */
    public double m_dNav;
    /**
    * 期初权益
    */
    public double m_dPreBalance;
    /**
    * 动态权益, 总资产
    */
    public double m_dBalance;
    /**
    * 可用资金
    */
    public double m_dAvailable;
    /**
    * 已用手续费
    */
    public double m_dCommission;
    /**
    * 持仓盈亏
    */
    public double m_dPositionProfit;
    /**
    * 平仓盈亏
    */
    public double m_dCloseProfit;
    /**
    * 出入金净值
    */
    public double m_dCashIn;
    /**
    * 当前占用保证金
    */
    public double m_dCurrMargin;
    /**
    * 合约市值
    */
    public double m_dInstrumentValue;
    /**
    * 入金
    */
    public double m_dDeposit;
    /**
    * 出金
    */
    public double m_dWithdraw;
    /**
    * 信用额度
    */
    public double m_dCredit;
    /**
    * 质押
    */
    public double m_dMortgage;
    /**
    * 股票总市值，期货没有
    */
    public double m_dStockValue;
    /**
    * 债券总市值，期货没有
    */
    public double m_dLoanValue;
    /**
    * 基金总市值，包括ETF和封闭式基金，期货没有
    */
    public double m_dFundValue;
    /**
    * 回购总市值，所有回购，期货没有
    */
    public double m_dRepurchaseValue;
    /**
    * 多单总市值，现货没有
    */
    public double m_dLongValue;
    /**
    * 空单总市值，现货没有
    */
    public double m_dShortValue;
    /**
    * 净持仓总市值，净持仓市值=多-空
    */
    public double m_dNetValue;
    /**
    * 净资产
    */
    public double m_dAssureAsset;
    /**
    * 总负债
    */
    public double m_dTotalDebit;
    /**
    * 权利金净支出 用于股票期权
    */
    public double m_dPremiumNetExpense;
    /**
    * 可用保证金 用于股票期权
    */
    public double m_dEnableMargin;
    /**
    * 可取金额
    */
    public double m_dFetchBalance;
    /**
    * 可取金额
    */
    public EDualStatus m_eDualStatus;
    /**
    * 双中心上海可用
    */
    public double m_dAvailableSH;
    /**
    * 双中心深圳可用
    */
    public double m_dAvailableSZ;
   
    /**
    *账号key
    */
    public String m_strAccountKey;
    /**
    * 迅投产品ID
    */
    public int m_nProductId;
    /**
    * 占用保证金 用于股票期权
    */
    public double m_dUsedMargin;
    /**
    * 权利金支出 用于股票期权
    */
    public double m_dRoyalty;
    /**
    *迅投产品名称
    */
    public String m_strProductName;
	/**
    * 当日盈亏
    */
    public double m_dDaysProfit;
	/**
    *账号名称
    */
    public String m_strAccountName;
	/**
    *经纪公司编号
    */
    public String m_strBrokerID;
	/**
    *经纪公司名称
    */
    public String m_strBrokerName;
	/**
    *动态权益含期权
    */
    public double m_dAssetBalance;
	/**
    *风险度含期权
    */
    public double m_dRiskDegree;
	/**
    *初始平仓盈亏
    */
    public double m_dInitCloseMoney;
    /**
    * 设置双中心状态
    * @param m_eDualStatus 双中心状态
    */
    public void setM_eDualStatus(EDualStatus m_eDualStatus) {
        this.m_eDualStatus = m_eDualStatus;
    }
}
