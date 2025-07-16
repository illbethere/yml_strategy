/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EProductClass.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 指令跨日开关
 *
 */
public enum EXTCommandDateLimit {
	/**不跨日*/
	XT_COMMAND_LIMIT_NO_OVER_DAY(0),           
    /**将跨日指令*/
	XT_COMMAND_LIMIT_CROSS_OVER_DAY(1),          
    /**已经跨日的指令*/
    XT_COMMAND_LIMIT_ALREADY_CROSSED(2);    

    public final int value;
    
    EXTCommandDateLimit(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
