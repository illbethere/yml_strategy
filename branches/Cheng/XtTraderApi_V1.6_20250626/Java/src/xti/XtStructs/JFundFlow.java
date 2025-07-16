/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JAccountDetail.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EMoneyType;

/**
* JFundFlow
* 用户下资金流水信息
*/
public class JFundFlow{
	/**
	 * 资金账户ID，股票，两融，深港通，沪港通，个股期权
	 */
	public String m_strAccountID;

	/**
	 * 发生日期，股票，两融，深港通，沪港通，个股期权
	 */
	public int m_nBizDate;

	/**
	 * 发生时间，股票，两融，深港通，沪港通，个股期权
	 */
	public int m_nBizTime;

	/**
	 * 流水序号，股票，两融，深港通，沪港通，个股期权
	 */
	public String m_strSerialNo;

	/**
	 * 业务名称，股票，两融，深港通，沪港通，个股期权
	 */
	public String m_strBizName;

	/**
	 * 发生金额，股票，两融，深港通，沪港通，个股期权
	 */
	public double m_dBizBalance;

	/**
	 * 剩余金额，股票，两融，深港通，沪港通，个股期权
	 */
	public double m_dBalance;

	/**
	 * 币种，股票，两融，深港通，沪港通，个股期权
	 */
	public EMoneyType m_eMoneyType; // 假设EMoneyType是一个枚举类型

	/**
	 * 市场，股票，两融，深港通，沪港通，个股期权
	 */
	public String m_strMarket;

	/**
	 * 合约，股票，两融，深港通，沪港通，个股期权
	 */
	public String m_strInstrument;

	/**
	 * 合约名称，股票，两融
	 */
	public String m_strInstrumentName;

	/**
	 * 业务类型，股票，两融
	 */
	public String m_strBizType;

	/**
	 * 成交价格，股票，两融
	 */
	public double m_dBizPrice;
	/**
	 * 成交金额，股票，两融
	 */
	public double m_dBizPriceBalance;

	/**
	 * 手续费，股票，两融
	 */
	public double m_dCommission;

	/**
	 * 印花税，股票，两融
	 */
	public double m_dStampTax;

	/**
	 * 过户费，股票，两融
	 */
	public double m_dTransFee;

	/**
	 * 其他费用，股票，两融
	 */
	public double m_dOtherFee;

	/**
	 * 发生数量/金额，股票，两融
	 */
	public double m_dChangeAmount;

	/**
	 * 剩余数量/金额，股票，两融
	 */
	public double m_dPostAmount;

	/**
	 * 委托价格，股票，两融
	 */
	public double m_dBizOrderPrice;

	/**
	 * 委托数量，股票，两融
	 */
	public double m_dBizOrderAmount;

	/**
	 * 股东账号，股票，两融
	 */
	public String m_strStockAccount;

	/**
	 * 成交序列号，股票，两融
	 */
	public String m_strBizNo;

	/**
	 * 委托号，股票，两融
	 */
	public String m_strEntrustNo;

	/**
	 * 买卖方向，股票，两融
	 */
	public String m_strEntrustBS;

	/**
	 * 备注，股票，两融
	 */
	public String m_strNotes;

    /**
    * 设置币种
    * @param m_eMoneyType 币种
    */
    public void setM_eMoneyType(EMoneyType m_eMoneyType) {
        this.m_eMoneyType = m_eMoneyType;
    }
}
