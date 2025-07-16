/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   ETransDirection.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 银证转账方向
 *
 */
public enum ETransDirection {
	/**银行转证券*/
	TRANS_DIRECTION_BANK_TO_SECURITIES(49),
    /**证券转银行*/
	TRANS_DIRECTION_SECURITIES_TO_BANK(50),
    /**快速转集中*/
	TRANS_DIRECTION_QUICK_TO_CENTER(51),
    /**集中转快速*/
	TRANS_DIRECTION_CENTER_TO_QUICK(52),
    /**查询*/
	TRANS_DIRECTION_QUERY(53);    

    public final int value;
    ETransDirection(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
