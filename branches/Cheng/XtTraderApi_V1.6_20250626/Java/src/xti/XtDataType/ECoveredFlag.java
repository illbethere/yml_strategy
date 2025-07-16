/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   ESideFlag.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 备兑标志
 *
 */
public enum ECoveredFlag {
	/**非备兑*/
    COVERED_FLAG_FALSE('0'),    
    /**备兑*/
    COVERED_FLAG_TRUE('1');     

    public final char value;
    
    ECoveredFlag(char value) {
        this.value = value;
    }
    
    public char value() {
        return this.value;
    }
}
