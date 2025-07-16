/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EProductClass.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 投组类型
 *
 */
public enum EProductClass {
	/**其他合约*/
	PRODECT_CLASS_NORMAL(0),           
    /**期货合约*/
	PRODECT_CLASS_FUTURE(1),          
    /**期货期权合约*/
    PRODECT_CLASS_FUTURE_OPTION(2);    

    public final int value;
    
    EProductClass(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
