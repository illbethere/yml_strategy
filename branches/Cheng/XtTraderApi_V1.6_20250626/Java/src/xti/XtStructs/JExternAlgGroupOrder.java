/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   ExternAlgGroupOrder.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

/**
* ExternAlgGroupOrder类
* 组合外部算法单下单请求数据
* 组合算法单最大支持 1000只股票
*/
public class JExternAlgGroupOrder{
    /**
    * 组合外部算法单下单配置
    */
    public JExternAlgorithmOrder m_orderParam;
    /**
    * 市场列表
    */
    public String[] m_strMarket;
    /**
    * 证券代码
    */
    public String[] m_strInstrument;
    /**
    * 每只股票的下单量
    */
    public int[] m_nVolume;
    /**
    * 每只股票的下单类型
    */
    public int[] m_eOperationType;
    /**
    * 股票只数
    */
    public int m_nOrderNum;
    /**
    * 投资备注
    */
    public String m_strRemark;
    
    /**
    * JExternAlgGroupOrder构造函数
    */
    public JExternAlgGroupOrder()
    {
        // 组合外部算法单最大支持 1000只股票
        m_orderParam = new JExternAlgorithmOrder();
        m_strMarket = new String[1000];
        m_strInstrument = new String[1000];
        m_nVolume = new int[1000];
        m_eOperationType = new int[1000];
        m_nOrderNum = 0;
        m_strRemark = "";
    }
}