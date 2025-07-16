/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EEntrustSubmitStatus.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 期货委托发送状态
 *
 */
public enum EEntrustSubmitStatus {
	/**已经提交*/
    ENTRUST_SUBMIT_STATUS_InsertSubmitted(48),       
    /**撤单已经提交*/
    ENTRUST_SUBMIT_STATUS_CancelSubmitted(49),       
    /**修改已经提交*/
    ENTRUST_SUBMIT_STATUS_ModifySubmitted(50),       
    /**已经接受*/
    ENTRUST_SUBMIT_STATUS_OSS_Accepted(51),          
    /**报单已经被拒绝*/
    ENTRUST_SUBMIT_STATUS_InsertRejected(52),        
    /**撤单已经被拒绝*/
    ENTRUST_SUBMIT_STATUS_CancelRejected(53),        
    /**改单已经被拒绝*/
    ENTRUST_SUBMIT_STATUS_ModifyRejected(54);        

    public final int value;
    
    EEntrustSubmitStatus(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
