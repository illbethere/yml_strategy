/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EVolumeCondition.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 期货数量条件单类型
 *
 */
public enum EVolumeCondition {
	/**任何数量*/
    VOLUME_CONDITION_ANY(1),      
    /**最小数量*/
    VOLUME_CONDITION_MIN(2),      
    /**全部数量*/
    VOLUME_CONDITION_TOTAL(3);    

    public final int value;
    EVolumeCondition(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
