/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JStockOptionCombPositionDetail.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EOptionType;
import xti.XtDataType.ESideFlag;

/**
* JStockOptionCombPositionDetail类
* 期权账号组合持仓数据
*/
public class JStockOptionCombPositionDetail{
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
    * 合约账号
    */
    public String m_strContractAccount;
    /**
    * 组合编号
    */
    public String m_strCombID;
    /**
    * 组合策略编码
    */
    public String m_strCombCode;
    /**
    * 组合策略名称
    */
    public String m_strCombCodeName;
    /**
    * 总持仓量
    */
    public int m_nVolume;
    /**
    * 冻结数量
    */
    public int m_nFrozenVolume;
    /**
    * 可用数量
    */
    public int m_nCanUseVolume;
    /**
    * 合约一
    */
    public String m_strFirstCode;
    /**
    * 合约一类型
    */
    public EOptionType m_eFirstCodeType;
    /**
    * 合约一名称
    */
    public String m_strFirstCodeName;
    /**
    * 合约一持仓类型
    */
    public ESideFlag m_eFirstCodePosType;
    /**
    * 合约一数量
    */
    public int m_nFirstCodeAmt;
    /**
    * 合约二
    */
    public String m_strSecondCode;
    /**
    * 合约二类型
    */
    public EOptionType m_eSecondCodeType;
    /**
    * 合约二名称
    */
    public String m_strSecondCodeName;
    /**
    * 合约二持仓类型
    */
    public ESideFlag m_eSecondCodePosType;
    /**
    * 合约二数量
    */
    public int m_nSecondCodeAmt;
    /**
    * 占用保证金
    */
    public double m_dCombBailBalance;

    /**
    * 设置合约一类型
    * @param m_eFirstCodeType 合约一类型
    */
    public void setM_eFirstCodeType(EOptionType m_eFirstCodeType) {
        this.m_eFirstCodeType = m_eFirstCodeType;
    }

    /**
    * 设置合约一持仓类型
    * @param m_eFirstCodePosType 合约一持仓类型
    */
    public void setM_eFirstCodePosType(ESideFlag m_eFirstCodePosType) {
        this.m_eFirstCodePosType = m_eFirstCodePosType;
    }

    /**
    * 设置合约二类型
    * @param m_eSecondCodeType 合约二类型
    */
    public void setM_eSecondCodeType(EOptionType m_eSecondCodeType) {
        this.m_eSecondCodeType = m_eSecondCodeType;
    }

    /**
    * 设置合约二持仓类型
    * @param m_eSecondCodePosType 合约二持仓类型
    */
    public void setM_eSecondCodePosType(ESideFlag m_eSecondCodePosType) {
        this.m_eSecondCodePosType = m_eSecondCodePosType;
    }
}
