/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JCreditAccountDetail.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

/**
* JCreditAccountDetail类
* 账号两融资金数据
*/
public class JCreditAccountDetail{
    /**
    * 个人维持担保比例
    */
    public double m_dPerAssurescaleValue;
    /**
    * 可用保证金
    */
    public double m_dEnableBailBalance;
    /**
    * 已用保证金
    */
    public double m_dUsedBailBalance;
    /**
    * 可买担保品资金
    */
    public double m_dAssureEnbuyBalance;
    /**
    * 可买标的券资金
    */
    public double m_dFinEnbuyBalance;
    /**
    * 可还券资金
    */
    public double m_dSloEnrepaidBalance;
    /**
    * 可还款资金
    */
    public double m_dFinEnrepaidBalance;
    /**
    * 融资授信额度
    */
    public double m_dFinMaxQuota;
    /**
    * 融资可用额度
    */
    public double m_dFinEnableQuota;
    /**
    * 融资已用额度
    */
    public double m_dFinUsedQuota;
    /**
    * 融资已用保证金额
    */
    public double m_dFinUsedBail;
    /**
    * 融资合约金额
    */
    public double m_dFinCompactBalance;
    /**
    * 融资合约费用
    */
    public double m_dFinCompactFare;
    /**
    * 融资合约利息
    */
    public double m_dFinCompactInterest;
    /**
    * 融资市值
    */
    public double m_dFinMarketValue;
    /**
    * 融资合约盈亏
    */
    public double m_dFinIncome;
    /**
    * 融券授信额度
    */
    public double m_dSloMaxQuota;
    /**
    * 融券可用额度
    */
    public double m_dSloEnableQuota;
    /**
    * 融券已用额度
    */
    public double m_dSloUsedQuota;
    /**
    * 融券已用保证金额
    */
    public double m_dSloUsedBail;
    /**
    * 融券合约金额
    */
    public double m_dSloCompactBalance;
    /**
    * 融券合约费用
    */
    public double m_dSloCompactFare;
    /**
    * 融券合约利息
    */
    public double m_dSloCompactInterest;
    /**
    * 融券市值
    */
    public double m_dSloMarketValue;
    /**
    * 融券合约盈亏
    */
    public double m_dSloIncome;
    /**
    * 其它费用
    */
    public double m_dOtherFare;
    /**
    * 标的证券市值
    */
    public double m_dUnderlyMarketValue;
    /**
    * 可融资金额
    */
    public double m_dFinEnableBalance;
    /**
    * 可用保证金调整值
    */
    public double m_dDiffEnableBailBalance;
    /**
    * 买券还券冻结资金
    */
    public double m_dBuySecuRepayFrozenMargin;
    /**
    * 买券还券冻结手续费
    */
    public double m_dBuySecuRepayFrozenCommission;
}
