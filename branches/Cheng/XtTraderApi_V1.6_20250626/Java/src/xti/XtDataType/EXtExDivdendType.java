/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EXtExDivdendType.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 除权除息标志
 *
 */
public enum EXtExDivdendType {
	/**不是除权除息*/
    XT_EXD_NORMAL(0),
    /**除权*/
    XT_EXD_RIGHT(1),
    /**除息*/
    XT_EXD_DIVDEND(2),
    /**除权除息*/
    XT_EXD_XT_RIGHT_DIVDEND(3);
    public final int value;
    
    EXtExDivdendType(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
