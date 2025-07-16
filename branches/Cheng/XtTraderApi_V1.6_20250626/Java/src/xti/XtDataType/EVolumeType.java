/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EVolumeType.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 下单量类型
 *
 */
public enum EVolumeType {
    VOLUME_INVALID(-1),
    /**卖一至卖五之和*/
    VOLUME_SALE12345(0),    
    /**卖一至卖四之和*/
    VOLUME_SALE1234(1),     
    /**卖一至卖三之和*/
    VOLUME_SALE123(2),      
    /**卖一至卖二之和*/
    VOLUME_SALE12(3),       
    /**卖一*/
    VOLUME_SALE1(4),        
    /**买一*/
    VOLUME_BUY1(5),         
    /**买一至买二之和*/
    VOLUME_BUY12(6),        
    /**买一至买三之和*/
    VOLUME_BUY123(7),       
    /**买一至买四之和*/
    VOLUME_BUY1234(8),      
    /**买一至买五之和*/
    VOLUME_BUY12345(9),     
    /**指定量*/
    VOLUME_FIX(10),         
    /**剩余量*/
    VOLUME_LEFT(11),        
    /**持仓数量*/
    VOLUME_POSITION(12),    
    _C_VOLUME_COUNT(13);

    public final int value;
    
    EVolumeType(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
