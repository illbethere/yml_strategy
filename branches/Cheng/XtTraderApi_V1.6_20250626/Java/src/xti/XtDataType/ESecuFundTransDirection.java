/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   ESecuFundTransDirection.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 资金股份划拨划拨方向
 *
 */
public enum ESecuFundTransDirection {
    /**从普通柜台拨入到极速柜台*/
    SECUFUNDTRANS_TRANSFER_NORMAL_TO_FAST(0),
    /**从极速柜台拨出到普通柜台*/
    SECUFUNDTRANS_TRANSFER_FAST_TO_NORMAL(1),
    /**上海划到深圳(节点划拨)*/
    SECUFUNDTRANS_TRANSFER_SH_TO_SZ(2),
    /**深圳划到上海(节点划拨)*/
    SECUFUNDTRANS_TRANSFER_SZ_TO_SH(3);    

    public final int value;
    ESecuFundTransDirection(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
