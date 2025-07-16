/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EBrokerLoginStatus.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 账号状态
 *
 */
public enum EBrokerLoginStatus {
	/**未知*/
    BROKER_LOGIN_STATUS_INALID(-1),
    /**可用，初始化完成*/
    BROKER_LOGIN_STATUS_OK(0),             
    /**连接中*/
    BROKER_LOGIN_STATUS_WAITING_LOGIN(1),  
    /**登录中*/
    BROKER_LOGIN_STATUS_LOGINING(2),       
    /**失败*/
    BROKER_LOGIN_STATUS_FAIL(3),           
    /**在初始化中*/
    BROKER_LOGIN_STATUS_INITING(4),        
    /**数据刷新校正中*/
    BROKER_LOGIN_STATUS_CORRECTING(5),     
    /**收盘后*/
    BROKER_LOGIN_STATUS_CLOSED(6);         

    public final int value;
    
    EBrokerLoginStatus(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
