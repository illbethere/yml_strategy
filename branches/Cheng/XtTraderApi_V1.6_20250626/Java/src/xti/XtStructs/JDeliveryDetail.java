/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JDeliveryDetail.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

/**
* JDeliveryDetail类
* 账号结算单信息
*/
public class JDeliveryDetail{
    /**
    * 资金账号ID
    */
    public String m_strAccountID;
    /**
    * 账号key
    */
    public int m_strAccountKey;
    /**
    * 账号类型
    */
    public int m_nAccountType;
    /**
    * 成交日期
    */
    public int m_nBizDate;
    /**
    * 成交时间
    */
    public int m_nBizTime;
    /**
    * 交易所代码
    */
    public String m_strExchangeID;
    /**
    * 交易所名称
    */
    public String m_strExchangeName;
    /**
    * 合约代码
    */
    public String m_strInstrumentID;
    /**
    * 合约名称
    */
    public String m_strInstrumentName;
    /**
    * 操作
    */
    public String m_strEntrustBS;
    /**
    * 操作名称
    */
    public String m_strEntrustBSName;
    /**
    * 成交数量
    */
    public double m_dBizAmount;
    /**
    * 成交价格
    */
    public double m_dBizPrice;
    /**
    * 成交金额
    */
    public double m_dBizBalance;
    /**
    * 委托号
    */
    public String m_strEntrustNo;
    /**
    * 成交序号
    */
    public String m_strBizNo;
    /**
    * 手续费
    */
    public double m_dCommission;
    /**
    * 印花税
    */
    public double m_dStampTax;
    /**
    * 委托日期  股票期权和港股特有
    */
    public int m_nEntrustDate;
    /**
    * 委托时间  股票期权和港股特有
    */
    public int m_nEntrustTime;
    /**
    * 记录序列号  股票期权和港股特有
    */
    public String m_strPositionStr;
    /**
    * 币种类型  股票期权和港股特有
    */
    public String m_strMoneyType;
    /**
    * 业务类型  股票期权和港股特有
    */
    public String m_strBizName;
    /**
    * 其他杂费  股票期权和股票特有
    */
    public double m_dTransFee;
    /**
    * 股东账号  股票和港股特有
    */
    public String m_strStockAccount;
    /**
    * 资金余额  股票和港股特有
    */
    public double m_dPostBalance;
    /**
    * 股份余额  股票和港股特有
    */
    public double m_dPostAmount;
    /**
    * 合约账号  股票期权特有
    */
    public String m_strContractAccount;
    /**
    * 币种  股票期权特有
    */
    public String m_strMoneyName;
    /**
    * 开平标识  股票期权特有
    */
    public String m_strOpenFlag;
    /**
    * 开平标识名称  股票期权特有
    */
    public String m_strOpenFlagName;
    /**
    * 备兑标记  股票期权特有
    */
    public String m_strCoveredFlag;
    /**
    * 备兑标记名称  股票期权特有
    */
    public String m_strCoveredFlagName;
    /**
    * 成交类型  股票期权特有
    */
    public String m_strBizType;
    /**
    * 备注  股票期权特有
    */
    public String m_strRemark;
    /**
    * 清算日期  港股特有
    */
    public int m_nClearDate;
    /**
    * 业务代码  港股特有
    */
    public int m_nBizFlag;
    /**
    * 客户姓名  港股特有
    */
    public String m_strCustName;
    /**
    * 合同序号  港股特有
    */
    public String m_strOrderId;
    /**
    * 委托数量  港股特有
    */
    public int m_nEntrustAmount;
    /**
    * 委托价格  港股特有
    */
    public double m_dEntrustPrice;
    /**
    * 成交笔数  港股特有
    */
    public int m_nbizTimes;
    /**
    * 成交状态  港股特有
    */
    public String m_strBizStatus;
    /**
    * 清算金额  港股特有
    */
    public double m_dFundEffect;
    /**
    * 标准手续费  港股特有
    */
    public double m_dStandardCommission;
    /**
    * 股份交收费  港股特有
    */
    public double m_dShareFee;
    /**
    * 交易费  港股特有
    */
    public double m_dTradeFee;
    /**
    * 前台费用  港股特有
    */
    public double m_dFrontFee;
    /**
    * 交易系统使用费用  港股特有
    */
    public double m_dSysUsageFee;
    /**
    * 交易征费  港股特有
    */
    public double m_dLevyFee;
    /**
    * m_dSettRate  港股特有
    */
    public double 结算汇率;
    /**
    * 结算单日期  期货和期货期权特有
    */
    public String m_strDate;
    /**
    * 结算单表  期货和期货期权特有
    */
    public String m_StrSettlementInfo;

}
