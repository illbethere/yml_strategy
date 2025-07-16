/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EXTSuspendedType.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 停牌标志
 *
 */
public enum EXtSuspendedType {
	/**不停牌*/
    XT_NO_SUSPENDED(0),     
    /**停牌*/
    XT_SUSPENDED(1);        

    public final int value;

    EXtSuspendedType(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
