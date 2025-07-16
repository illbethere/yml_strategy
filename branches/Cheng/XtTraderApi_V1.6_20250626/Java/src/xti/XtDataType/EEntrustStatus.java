/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EEntrustStatus.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 委托状态
 *
 */
public enum EEntrustStatus {
	/**委托状态已经在ENTRUST_STATUS_CANCELED或以上，但是成交数额还不够，等成交回报来*/
    ENTRUST_STATUS_WAIT_END(0),             
    /**未报*/
    ENTRUST_STATUS_UNREPORTED(48),          
    /**待报*/
    ENTRUST_STATUS_WAIT_REPORTING(49),      
    /**已报*/
    ENTRUST_STATUS_REPORTED(50),            
    /**已报待撤*/
    ENTRUST_STATUS_REPORTED_CANCEL(51),     
    /**部成待撤*/
    ENTRUST_STATUS_PARTSUCC_CANCEL(52),     
    /**部撤*/
    ENTRUST_STATUS_PART_CANCEL(53),         
    /**已撤*/
    ENTRUST_STATUS_CANCELED(54),            
    /**部成*/
    ENTRUST_STATUS_PART_SUCC(55),           
    /**已成*/
    ENTRUST_STATUS_SUCCEEDED(56),           
    /**废单*/
    ENTRUST_STATUS_JUNK(57),                
    /**已受理*/
    ENTRUST_STATUS_ACCEPT(58),              
    /**已确认(担保品划转，待柜台清算)*/
    ENTRUST_STATUS_CONFIRMED(59),           
    /**已确认(协议回购和理财)*/
    ENTRUST_STATUS_DETERMINED(86),          
    /**预埋*/
    ENTRUST_STATUS_PREPARE_ORDER(87),       
    /**预埋已撤*/
    ENTRUST_STATUS_PREPARE_CANCELED(88),    
    /**未知*/
    ENTRUST_STATUS_UNKNOWN(255);            

    public final int value;
    
    EEntrustStatus(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
