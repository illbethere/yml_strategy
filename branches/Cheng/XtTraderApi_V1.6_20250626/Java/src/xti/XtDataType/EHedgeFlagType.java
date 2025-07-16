/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EHedgeFlagType.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 投保标志
 *
 */
public enum EHedgeFlagType {
	/**投机*/
    HEDGE_FLAG_SPECULATION(49),  
    /**套利*/
    HEDGE_FLAG_ARBITRAGE(50),    
    /**套保*/
    HEDGE_FLAG_HEDGE(51);        

    public final int value;
    
    EHedgeFlagType(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
