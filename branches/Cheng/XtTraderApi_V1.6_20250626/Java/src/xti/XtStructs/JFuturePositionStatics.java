/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JPositionStatics.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.EEntrustBS;
import xti.XtDataType.EHedgeFlagType;

/**
* JPositionStatics类
* 账号持仓统计数据
*/
public class JFuturePositionStatics{
    /**
    * 资金账号ID
    */
    public String m_strAccountID;
    /**
    * 市场代码
    */
    public String m_strExchangeID;
    /**
     * 市场名称
     */
    public String m_strExchangeName;
    /**
    * 合约品种
    */
    public String m_strProductID;
    /**
    * 合约代码
    */
    public String m_strInstrumentID;
    /**
    * 合约名称
    */
    public String m_strInstrumentName;
    /**
     * 期货多空，该字段与m_eOffsetFlag一起判断期货的报单类型。股票无用
     */
    public EEntrustBS m_nDirection;
    /**
     * 投机 套利 套保
     */
    public EHedgeFlagType m_nHedgeFlag;
    /**
     * 总持仓
     */
    public int m_nPosition;
    /**
     * 昨仓
     */
    public int m_nYestodayPosition;
    /**
     * 今仓
     */
    public int m_nTodayPosition;
    /**
     * 可平量
     */
    public int m_nCanCloseVol;
    /**
     * 持仓成本 detail的汇总
     */
    public double m_dPositionCost;
    /**
     * 持仓均价
     */
    public double m_dAvgPrice;
    /**
     * 持仓盈亏 detail的汇总
     */
    public double m_dPositionProfit;
    /**
     * 浮动盈亏 detail的汇总
     */
    public double m_dFloatProfit;
    /**
     * 开仓均价 股票不需要
     */
    public double m_dOpenPrice;
    /**
     * 已使用保证金
     */
    public double m_dUsedMargin;
    /**
     * 已使用的手续费
     */
    public double m_dUsedCommission;
    /**
     * 冻结保证金
     */
    public double m_dFrozenMargin;
    /**
     * 冻结手续费
     */
    public double m_dFrozenCommission;
    /**
     * 合约价值
     */
    public double m_dInstrumentValue;
    /**
     * 开仓次数
     */
    public int m_nOpenTimes;
    /**
     * 总开仓量 中间平仓不减
     */
    public int m_nOpenVolume;
    /**
     * 撤单次数
     */
    public int m_nCancelTimes;
    /**
     * 最新价
     */
    public double m_dLastPrice;
    /**
     * 当日涨幅
     */
    public double m_dRiseRatio;
    /**
     * 产品名称
     */
    public String m_strProductName;
    /**
     * 权利金市值
     */
    public double m_dRoyalty;
    /**
     * 到期日
     */
    public String m_strExpireDate;
    /**
     * 资产占比
     */
    public double m_dAssestWeight;
    /**
     * 当日涨幅（结）
     */
    public double m_dIncreaseBySettlement;
    /**
     * 保证金占比
     */
    public double m_dMarginRatio;
    /**
     * 浮盈比例（保证金）
     */
    public double m_dFloatProfitDivideByUsedMargin;
    /**
     * 浮盈比例（动态权益）
     */
    public double m_dFloatProfitDivideByBalance;
    /**
     * 当日盈亏(结）
     */
    public double m_dTodayProfitLoss;
    /**
     * 昨日持仓
     */
    public int m_nYestodayInitPosition;
    /**
     * 冻结权利金
     */
    public double m_dFrozenRoyalty;
    /**
     * 当日盈亏（收）
     */
    public double m_dTodayCloseProfitLoss;
    /**
     * 平仓盈亏
     */
    public double m_dCloseProfit;
    /**
     * 品种名称
     */
    public String m_strFtProductName;
    /**
     * 开仓成本
     */
    public double m_dOpenCost;
    /**
     * 保证金（预结）
     */
    public double m_dEstimateSettleProfitLoss;
    /**
     * 当日盈亏（预结）
     */
    public double m_dEstimateSettleMargin;
    /**
     * 结算价
     */
    public double m_dSettlementPrice;


    /**
    * 设置多空方向
    * @param m_nDirection 多空方向
    */
    public void setM_nDirection(EEntrustBS m_nDirection) {
        this.m_nDirection = m_nDirection;
    }

    /**
    * 设置投保标志
    * @param m_nHedgeFlag 投保标志
    */
    public void setM_nHedgeFlag(EHedgeFlagType m_nHedgeFlag) {
        this.m_nHedgeFlag = m_nHedgeFlag;
    }


}
