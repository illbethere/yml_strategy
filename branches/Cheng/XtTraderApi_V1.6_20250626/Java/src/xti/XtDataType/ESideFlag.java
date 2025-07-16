/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   ESideFlag.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 期权持仓类型
 *
 */
public enum ESideFlag {
	/**权利*/
    SIDE_FLAG_RIGHT(48),        
    /**义务*/
    SIDE_FLAG_DUTY(49),         
    /**备兑*/
    SIDE_FLAG_COVERED(50);      

    public final int value;
    
    ESideFlag(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
