/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EXTPlatForm.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 平台类型
 */
public enum EXTPlatForm {
	/**中投实盘*/
    PLATFORM_ZTSP(10001),          
    /**中投模拟*/
    PLATFORM_ZTMN(11001),          
    /**中金实盘*/
    PLATFORM_ZJSP(10002),          
    /**长江实盘*/
    PLATFORM_CJSP(10004),          
    /**东方实盘*/
    PLATFORM_DFSP(10003),          
    /**东方模拟*/
    PLATFORM_DFMN(11003),          
    /**中信实盘*/
    PLATFORM_ZXSP(10005),          
    /**中信模拟*/
    PLATFORM_ZXMN(11005),          
    /**齐鲁实盘*/
    PLATFORM_QLSP(10006),          
    /**齐鲁模拟*/
    PLATFORM_QLMN(11006),          
    /**华泰实盘*/
    PLATFORM_HUATAISP(10007),      
    /**华泰模拟*/
    PLATFORM_HUATAIMN(11007),      
    /**国信实盘*/
    PLATFORM_GXSP(10008),          
    /**国信模拟*/
    PLATFORM_GXMN(11008),          
    /**迅投自有股票*/
    PLATFORM_XTGPMN(11009),        
    /**申银万国实盘*/
    PLATFORM_SWSP(10010),          
    /**申银万国模拟*/
    PLATFORM_SWMN(11010),          
    /**国泰君安实盘*/
    PLATFORM_GTSP(10011),          
    /**UFX实盘*/
    PLATFORM_UFXSP(10012),         
    /**UFX模拟*/
    PLATFORM_UFXMN(11012),         
    /**广州证券实盘*/
    PLATFORM_GZSP(10013),          
    /**广州证券模拟*/
    PLATFORM_GZMN(11013),          
    /**光大证券实盘*/
    PLATFORM_GDSP(10014),          
    /**光大证券模拟*/
    PLATFORM_GDMN(11014),          
    /**山西证券实盘*/
    PLATFORM_SXSP(10015),          
    /**山西证券模拟*/
    PLATFORM_SXMN(11015),          
    /**海通证券新API实盘*/
    PLATFORM_HAITONGSP(10016),     
    /**海通证券新API模拟*/
    PLATFORM_HAITONGMN(11016),     
    /**海通证券SPX接口实盘*/
    PLATFORM_HAITONGSPXSP(10017),  
    /**海通证券SPX接口模拟*/
    PLATFORM_HAITONGSPXMN(11017),  
    /**银河证券KCXP实盘*/
    PLATFORM_YHSP(10018),          
    /**银河证券KCXP模拟*/
    PLATFORM_YHMN(11018),          
    /**银河证券顶点柜台实盘*/
    PLATFORM_YHDDSP(10019),        
    /**银河证券顶点柜台模拟*/
    PLATFORM_YHDDMN(11019),        
    /**O32虚拟broker*/
    PLATFORM_O32DB(10020),         
    /**O32虚拟broker模拟*/
    PLATFORM_O32DBMN(11020),       
    /**兴业证券CTP柜台实盘*/
    PLATFORM_XINGYESP(10021),      
    /**兴业证券CTP柜台模拟*/
    PLATFORM_XINGYEMN(11021),      
    /**广发证券顶点柜台实盘*/
    PLATFORM_GUANGFASP(10022),     
    /**广发证券顶点柜台模拟*/
    PLATFORM_GUANGFAMN(11022),     
    /**东兴证券顶点柜台实盘*/
    PLATFORM_DONGXINGSP(10023),    
    /**东兴证券顶点柜台模拟*/
    PLATFORM_DONGXINGMN(11023),    
    /**迅投高级行情*/
    PLATFORM_XTGJHQ(10000),        
    /**股票分界线*/
    PLATFORM_MAX_STOCK(19999),     
    /**CTP期货实盘*/
    PLATFORM_CTPSP(20001),         
    /**CTP期货模拟*/
    PLATFORM_CTPMN(21001),         
    /**华海期货实盘*/
    PLATFORM_HHSP(20002),          
    /**华海期货模拟*/
    PLATFORM_HHMN(21002),          
    /**金仕达期货实盘*/
    PLATFORM_KSSP(20010),          
    /**金仕达期货模拟*/
    PLATFORM_KSMN(21010),          
    /**迅投自有期货*/
    PLATFORM_XTXHMN(21009),        
    /**资管实盘*/
    PLATFORM_ZGSP_FUTURE(21111),   
    /**资管模拟*/
    PLATFORM_ZGMN_FUTURE(21112),   
    /**期货分界线*/
    PLATFORM_MAX_FUTURE(29999);    

    public final int value;
    
    EXTPlatForm(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
