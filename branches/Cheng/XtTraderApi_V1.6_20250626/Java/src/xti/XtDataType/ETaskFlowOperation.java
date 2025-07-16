/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   ETaskFlowOperation.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/***
 * 
 * 任务操作
 *
 */
public enum ETaskFlowOperation {
	/**暂停*/
    TFO_PAUSE(5),      
    /**恢复*/
    TFO_RESUME(6);      

    ETaskFlowOperation(int value) {
        this.value = value;
    }
    public final int value;
    public int value() {
        return this.value;
    }
}
