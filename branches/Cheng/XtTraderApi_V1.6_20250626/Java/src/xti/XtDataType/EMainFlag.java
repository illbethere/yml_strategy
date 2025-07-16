/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EMainFlag.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 主副标记
 *
 */
public enum EMainFlag {
	/**副账户*/
	MAIN_FLAG_VICE(48),              
    /**主账户*/
    MAIN_FLAG_MAIN(49);      

    public final int value;
    
    EMainFlag(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
