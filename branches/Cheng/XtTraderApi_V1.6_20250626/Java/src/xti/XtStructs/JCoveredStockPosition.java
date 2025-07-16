/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JCoveredStockPosition.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

/**
* JCoveredStockPosition类
* 期权账号备兑持仓数据
*/
public class JCoveredStockPosition{
    /**
    * 资金账号ID
    */
    public String m_strAccountID;
    /**
    * 交易类别
    */
    public String m_strExchangeID;
    /**
    * 市场名字
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
    * 总持仓量
    */
    public int m_nTotalAmount;
    /**
    * 锁定量
    */
    public int m_nLockAmount;
    /**
    * 未锁定量
    */
    public int m_nUnlockAmount;
}
