/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EErrorType.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 错误号
 */
public enum EErrorType {
	/** 无错误*/
    XT_ERROR_SUCCESS(0),                                    
    /** 未建立连接*/
    XT_ERROR_NET_DISCONNECTED(200000),                      
    /** 未登录*/
    XT_ERROR_NOT_LOGINED(200001),                           
    /** 初始化未完成*/
    XT_ERROR_NOT_INITIALIZED(200002),                       
    /** 超时*/
    XT_ERROR_TIME_OUT(200003),                              
    /** 未找到账号*/
    XT_ERROR_NOT_FIND_ACCOUNT(200004),                      
    /** 未找到处理函数*/
    XT_ERROR_NOT_FIND_FUNCTION(200005),                     
    /** 参数有误*/
    XT_ERROR_INVALID_PARAM(200006),                         
    /** 默认错误号*/
    XT_ERROR_DEFAULT(300000),                               
    /** 未知错误*/
    XT_ERROR_UNKNOWN(300001),                               
    /** 重复登录*/
    XT_ERROR_REPEAT_LOGIN(300002),                          
    /** md5值不匹配*/
    XT_ERROR_LOGIN_MD5_NOT_MATCH(300003),                   
    /** api版本较低*/
    XT_ERROR_LOGIN_API_VERSINO_TOO_LOW(300004),             
    /** 用户不允许登陆*/
    XT_ERROR_LOGIN_USER_NOT_ALLOWEDLOGIN(300005),           
    /** 创建指令时，解析参数失败*/
    XT_ERROR_CREATECOMMOND_PARAM(300006),                   
    /** 创建指令时，获取行情数据失败*/
    XT_ERROR_CREATECOMMOND_QUOTE(300007),                   
    /** 创建指令时，获取有关报价类型的价格失败（如最新价等）*/
    XT_ERROR_CREATECOMMOND_PRICE_TYPE(300008),              
    /** 下单超过流量控制*/
    XT_ERROR_ORDER_FLOW_CONTROL(300009),                    
    /** 股票期货业务没有授权*/
    XT_ERROR_ORDER_NOT_AUTHORIZE_STOCK_FUTURE(300010),      
    /** 股票期权业务没有授权*/
    XT_ERROR_ORDER_NOT_AUTHORIZE_STOCKOPTION(300011),       
    /** 信用业务没有授权*/
    XT_ERROR_ORDER_NOT_AUTHORIZE_CREDIT(300012),            
    /** 黄金业务没有授权*/
    XT_ERROR_ORDER_NOT_AUTHORIZE_GOLD(300013),      
    /** 沪港通业务没有授权*/
    XT_ERROR_ORDER_NOT_AUTHORIZE_HGT(300014),  
    /** 深港通业务没有授权*/
    XT_ERROR_ORDER_NOT_AUTHORIZE_SGT(300015),           
    /** 请求超时流量控制*/
    XT_ERROR_QUERYDATA_FLOW_CONTROL(300016),
    /** mac不匹配*/
    XT_ERROR_LOGIN_MAC_NOT_MATCH(300017),
    /** mac未授权*/
    XT_ERROR_LOGIN_MAC_NOT_AUTHORIZE(300018),
    /** 订阅行情报错*/
    XT_ERROR_SUBSCRIBE_QUOTE(300019),
    /** 创建指令时，合约不可交易*/
    XT_ERROR_CREATECOMMOND_TRANSUNABLE(300020);
    public final int value;
    
    EErrorType(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
