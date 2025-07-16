/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EXTSubjectsStatus.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 两融标的状态
 *
 */
public enum EXTSubjectsStatus {
	/**正常*/
    SUBJECTS_STATUS_NORMAL(48),     
    /**暂停*/
    SUBJECTS_STATUS_PAUSE(49),      
    /**非标的*/
    SUBJECTS_STATUS_NOT(50);        

    public final int value;
    
    EXTSubjectsStatus(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
