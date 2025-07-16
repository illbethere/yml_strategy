/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EEntrustTypes.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 委托类型
 *
 */
public enum EEntrustTypes {
	/**买卖*/
    ENTRUST_BUY_SELL(48),               
    /**查询*/
    ENTRUST_QUERY(49),                  
    /**撤单*/
    ENTRUST_CANCEL(50),                 
    /**补单*/
    ENTRUST_APPEND(51),                 
    /**确认*/
    ENTRUST_COMFIRM(52),                
    /**大宗*/
    ENTRUST_BIG(53),                    
    /**融资委托*/
    ENTRUST_FIN(54),                    
    /**融券委托*/
    ENTRUST_SLO(55),                    
    /**信用平仓*/
    ENTRUST_CLOSE(56),                  
    /**信用普通委托*/
    ENTRUST_CREDIT_NORMAL(57),          
    /**撤单补单*/
    ENTRUST_CANCEL_OPEN(58),            
    /**行权*/
    ENTRUST_TYPE_OPTION_EXERCISE(59),   
    /**锁定*/
    ENTRUST_TYPE_OPTION_SECU_LOCK(60),  
    /**解锁*/
    ENTRUST_TYPE_OPTION_SECU_UNLOCK(61),
    /**组合行权*/
    ENTRUST_TYPE_OPTION_COMB_EXERCISE(65),         
    /**构建组合策略持仓*/
    ENTRUST_TYPE_OPTION_BUILD_COMB_STRATEGY(66),   
    /**解除组合策略持仓*/
    ENTRUST_TYPE_OPTION_RELEASE_COMB_STRATEGY(67); 

    public final int value;
    
    EEntrustTypes(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
