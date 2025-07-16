package xti.XtDataType;

/**
 * 
 * 订阅行情平台类型
 *
 */
public enum EXTOfferStatus {
	/**实盘*/
    XT_OFFER_STATUS_SP(48),    
    /**模拟盘*/
    XT_OFFER_STATUS_MN(49); 
    
    public final int value;
    
    EXTOfferStatus(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}