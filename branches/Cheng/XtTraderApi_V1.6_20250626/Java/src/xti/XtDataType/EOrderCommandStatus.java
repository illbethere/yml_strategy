/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EOrderCommandStatus.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 指令状态
 *
 */
public enum EOrderCommandStatus
	/**风控检查中*/{
    OCS_CHECKING(-1),          
    /**审批中*/
    OCS_APPROVING(0),          
    /**已驳回*/
    OCS_REJECTED(1),           
    /**运行中*/
    OCS_RUNNING(2),            
    /**撤销中*/
    OCS_CANCELING(3),          
    /**已完成*/
    OCS_FINISHED(4),           
    /**已停止*/
    OCS_STOPPED(5),            
    /**强制撤销*/
    OCS_FROCE_COMPLETED(6),    
    /**风控驳回*/
    OCS_CHECKFAILED(7);        

    public final int value;
    
    EOrderCommandStatus(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
