/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JPortfolioInfo.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EPortfolioType;

/**
* JPortfolioInfo类
* 投资组合信息
*/
public class JPortfolioInfo{
    /**
    * 投组类型编号
    */
    public int m_nPortfolioID;
    /**
    * 投资组合名称
    */
    public String m_strName;
    /**
    * 策略名称
    */
    public String m_strStrategy;
    /**
    * 备注
    */
    public String m_strRemark;
    /**
    * 账号key
    */
    public String m_strAccountKey;
    /**
    * 产品编号
    */
    public int m_nProductID;
    /**
    * 创建日期
    */
    public int m_nCreateDate;
    /**
    * 用户编号
    */
    public int m_nUserId;
    /**
    * 投资组合停用状态
    */
    public int m_nStatus;
    /**
    * 初始资产
    */
    public double m_dInitBalance;
    /**
    * 投组类型
    */
    public EPortfolioType m_eType;

    /**
    * 设置投组类型
    * @param m_eType 投组类型
    */
    public void setM_eType(EPortfolioType m_eType) {
        this.m_eType = m_eType;
    }
}
