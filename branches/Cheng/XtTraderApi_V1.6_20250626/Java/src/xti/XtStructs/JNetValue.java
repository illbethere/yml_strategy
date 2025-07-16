/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JNetValue.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

/**
* JNetValue类
* 产品净值数据
*/
public class JNetValue{
    /**
    * 迅投产品ID
    */
    public int m_nProductId;
    /**
    * 产品类型 1-普通基金 2-分级基金
    */
    public int m_nTypes;
    /**
    * 产品净资产, 产品净值
    */
    public double m_dTotalNetValue;
    /**
    * 母基金单位净值
    */
    public double m_dNetValue;
    /**
    * B级基金单位净值
    */
    public double m_dBNetValue;
    /**
    * 更新时间
    */
    public int m_nUpdateTime;

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
