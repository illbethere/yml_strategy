/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EEntrustBS.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 买卖方向
 *
 */
public enum EEntrustBS {
	/**买入*/
    ENTRUST_BUY(48),           
    /**卖出*/
    ENTRUST_SELL(49),          
    /**备兑*/
    ENTRUST_COVERED(50),          
    /**质押入库*/
    ENTRUST_PLEDGE_IN(81),     
    /**质押出库*/
    ENTRUST_PLEDGE_OUT(66);    

    public final int value;
    
    EEntrustBS(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
