/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JStockComPosition.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

/**
* JStockComPosition类
* 普通柜台持仓信息
*/
public class JStockComPosition{
    /**
    * 资金账户ID
    */
    public String m_strAccountID;
    /**
    * 账号key
    */
    public String m_strAccountKey;
    /**
    * 市场代码
    */
    public String m_strExchangeID;
    /**
    * 合约代码
    */
    public String m_strInstrumentID;
    /**
    * 合约名称
    */
    public String m_strInstrumentName;
    /**
    * 持仓量
    */
    public int m_nVolume;
    /**
    * 可用数量
    */
    public int m_nCanUseVolume;
    /**
    * 成本价
    */
    public double m_dLastPrice;
    /**
    * 盈亏
    */
    public double m_dIncome;
    /**
    * 盈亏比例
    */
    public double m_dIncomeRate;
    /**
    * 股手标记
    */
    public String m_strHandFlag;
    /**
    * 证券账号
    */
    public String m_strStockAccount;
    /**
    * 市值
    */
    public double m_dInstrumentValue;
    /**
    * 成本总额
    */
    public double m_dCostBalance;
    /**
    * 在途量
    */
    public int m_nOnRoadVolume;
    /**
    * 申赎可用量
    */
    public int m_nPREnableVolume;
    /**
    * 是否是从极速接口查到的
    */
    public boolean m_bFast;
}
