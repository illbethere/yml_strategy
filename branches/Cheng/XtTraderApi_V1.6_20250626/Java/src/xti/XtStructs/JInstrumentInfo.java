/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JInstrumentInfo.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EProductClass;
import xti.XtDataType.EXtMaxMarginSideAlgorithmType;
import xti.XtDataType.EXtSuspendedType;
import xti.XtDataType.EXtExDivdendType;
import xti.XtDataType.EStockType;

/**
* JInstrumentInfo
* 合约信息
*/
public class JInstrumentInfo{
    /**
    * 合约代码
    */
    public String m_strInstrumentID;
    /**
    * 合约名称
    */
    public String m_strInstrumentName;
    /**
    * 交易所代码
    */
    public String m_strExchangeID;
    /**
    * 合约在交易所的代码
    */
    public String m_strExchangeInstID;
    /**
    * 品种代码
    */
    public String m_strProductID;
    /**
    * 创建日
    */
    public String m_strCreateDate;
    /**
    * 上市日
    */
    public String m_strOpenDate;
    /**
    * 到期日
    */
    public String m_strExpireDate;
    /**
    * 开始交割日
    */
    public String m_strStartDelivDate;
    /**
    * 结束交割日
    */
    public String m_strEndDelivDate;
    /**
    * 期权标的代码
    */
    public String m_strOptUndlCode;
    /**
    * 期权标的市场
    */
    public String m_strOptUndlMarket;
    /**
    *合约类型
    */
    public EProductClass m_eProductClass;
    /**
    * 交割年份
    */
    public int m_nDeliveryYear;
    /**
    * 交割月
    */
    public int m_nDeliveryMonth;
    /**
    * 市价单最大下单量
    */
    public int m_nMaxMarketOrderVolume;
    /**
    * 市价单最小下单量
    */
    public int m_nMinMarketOrderVolume;
    /**
    * 限价单最大下单量
    */
    public int m_nMaxLimitOrderVolume;
    /**
    * 限价单最小下单量
    */
    public int m_nMinLimitOrderVolume;
    /**
    * 合约数量乘数
    */
    public int m_nVolumeMultiple;
    /**
    * 当前是否交易
    */
    public int m_nIsTrading;
    /**
    * 最小变动价位
    */
    public double m_dPriceTick;
    /**
    * 多头保证金率
    */
    public double m_dLongMarginRatio;
    /**
    * 空头保证金率
    */
    public double m_dShortMarginRatio;
    /**
    * 涨停价
    */
    public double m_dUpStopPrice;
    /**
    * 跌停价
    */
    public double m_dDownStopPrice;
    /**
    * 前结算
    */
    public double m_dSettlementPrice;
    /**
    * 是否使用大额单边保证金算法
    */
    public EXtMaxMarginSideAlgorithmType m_eMaxMarginSideAlgorithm;
    /**
    * 停牌状态
    */
    public EXtSuspendedType m_eSuspendedType;
    /**
    * 除权除息标志
    */
    public EXtExDivdendType m_eExDivdendType;
    /**
    * 期权行权价
    */
    public double m_dOptExercisePrice;
    /**
    * 合约种类(个股期权：0认购，1认沽)
    */
    public int m_nCallOrPut;
	/**
    * 保证金单位
    */
    public double m_dMarginUnit;
    /**
     * 期权标的证券名称
     */
    public String m_strOptUndlName;
    /**
     * 期权合约单位
     */
    public int m_nOptUnit;
    /**
    * 证券类别
    */
    public EStockType m_eStockType;
   /**
    * 合约类型
    * @param m_eProductClass 合约类型
    */
    public void setM_eProductClass(EProductClass m_eProductClass) {
        this.m_eProductClass = m_eProductClass;
    }

    /**
    * 是否使用大额单边保证金算法
    * @param m_eMaxMarginSideAlgorithm 是否使用大额单边保证金算法
    */
    public void setM_eMaxMarginSideAlgorithm(EXtMaxMarginSideAlgorithmType m_eMaxMarginSideAlgorithm) {
        this.m_eMaxMarginSideAlgorithm = m_eMaxMarginSideAlgorithm;
    }

    /**
    * 停牌状态
    * @param m_eSuspendedType 停牌状态
    */
    public void setM_eSuspendedType(EXtSuspendedType m_eSuspendedType) {
        this.m_eSuspendedType = m_eSuspendedType;
    }

    /**
    * 除权除息标志
    * @param m_eExDivdendType 除权除息标志
    */
    public void setM_eExDivdendType(EXtExDivdendType m_eExDivdendType) {
        this.m_eExDivdendType = m_eExDivdendType;
    }

    /**
     * 证券类别
     * @param m_eStockType 证券类别
     */
    public void setM_eStockType(EStockType m_eStockType) {
        this.m_eStockType = m_eStockType;
    }
}
