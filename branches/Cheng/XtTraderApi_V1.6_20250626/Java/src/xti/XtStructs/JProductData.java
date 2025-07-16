/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JProductData.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

/**
* JProductData类
* 产品信息数据
*/
public class JProductData {
    /**
    * 迅投产品ID
    */
    public int         m_nProductId;
    /**
    *迅投产品名称
    */
    public String      m_strProductName;
	/**
    *迅投产品代码
    */
    public String      m_strProductCode;
	/**
    *迅投产品创建日期
    */
    public String      m_strCreateDate;
    /**
    * 产品净资产, 产品净值
    */
    public double      m_dTotalNetValue;
    /**
    * 当前资金余额（期货的动态权益和证券的可用）
    */
    public double      m_dBalance;
    /**
    * 期初资金余额（期货静态权益和证券的资金余额）
    */
    public double      m_dPreBalance;
    /**
    * 期货帐号的可用资金之和
    */
    public double      m_dAvaliableFuture;
    /**
    * 期货账号占用保证金
    */
    public double      m_dCurrMargin;
    /**
    * 期货动态权益之和
    */
    public double      m_dBalancefuture;
    /**
    * 股票总市值
    */
    public double      m_dStockValue;
    /**
    * 债券总市值，期货没有
    */
    public double      m_dLoanValue;
    /**
    * 基金总市值，包括ETF和封闭式基金，期货没有
    */
    public double      m_dFundValue;
    /**
    * 回购总市值，所有回购，期货没有
    */
    public double      m_dRepurchaseValue;
	/**
    * 总负债
    */
    public double      m_dTotalDebt;

    /**
     * 产品份额
     */
    public double      m_dShare;

    /**
     * 当日产品盈亏
     */
    public double      m_dTotalIncome;

    /**
     * 产品累计盈亏
     */
    public double      m_dAccumulateIncome;

    /**
     * 产品收盘盈亏
     */
    public double      m_dCloseTotalIncome;

    /**
     * 前日产品净值
     */
    public double      m_dPrevTotalNetValue;

    /**
     * 前日单位净值
     */
    public double      m_dPrevNetValue;
}
