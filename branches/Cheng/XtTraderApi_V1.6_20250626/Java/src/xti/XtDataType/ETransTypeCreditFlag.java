/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   ETransTypeCreditFlag.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 股份划拨信用划拨类别
 *
 */
public enum ETransTypeCreditFlag {
    /**操作客户股份划拨，默认送0*/
    TRANS_TRANSFER_SHARE(0),
    /**操作客户专向头寸调拨*/
    TRANS_TRANSFER_SPECIAL_POSITIONS(1),
    /**融资融券客户股份调拨*/
    TRANS_TRANSFER_CREDIT_SHARE(2);  

    public final int value;
    ETransTypeCreditFlag(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
