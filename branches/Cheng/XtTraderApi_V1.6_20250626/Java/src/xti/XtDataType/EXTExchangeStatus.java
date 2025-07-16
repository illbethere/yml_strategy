/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EXTExchangeStatus.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 市场状态
 *
 */
public enum EXTExchangeStatus {
    /**非法值*/
    EXCHANGE_STATUS_INVALID(0),
    /**开盘前*/
    EXCHANGE_STATUS_IN_BEFORE_TRADING(48),
    /**非交易*/
    EXCHANGE_STATUS_NOTRADING(49),
    /**连续交易*/
    EXCHANGE_STATUS_IN_CONTINOUS(50),
    /**集合竞价报单*/
    EXCHANGE_STATUS_AUCTION_ORDERING(51),
    /**集合竞价价格平衡*/
    EXCHANGE_STATUS_AUCTION_BALANCE(52),
    /**集合竞价撮合*/
    EXCHANGE_STATUS_AUCTION_MATCH(53),
    /**收盘*/
    EXCHANGE_STATUS_IN_CLOSED(54),
    /**仅允许撤单*/
    EXCHANGE_STATUS_ONLY_CANCEL(55),
    /**大宗交易申报*/
    EXCHANGE_STATUS_DAZONG_ORDERING(56),
    /**大宗交易意向申报*/
    EXCHANGE_STATUS_DAZONG_INTENTION_ORDERING(57),
    /**大宗交易成交申报*/
    EXCHANGE_STATUS_DAZONG_CONFIRM_ORDERING(58),
    /**大宗交易盘后定价申报*/
    EXCHANGE_STATUS_DAZONG_CLOSE_PRICE_ORDERING(59),
    /**交割申报*/
    EXCHANGE_STATUS_ONLY_GOLD_DELIVERY(60),
    /**中立仓申报*/
    EXCHANGE_STATUS_ONLY_GOLD_MIDDLE(61),
    /**盘后协议买卖*/
    EXCHANGE_STATUS_AFTER_HOURS_SALE(62),
    /**收盘集合竞价*/
    EXCHANGE_STATUS_CLOSING_AUCTION_MATCH(63),
    /**盘后定价申报*/
    EXCHANGE_STATUS_CLOSE_PRICE_ORDERING(64);

    public final int value;
    
    EXTExchangeStatus(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
