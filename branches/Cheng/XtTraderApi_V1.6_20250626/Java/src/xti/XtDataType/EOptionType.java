/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EOptionType.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 股票期权合约类型
 *
 */
public enum EOptionType {
	/**认购合约*/
    OPTION_TYPE_CALL(48),      
    /**认沽合约*/
    OPTION_TYPE_PUT(49);       

    public final int value;
    
    EOptionType(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
