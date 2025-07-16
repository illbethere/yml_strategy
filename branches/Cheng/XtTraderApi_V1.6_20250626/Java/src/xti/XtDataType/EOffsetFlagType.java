/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EOffsetFlagType.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 开平标志
 *
 */
public enum EOffsetFlagType {
	/**未知*/
    EOFF_THOST_FTDC_OF_INVALID(-1),        
    /**开仓，对应股票买入*/
    EOFF_THOST_FTDC_OF_Open(48),           
    /**平仓，对应股票卖出*/
    EOFF_THOST_FTDC_OF_Close(49),          
    /**强平*/
    EOFF_THOST_FTDC_OF_ForceClose(50),     
    /**平今*/
    EOFF_THOST_FTDC_OF_CloseToday(51),     
    /**平昨*/
    EOFF_THOST_FTDC_OF_CloseYesterday(52), 
    /**强减*/
    EOFF_THOST_FTDC_OF_ForceOff(53),       
    /**本地强平*/
    EOFF_THOST_FTDC_OF_LocalForceClose(54),
    /**质押入库*/
    EOFF_THOST_FTDC_OF_PLEDGE_IN(81),      
    /**质押出库*/
    EOFF_THOST_FTDC_OF_PLEDGE_OUT(66),     
    /**股票配股*/
    EOFF_THOST_FTDC_OF_ALLOTMENT(67),      
    /**行权*/
    EOFF_THOST_FTDC_OF_OPTION_EXERCISE(68),
    /**锁定*/
    EOFF_THOST_FTDC_OF_OPTION_LOCK(69),    
    /**解锁*/
    EOFF_THOST_FTDC_OF_OPTION_UNLOCK(70);  

    public final int value;
    
    EOffsetFlagType(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
