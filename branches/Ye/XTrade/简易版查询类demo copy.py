# coding:gbk
from XtTraderPyApi import *
import time
import math

"""
������ע�⣺���demoֻ�ṩ������������ṩ�������
        ���ǣ��������ݿ���ͨ��XtTraderApiCallback.m_api�����ȡ��������鿴XtTraderPyApi.py�ļ�

��demo����չʾpython traderapi�Ĺ������ƣ���demo�ṩ��ͨί�к͸����㷨ί���µ��Լ������ӿڣ��ֱ�չʾ��ͬ�����첽�ӿڵ�ʹ�÷�ʽ������ѡ��
ͬ���첽����
���壺ͬ�����첽��ע������Ϣͨ�Ż��� (synchronous communication/ asynchronous communication)��
ͬ�������ǵ���ĳ�������ǣ����÷��õȴ�������÷��ؽ�����ܼ�������ִ�С�
�첽����ͬ���෴  ���÷��������õ�����������ڵ��÷���������߿��ü���ִ�к�����������������ͨ��״����֪ͨ�����ߣ�����ͨ���ص������������������
������Բο� https://www.cnblogs.com/IT-CPC/p/10898871.html
"""


# CallBack��̳�XtTraderApiCallback�࣬���ڽ��������Լ����ƵĻص�
class CallBack(XtTraderApiCallback):
    def __init__(self, address, username, password, accountID):
        super(CallBack, self).__init__()
        self.m_strAddress = address
        self.m_strUserName = username
        self.m_strPassword = password
        self.m_strFutureAccountKey = ""
        self.m_strAccountID = accountID
        self.m_strAccountKey = ""
        self.m_nRequestId = 1
        self.m_api = XtTraderApi.createXtTraderApi(self.m_strAddress)  # �����û�
        self.m_nUserLogined = 0
        self.m_brequest = 1
        self.m_dictAccountKeyStatus = {}
        self.m_dictAccountID2Key = {}
        self.m_dictAccountKey2type = {}
        self.m_bConnected = 0

    def init(self):
        if self.m_strAddress == None:
            return -1, "server address is empty"
        if self.m_api == None:
            return -1, "failed to create traderapi client"
        if isinstance(self, XtTraderApiCallback):  # ��ǰ���Ƿ�Ϊ�����ʵ��
            self.m_api.setCallback(self)
            return self.m_api.init("./config/")
        return 0, ""

    def join(self):
        # self.m_api.joinAll()
        self.m_api.join()

    def joinAsync(self):
        self.m_api.join_async()

    # ���ӷ������Ļص�����������success��ʶ�����������Ƿ�ɹ�,����errorMsg��ʾ����������ʧ�ܵĴ�����Ϣ
    def onConnected(self, success, error_msg):
        print(
            "[onConnected] connect to server: {}, success:{}, error_msg:{}".format(
                self.m_strAddress, success, error_msg
            )
        )
        if success:
            self.m_bConnected = 1
        else:
            self.m_bConnected = 0

    def doLogin(self):
        # machineInfo����"IP��ַ|mac��ַ|�������к�|cpu��|������|������Ϣ|CPUIDָ���ecx����|������Ϣ"���������ֶ��޹أ��Ǿ�ֱ�Ӹ�����ֵ��������Ӧ�ֶξͺã������ֶμ��÷ָ���|������
        # machineInfo = "192.168.1.172|5C-F9-DD-73-7C-83|0682056C|BFEBFBFF000206A7|DESKTOP-84OBV5E|C,NTFS,223|6VKJD3X"
        machineInfo = ""
        appid = "xt_api_2.0"
        authcode = "7f3c92e678f9ec77"
        # �첽��¼
        # self.m_api.userLogin(self.m_strUserName, self.m_strPassword, self.m_nRequestId, machineInfo, appid, authcode)
        # ͬ����¼
        self.userLoginSync(
            self.m_strUserName, self.m_strPassword, machineInfo, appid, authcode
        )

    # ͬ����¼
    def userLoginSync(self, username, password, machineInfo, appid, authcode):
        print("userLoginSync started")
        error = self.m_api.userLoginSync(
            username, password, machineInfo, appid, authcode
        )
        if error.isSuccess():
            self.m_nUserLogined = 1
            print("userLoginSync resilt:", error.isSuccess())
            # self.request()
        else:
            print(error.errorMsg())

    # ͬ�������˺�key
    def reqAccountKeySync(self):
        print("reqAccountKeysSync started")
        error = XtError(0, "")
        print(self.m_api.reqAccountKeysSync(error))
        acckeyList = self.m_api.reqAccountKeysSync(error)
        if error.isSuccess():
            print("acckeyList size", len(acckeyList))
            for data in acckeyList:
                print("accountKey: ", data.m_strAccountKey)

    # ͬ����ѯ��Ʒ��Ϣ
    def reqProductDataSync(self):
        error = XtError(0, "")
        productList = self.m_api.reqProductDataSync(error)
        if error.isSuccess():
            print("productList size", len(productList))
            for data in productList:
                print(
                    "m_nProductId: ",
                    data.m_nProductId,
                    "m_strProductName",
                    data.m_strProductName,
                    "m_strProductCode",
                    data.m_strProductCode,
                    "m_dTotalNetValue",
                    data.m_dTotalNetValue,
                    "m_dGGTStockValue",
                    data.m_dGGTStockValue,
                )
        else:
            print("reqProductDataSync errmsg:", error.errorMsg())
            for data in productList:
                print(
                    "m_nProductId: ",
                    data.m_nProductId,
                    "m_strProductName",
                    data.m_strProductName,
                    "m_strProductCode",
                    data.m_strProductCode,
                    "m_dTotalNetValue",
                    data.m_dTotalNetValue,
                    "m_dGGTStockValue",
                    data.m_dGGTStockValue,
                )

    # ��ѯ��Ʒ��Ϣ
    def reqProductData(self):
        self.m_api.reqProductData(self.m_nRequestId)
        self.m_nRequestId += 1

    def onReqProductData(self, nRequestId, data, isLast, error):
        # if error.isSuccess():
        print(
            "m_nProductId: ",
            data.m_nProductId,
            "m_strProductName",
            data.m_strProductName,
        )
        # else:
        #    print("��ѯ��Ʒ��Ϣʧ�ܣ� errmsg: ", error.errorMsg())

    # �˺ŵ�¼֮�������
    def request(self):
        # demo���������˻����Բ�ѯ�������ʵ������޸Ĵ���
        if self.m_dictAccountID2Key:
            for name in self.m_dictAccountID2Key:
                self.m_strAccountID = name
                self.m_strAccountKey = self.m_dictAccountID2Key[name]
                print(
                    "m_dictAccountID2Key accountID:",
                    name,
                    "accountkey",
                    self.m_strAccountKey,
                )
                if name and self.checkAccountStatus(self.m_strAccountKey):
                    self.doRequest()

    # ��������˺��Ƿ��¼�ɹ�
    def checkAccountStatus(self, accountKey):
        if accountKey in self.m_dictAccountKeyStatus:
            print("userlogin status:", self.m_nUserLogined)
            status = self.m_dictAccountKeyStatus[accountKey]
            print("accountKey", accountKey, " status:", status)
            if self.m_nUserLogined:
                return 1
                # if status == EBrokerLoginStatus.BROKER_LOGIN_STATUS_OK or status == EBrokerLoginStatus.BROKER_LOGIN_STATUS_CLOSED:
                #     return 1
                # else:
                #     return 0
            else:
                return 0
        else:
            return 0

    # ������֮��Ĳ�������
    def doRequest(self):
        # ͬ���������demo
        print("start request")
        # ��ѯ�û���Ӧ��accountKey
        # self.reqAccountKeySync()
        # ��ѯ��Ʒ��Ϣ
        # self.reqProductDataSync()

        # ��ѯ�˺��ʽ���Ϣ
        # self.reqAccountDetailSync(self.m_strAccountID,self.m_strAccountKey)
        # ��ѯ�˺���ʷ�ʽ���Ϣ
        # self.reqHistoryAccountDetailSync(self.m_strAccountID,self.m_strAccountKey)

        # ��ѯ�˺�ί����ϸ��Ϣ
        # self.reqOrderDetailSync(self.m_strAccountID,self.m_strAccountKey)
        # ��ѯ�˺���ʷί����ϸ��Ϣ
        # self.reqHistoryOrderDetailSync(self.m_strAccountID,self.m_strAccountKey)

        # ��ѯ�˺ųɽ���ϸ��Ϣ
        # self.reqDealDetailSync(self.m_strAccountID,self.m_strAccountKey)
        # ��ѯ�˺ųɽ�ͳ����Ϣ
        # self.reqDealStaticsSync(self.m_strAccountID,self.m_strAccountKey)
        # ��ѯ�˺���ʷ�ɽ���ϸ��Ϣ
        # self.reqHistoryDealDetailSync(self.m_strAccountID,self.m_strAccountKey)

        # ��ѯ�˺ųֲ���ϸ��Ϣ
        # self.reqPositionDetailSync(self.m_strAccountID,self.m_strAccountKey)
        # ��ѯ�˺ųֲ�ͳ����Ϣ
        # self.reqPositionStaticsSync(self.m_strAccountID,self.m_strAccountKey)
        # ��ѯ�˺���ʷ�ֲ�ͳ����Ϣ
        # self.reqHistoryPositionStaticsSync(self.m_strAccountID,self.m_strAccountKey)
        # ��ѯ�ճ��ֲ�
        # self.reqInitialPositionStaticsSync(self.m_strAccountID,self.m_strAccountKey)
        # ͬ�����������Ӧ��Լ����
        # self.reqPriceDataSync("SH", "600000")
        # ��ѯ�û�����ָ����Ϣ
        # self.reqCommandsInfoSync()
        # ��ѯ�˺�ί����ϸ��Ϣ
        # self.reqOrderDetailSyncByOrderID(self.m_strAccountID,self.m_strAccountKey)
        # ��ѯ�˺ųɽ���ϸ��Ϣ
        # self.reqDealDetailSyncByOrderID(self.m_strAccountID,self.m_strAccountKey)
        # ��ѯ���µ���
        # self.reqCanOrderVolumeSync(self.m_strAccountID, self.m_strAccountKey)
        # ��ѯö������
        # self.reqEnumItemName()
        # ��ѯδ�˽Ḻծ��Լ
        # self.reqStkUnCloseCompactsSync(self.m_strAccountID, self.m_strAccountKey)
        # ��ѯδ�˽Ḻծ��Լ
        # self.reqStkClosedCompactsSync(self.m_strAccountID, self.m_strAccountKey)
        # ���������˺��ʲ�����
        # self.reqCreditDetailSync(self.m_strAccountID,self.m_strAccountKey)

        # �첽�������demo

        # �����˺��ʲ�����
        # self.reqAccountDetail(self.m_strAccountID,self.m_strAccountKey)
        # ���������˺��ʲ�����
        # self.reqCreditDetail(self.m_strAccountID,self.m_strAccountKey)
        # ����ί����ϸ
        # self.reqOrderDetail(self.m_strAccountID,self.m_strAccountKey)
        # ����ɽ���ϸ
        self.reqDealDetail(self.m_strAccountID, self.m_strAccountKey)
        # self.reqHistoryDealDetail(self.m_strAccountID,self.m_strAccountKey)
        # ����ֲ���ϸ
        # self.reqPositionDetail(self.m_strAccountID,self.m_strAccountKey)
        # ����ֲ�ͳ��
        # self.reqPositionStatics(self.m_strAccountID,self.m_strAccountKey)
        # �����˺���ʷ�ֲ�ͳ��
        # self.reqHistoryPositionStatics(self.m_strAccountID,self.m_strAccountKey)
        # ��ѯ��������
        # self.reqPriceData(self.m_strAccountID,self.m_strAccountKey)
        # ��ѯ��Ʒ��Ϣ
        # self.reqProductData()
        # ��ѯ�û�����ָ����Ϣ
        # self.reqCommandsInfo()

        # ��ѯ�ɶ�
        # self.reqSecuAccount(self.m_strAccountID, self.m_strAccountKey)

        # ��ѯ���µ���
        # self.reqCanOrderVolume(self.m_strAccountID, self.m_strAccountKey)
        # ��ѯδ�˽Ḻծ��Լ
        # self.reqStkUnCloseCompacts(self.m_strAccountID, self.m_strAccountKey)
        # ��ѯ�г�״̬
        # self.reqExchangeStatus(self.m_strAccountID, self.m_strAccountKey)

    # ��ѯ�ʽ���ˮ
    def reqFundFlowSync(self, accountID, accountKey):
        startdate = "20240101"
        enddate = "20240516"
        error = XtError(0, "")
        fundflowList = self.m_api.reqFundFlowSync(
            accountID, startdate, enddate, error, accountKey
        )
        if error.isSuccess():
            print("reqFundFlowSync success records:", len(fundflowList))

        else:
            print("reqFundFlowSync errmsg:", error.errorMsg())

    # ��ѯ�г�״̬
    def reqExchangeStatus(self, accountID, accountKey):
        print("reqExchangeStatus, accountID: ", accountID, "accountKey", accountKey)
        self.m_api.reqExchangeStatus(accountID, self.m_nRequestId, accountKey)

    def onReqExchangeStatus(self, accountID, nRequestId, accountKey, datas, error):
        if error.isSuccess:
            print("onReqExchangeStatus")
            if datas:
                print("onReqExchangeStatus,records: ", len(datas))
            for marketdata in datas:
                print("reqExchangeStatus,records: ", len(datas))
                print(
                    "����������",
                    marketdata.m_strExchangeId,
                    "�г�״̬",
                    marketdata.m_eInstrumentStatus,
                )
        else:
            print("onReqExchangeStatus errMsg: ", error.errorMsg())

    def refreshStkClosedCompacts(self, accountID, accountKey):
        self.m_api.refreshStkClosedCompacts(accountID, self.m_nRequestId, accountKey)
        self.m_nRequestId += 1
        print("refreshStkClosedCompacts")

    def refreshStkUnCloseCompacts(self, accountID, accountKey):
        self.m_api.refreshStkUnCloseCompacts(accountID, self.m_nRequestId, accountKey)
        self.m_nRequestId += 1
        print("refreshStkClosedCompacts")

    # ͬ����ѯδ�˽��Լ
    def reqStkUnCloseCompactsSync(self, accountID, accountKey):
        error = XtError(0, "")
        dataList = self.m_api.reqStkUnCloseCompactsSync(accountID, error, accountKey)
        if error.isSuccess():
            print("reqStkUnCloseCompactsSync records: ", len(dataList))
            for data in dataList:
                print(
                    "�˺�ID: {}, ��Լ����: {}, ��Լ���: {}, ��Լ���: {}, δ����Լ���: {}, δ����ԼϢ��: {}".format(
                        data.m_strAccountID,
                        data.m_strInstrumentID,
                        data.m_strCompactId,
                        data.m_dBusinessBalance,
                        data.m_dRealCompactBalance,
                        data.m_dRealCompactFare,
                    )
                )
        else:
            print("reqStkUnCloseCompactsSync failed, esrrmsg:", error.errorMsg())

    # ͬ����ѯ���˽��Լ
    def reqStkClosedCompactsSync(self, accountID, accountKey):
        error = XtError(0, "")
        dataList = self.m_api.reqStkClosedCompactsSync(accountID, error, accountKey)
        if error.isSuccess():
            print("reqStkClosedCompactsSync records: ", len(dataList))
            for data in dataList:
                print(
                    "�˺�ID: {}, ��Լ����: {}, ��Լ���: {}, ��Լ���: {}, �ѻ����: {}, �ѻ�Ϣ��: {}".format(
                        data.m_strAccountID,
                        data.m_strInstrumentID,
                        data.m_strCompactId,
                        data.m_dBusinessBalance,
                        data.m_dRepaidBalance,
                        data.m_dRepaidFare,
                    )
                )
        else:
            print("reqStkClosedCompactsSync failed, esrrmsg:", error.errorMsg())

    # ��ѯδ�˽��Լ
    def reqStkUnCloseCompacts(self, accountID, accountKey):
        self.m_api.reqStkUnCloseCompacts(accountID, self.m_nRequestId, accountKey)
        self.m_nRequestId += 1
        print("reqStkUnCloseCompacts")

    def onReqStkUnCloseCompact(
        self,
        accountID: str,
        nRequestId: int,
        data: CStkUnClosedCompacts,
        isLast: bool,
        error: XtError,
    ):
        if error.isSuccess():
            print("onReqStkUnCloseCompact success")
            if data:
                print(
                    "�˺�ID: {}, ��Լ����: {}, ��Լ���: {}, ��Լ���: {}, δ����Լ���: {}, δ����ԼϢ��: {}".format(
                        data.m_strAccountID,
                        data.m_strInstrumentID,
                        data.m_strCompactId,
                        data.m_dBusinessBalance,
                        data.m_dRealCompactBalance,
                        data.m_dRealCompactFare,
                    )
                )
        else:
            print("onReqStkUnCloseCompact failed, errmsg:", error.errorMsg())

    def onReqStkUnCloseCompactWithAccKey(
        self,
        accountID: str,
        nRequestId: int,
        accountKey: str,
        data: CStkUnClosedCompacts,
        isLast: bool,
        error: XtError,
    ):
        pass

    def onBatchReqStkUnCloseCompact(
        self,
        accountID: str,
        nRequestId: int,
        data: list[CStkUnClosedCompacts],
        isLast: bool,
        error: XtError,
    ):
        if error.isSuccess():
            print("onBatchReqStkUnCloseCompact success")
            if data:
                print("CStkUnClosedCompacts records:", len(data))
                for unCloseCompace in data:
                    print(
                        "�˺�ID: {}, ��Լ����: {}, ��Լ���: {}, ��Լ���: {}, δ����Լ���: {}, δ����ԼϢ��: {}".format(
                            unCloseCompace.m_strAccountID,
                            unCloseCompace.m_strInstrumentID,
                            unCloseCompace.m_strCompactId,
                            unCloseCompace.m_dBusinessBalance,
                            unCloseCompace.m_dRealCompactBalance,
                            unCloseCompace.m_dRealCompactFare,
                        )
                    )
        else:
            print("onBatchReqStkUnCloseCompact failed, errmsg:", error.errorMsg())

    # ��ѯö������
    def reqEnumItemName(self):
        name = self.m_api.reqEnumItemName(
            "EBrokerPriceType",
            EBrokerPriceType.BROKER_PRICE_PROP_OPTION_RELEASE_COMB_STRATEGY_KKS,
        )
        print(name)
        name = self.m_api.reqEnumItemName(
            "EOperationType",
            EOperationType.OPT_CLOSE_LONG_TODAY_HISTORY_THEN_OPEN_SHORT,
        )
        print(name)
        name = self.m_api.reqEnumItemName(
            "ETimeCondition", ETimeCondition.TIME_CONDITION_GTD
        )
        print(name)

    # ��ѯ���µ�����
    def reqCanOrderVolumeSync(self, account_id, account_key):
        error = XtError(0, "")
        reqParam = COpVolumeReq()
        reqParam.m_strAccountID = account_id
        reqParam.m_strMarket = "SH"
        reqParam.m_strInstrument = "601919"
        reqParam.m_dPrice = 9.88
        # reqParam.m_eOperationType = EOperationType.OPT_BUY
        reqParam.m_eOperationType = EOperationType.OPT_SELL
        reqParam.m_eHedgeFlag = EHedgeFlagType.HEDGE_FLAG_SPECULATION
        volume = self.m_api.reqCanOrderVolumeSync(reqParam, error, account_key)
        print(
            "reqCanOrderVolumeSync market {}, code {}, volume {}".format(
                reqParam.m_strMarket, reqParam.m_strInstrument, volume
            )
        )

    def reqCanOrderVolume(self, account_id, account_key):
        reqParam = COpVolumeReq()
        reqParam.m_strAccountID = account_id
        reqParam.m_strMarket = "SH"
        reqParam.m_strInstrument = "601919"
        reqParam.m_dPrice = 9.88
        # reqParam.m_eOperationType = EOperationType.OPT_BUY
        reqParam.m_eOperationType = EOperationType.OPT_SELL
        reqParam.m_eHedgeFlag = EHedgeFlagType.HEDGE_FLAG_SPECULATION
        print(
            "reqCanOrderVolume makret {} code {}".format(
                reqParam.m_strMarket, reqParam.m_strInstrument
            )
        )
        self.m_api.reqCanOrderVolume(reqParam, self.m_nRequestId, account_key)
        self.m_nRequestId += 1

    def onReqCanOrderVolume(
        self, accountID, nRequestId, accountKey, market, instrument, nVolume, error
    ):
        if error.isSuccess():
            print(
                "��ѯ�г�{} ���� {}���µ���Ϊ��{}".format(market, instrument, nVolume)
            )
        else:
            print("onReqCanOrderVolume failed, errmsg:", error.errorMsg())

    # ͬ����ѯ�ʽ�����
    def reqAccountDetailSync(self, account_id, account_key):
        print("reqAccountDetailSync account_id:", account_id)
        errno = XtError(0, "")
        data = self.m_api.reqAccountDetailSync(account_id, errno, account_key)
        if errno.isSuccess():
            print("reqAccountDetailSync success")
            print(data.m_strAccountID)
            print(data.m_strStatus)
            print("���ʲ�", data.m_dBalance)
            print("�����ʽ�", data.m_dAvailable)
            print("��Ʊ����ֵ:", data.m_dStockValue)
            print("ծȯ����ֵ", data.m_dLoanValue)
            print("��������ֵ", data.m_dFundValue)
            print("m_dFrozenMargin", data.m_dFrozenMargin)
            print("m_dFrozenCash", data.m_dFrozenCash)
            print("m_dFrozenCommission", data.m_dFrozenCommission)
            print("m_dRisk", data.m_dRisk)
            print("m_dNav", data.m_dNav)
            print("�ֲ�ӯ��", data.m_dPositionProfit)
            print("ƽ��ӯ��", data.m_dCloseProfit)
            print("����ӯ��", data.m_dDaysProfit)
            print("m_eDualStatus", data.m_eDualStatus)
            print("�˺�����", data.m_strAccountName)
            print("���͹�˾���", data.m_strBrokerID)
            print("���͹�˾����", data.m_strBrokerName)
        else:
            print(
                "reqAccountDetailSync failed, errmsg:",
                errno.errorMsg(),
                "account_id: ",
                account_id,
            )

    # ��ѯ�˺���ʷ�ʽ���Ϣ
    def reqHistoryAccountDetailSync(self, account_id, account_key):
        print("reqHistoryAccountDetailSync started")
        errno = XtError(0, "")
        deallist = self.m_api.reqHistoryAccountDetailSync(
            account_id, "20230911", "20230911", errno, account_key
        )
        if errno.isSuccess:
            print("reqHistoryAccountDetailSync success, record:", len(deallist))
            for data in deallist:
                print(
                    "m_strAccountID",
                    data.m_strAccountID,
                    "m_strTradingDate",
                    data.m_strTradingDate,
                    "m_dAvailable",
                    data.m_dAvailable,
                )

    # ͬ����ѯί������
    def reqOrderDetailSync(self, account_id, account_key):
        print("reqOrderDetailSync started")
        errno = XtError(0, "")
        orderlist = self.m_api.reqOrderDetailSync(account_id, errno, account_key)
        if errno.isSuccess:
            print("reqOrderDetailSync success, record:", len(orderlist))
            # for data in orderlist:
            #     print("m_strOrderSysID:", data.m_strOrderSysID,
            #           "m_strSecuAccount:", data.m_strSecuAccount,
            #           "m_strInsertDate", data.m_strInsertDate,
            #           "m_dAveragePrice", data.m_dAveragePrice,
            #           "m_dTradeAmount", data.m_dTradeAmount,
            #           "m_strInsertTime", data.m_strInsertTime)

    # ͬ����ѯָ���Ӧί������
    def reqOrderDetailSyncByOrderID(self, account_id, account_key):
        print("reqOrderDetailSyncByOrderID started")
        errno = XtError(0, "")
        orderId = 703377
        orderlist = self.m_api.reqOrderDetailSyncByOrderID(
            account_id, errno, orderId, account_key
        )
        if errno.isSuccess:
            print("reqOrderDetailSyncByOrderID success, record:", len(orderlist))
            for data in orderlist:
                print(
                    "m_strOrderSysID:",
                    data.m_strOrderSysID,
                    "m_strSecuAccount:",
                    data.m_strSecuAccount,
                    "m_strInsertDate",
                    data.m_strInsertDate,
                    "m_dAveragePrice",
                    data.m_dAveragePrice,
                    "m_dTradeAmount",
                    data.m_dTradeAmount,
                    "m_nOrderID",
                    data.m_nOrderID,
                    "m_nOrderPriceType",
                    data.m_nOrderPriceType,
                    "m_nDirection",
                    data.m_nDirection,
                    "m_eOffsetFlag",
                    data.m_eOffsetFlag,
                    "m_strInsertTime",
                    data.m_strInsertTime,
                )

    # ͬ����ѯ��ʷί������
    def reqHistoryOrderDetailSync(self, account_id, account_key):
        print("reqHistoryOrderDetailSync started")
        errno = XtError(0, "")
        orderlist = self.m_api.reqHistoryOrderDetailSync(
            account_id, "20240614", "20240614", errno, account_key
        )
        if errno.isSuccess:
            print("reqHistoryOrderDetailSync success, record:", len(orderlist))
            for data in orderlist:
                # print('m_strInstrumentID: ', data.m_strInstrumentID,  'm_strOrderSysID:', data.m_strOrderSysID)
                pass

    # ͬ����ѯ��ʷί������
    def reqHistoryOrderDetail(self, account_id, account_key):
        print("reqHistoryOrderDetail started")
        self.m_nRequestId += 1
        self.m_api.reqHistoryOrderDetail(
            account_id, "20240614", "20240614", self.m_nRequestId, account_key
        )

    def onReqHistoryOrderDetail(self, accountID, nRequestId, data, isLast, error):
        print(data.m_strOrderSysID, "isLast:", isLast)

    # ͬ����ѯ�ɽ�����
    def reqDealDetailSync(self, account_id, account_key):
        print("reqDealDetailSync started, account_id:", account_id)
        errno = XtError(0, "")
        deallist = self.m_api.reqDealDetailSync(account_id, errno, account_key)
        if errno.isSuccess:
            print("reqDealDetailSync success, record:", len(deallist))
            # for data in deallist:
            #     print("reqDealDetailSync", data.m_nOrderID, "code:",
            #  data.m_strInstrumentID,"m_nOrderID", data.m_nOrderID, "m_strOrderSysID:",
            #  data.m_strOrderSysID, "volume:", data.m_nVolume, "m_nHedgeFlag",
            #  data.m_nHedgeFlag, "m_strTradeID", data.m_strTradeID)

    def reqDealStaticsSync(self, account_id, account_key):
        print(
            "reqDealStaticsSync started, account_id:",
            account_id,
            "account_key:",
            account_key,
        )
        errno = XtError(0, "")
        dealStaticsList = self.m_api.reqDealStaticsSync(account_id, errno, account_key)
        if errno.isSuccess:
            print("reqDealStaticsSync success, record:", len(dealStaticsList))
            for data in dealStaticsList:
                print(
                    "m_strInstrumentID:",
                    data.m_strInstrumentID,
                    "m_nVolume:",
                    data.m_nVolume,
                )

    # ͬ����ѯָ���Ӧ�ɽ�����
    def reqDealDetailSyncByOrderID(self, account_id, account_key):
        print("reqDealDetailSyncByOrderID started")
        errno = XtError(0, "")
        orderID = 703377
        deallist = self.m_api.reqDealDetailSyncByOrderID(
            account_id, errno, orderID, account_key
        )
        if errno.isSuccess:
            print("reqDealDetailSyncByOrderID success, record:", len(deallist))
            for data in deallist:
                print(
                    "reqDealDetailSync",
                    "code:",
                    data.m_strInstrumentID,
                    "m_nOrderID",
                    data.m_nOrderID,
                    "m_strOrderSysID:",
                    data.m_strOrderSysID,
                    "volume:",
                    data.m_nVolume,
                    "m_nHedgeFlag",
                    data.m_nHedgeFlag,
                    "m_nDirection",
                    data.m_nDirection,
                    "m_nOffsetFlag",
                    data.m_nOffsetFlag,
                    "m_strTradeID",
                    data.m_strTradeID,
                )

    # ͬ����ѯ��ʷ�ɽ�����
    def reqHistoryDealDetailSync(self, account_id, account_key):
        print("reqHistoryDealDetailSync started")
        errno = XtError(0, "")
        deallist = self.m_api.reqHistoryDealDetailSync(
            account_id, "20240614", "20240614", errno, account_key
        )
        if errno.isSuccess:
            print("reqHistoryDealDetailSync success, record:", len(deallist))
            for data in deallist:
                print(
                    "m_strInstrumentID",
                    data.m_strInstrumentID,
                    "m_strOrderSysID",
                    data.m_strOrderSysID,
                )
                # print('m_strInstrumentID', data.m_strInstrumentID, 'm_strOrderSysID',
                #  data.m_strOrderSysID, 'm_strTradeDate', data.m_strTradeDate, "m_nHedgeFlag", data.m_nHedgeFlag)

    # ͬ����ѯ�ֲ�����
    def reqPositionDetailSync(self, account_id, account_key):
        print("reqPositionDetailSync started")
        error = XtError(0, "")
        positionlist = self.m_api.reqPositionDetailSync(account_id, error, account_key)
        if error.isSuccess():
            print("reqPositionDetailSync success, record:", len(positionlist))
            for data in positionlist:
                print(data.m_strInstrumentID)
                print(data.m_dOpenPrice)
        else:
            print("reqPositionDetailSync failed, errmsg", error.errorMsg())

    # ͬ����ѯ�ֲ�ͳ��
    def reqPositionStaticsSync(self, account_id, account_key):
        print("reqPositionStaticsSync started, account_id", account_id)
        errno = XtError(0, "")
        positionlist = self.m_api.reqPositionStaticsSync(account_id, errno, account_key)
        if errno.isSuccess:
            print("reqPositionStaticsSync success, record:", len(positionlist))
            for data in positionlist:
                # print("data ���� == {}��".format(dir(data)))
                # if data.m_strInstrumentID == "601318":
                print(
                    "accountId",
                    data.m_strAccountID,
                    "m_strInstrumentID",
                    data.m_strInstrumentID,
                    "m_strInstrumentName",
                    data.m_strInstrumentName
                    ,"m_nOpenVolume", data.m_nOpenVolume
                    , "m_nPosition", data.m_nPosition
                    , "m_nOnRoadVolume", data.m_nOnRoadVolume
                    , "m_nYesterdayVolume", data.m_nYesterdayVolume
                    , "m_dPositionProfit", data.m_dPositionProfit
                    , "m_dFloatProfit", data.m_dFloatProfit
                    , "m_nCoveredAmount", data.m_nCoveredAmount
                    , "m_dUsedMargin", data.m_dUsedMargin
                    , "m_nDirection", data.m_nDirection
                    , "m_bIsToday", data.m_bIsToday
                    , "m_strSecuAccount", data.m_strSecuAccount
                    , "m_nCanCloseVol", data.m_nCanCloseVolume
                    , "m_nCanUseVolume", data.m_nCanUseVolume
                )

    # ͬ����ѯ��ʷ�ֲ�ͳ��
    def reqHistoryPositionStaticsSync(self, account_id, account_key):
        print("reqHistoryDealDetailSync started")
        errno = XtError(0, "")
        deallist = self.m_api.reqHistoryPositionStaticsSync(
            account_id, "20230913", "20230913", errno, account_key
        )
        if errno.isSuccess:
            print("reqHistoryPositionStaticsSync success, record:", len(deallist))
            for data in deallist:
                print(
                    "m_strInstrumentID",
                    data.m_strInstrumentID,
                    "m_dInstrumentValue",
                    data.m_dInstrumentValue,
                    "m_strAccountKey",
                    data.m_strAccountKey,
                )

    # ͬ����ѯ�ճ��ֲ�ͳ��
    def reqInitialPositionStaticsSync(self, account_id, account_key):
        print("reqInitialPositionStaticsSync started account_id�� ", account_id)
        errno = XtError(0, "")
        positionlist = self.m_api.reqInitialPositionStaticsSync(
            account_id, errno, account_key
        )
        if errno.isSuccess:
            print("reqInitialPositionStaticsSync success, record:", len(positionlist))
            for data in positionlist:
                print(data.m_strInstrumentID)

    # ͬ����ѯ��������
    def reqPriceDataSync(self, market, code):
        errno = XtError(0, "")
        pricelist = self.m_api.reqPriceDataSync(market, code, errno)
        if errno.isSuccess():
            for data in pricelist:
                print("��Լ����", data.m_strInstrumentID)
                print("���¼�", data.m_dLastPrice)
                print("m_dUpDown", data.m_dUpDown)
                print("m_dUpDownRate", data.m_dUpDownRate)

    # �û���¼�Ļص�����
    def onUserLogin(self, username, password, nRequestId, error):
        if error.isSuccess():
            print("[onUserlogin] username:{},��¼�ɹ�".format(username))
            self.m_nUserLogined = 1
            # self.request()
        else:
            print(
                "[onUserlogin] username:{},��¼ʧ�ܣ�ʧ��ԭ��{}".format(
                    username, error.errorMsg()
                )
            )

    # �û��ǳ��Ļص����� ,username�û�����password���룬error��
    def onUserLogout(self, username, password, nRequestId, error):
        print("[onUserLogout] success: ", error.isSuccess(), ", username: ", username)

    def onRtnLoginStatus(self, account_id, status, account_type, error_msg):
        # print("onRtnLoginStatus")
        pass

    # �˺�key���ƽӿڣ��˺ŵ�¼�ɹ���ſ���ִ���µ��Ȳ��������Ը��������status�ֶ����ж�
    # ����: status �����ʽ��˺ŵĵ�¼״̬
    # ����: account_type �����ʽ��˺ŵ����� 1:�ڻ��˺�, 2:��Ʊ�˺�, 3:�����˺�
    def onRtnLoginStatusWithActKey(
        self, account_id, status, account_type, account_key, error_msg
    ):
        # if account_id == self.m_strAccountID:
        self.m_dictAccountKeyStatus[account_key] = status
        self.m_dictAccountID2Key[account_id] = account_key
        self.m_dictAccountKey2type[account_key] = account_type
        print(
            "[onRtnLoginStatusWithActKey] account_id��{}, account_id��{}, account_type: {}, status:{}, error_msg:{}".format(
                account_id, account_key, account_type, status, error_msg
            )
        )
        # if status == EBrokerLoginStatus.BROKER_LOGIN_STATUS_OK or status == EBrokerLoginStatus.BROKER_LOGIN_STATUS_CLOSED:
        #     self.request()
        # else:
        #     pass

    # �����˺��ʲ�����
    def reqAccountDetail(self, account_id, account_key):
        print("[reqAccountDetail]��ѯ�˺�:", account_id, "���ʲ�����")
        self.m_nRequestId += 1
        self.m_api.reqAccountDetail(account_id, self.m_nRequestId, account_key)

    # �����ʽ����ݵĻص�������data��ӦCAccountDetail�ṹ, error��ӦXtError�ṹ
    def onReqAccountDetail(self, account_id, request_id, data, is_last, error):
        if error.isSuccess():
            print(
                "[onReqAccountDetail] success, account_id:",
                account_id,
                ", m_dAvailable:",
                data.m_dAvailable,
                ", m_dPositionProfit:",
                data.m_dPositionProfit,
                ", m_dDaysProfit:",
                data.m_dDaysProfit,
                ", m_dStockValue:",
                data.m_dStockValue,
            )
        else:
            print(
                "[onReqAccountDetail] failed, account_id:",
                account_id,
                ", error_msg:",
                error.errorMsg(),
            )

    def onRtnAccountDetail(self, account_id, data):
        # print(u'[onRtnAccountDetail] success, account_id:', account_id)
        pass

    # ���������˺��ۺ��ʽ���Ϣ
    def reqCreditDetailSync(self, accountID):
        error = XtError(0, "")
        creditData = self.m_api.reqCreditDetailSync(accountID, error)
        if error.isSuccess():
            pass
        else:
            print("reqCreditDetailSync failed, errmsg: ", error.errorMsg())

    # ���������˺��ʲ�����
    def reqCreditDetail(self, account_id, account_key):
        print("[reqCreditAccountDetail]��ѯ�����˺�:", account_id, "���ʲ�����")
        self.m_nRequestId += 1
        self.m_api.reqCreditDetail(account_id, self.m_nRequestId, account_key)

    # ���������ʲ����ݵĻص�������data��ӦCCreditDetail�ṹ, error��ӦXtError�ṹ
    def onReqCreditDetail(self, account_id, request_id, data, is_last, error):
        if error.isSuccess():
            print(
                "[onReqCreditAccountDetail] success, account_id:",
                account_id,
                "is_last:",
                is_last,
            )
        else:
            print(
                "[onReqCreditAccountDetail] failed, account_id:",
                account_id,
                ", error_msg:",
                error.errorMsg(),
            )

    # ����ί����ϸ
    def reqOrderDetail(self, account_id, account_key):
        print("[reqOrderDetail]��ѯ�˺�:", account_id, "�ĵ���ί����ϸ")
        self.m_nRequestId += 1
        self.m_api.reqOrderDetail(account_id, self.m_nRequestId, account_key)

    # ί����ϸ��ѯ�Ļص�������data��ӦCOrderDetail�ṹ, error��ӦXtError�ṹ
    def onReqOrderDetail(self, account_id, request_id, data, is_last, error):
        if error.isSuccess():
            print(
                "[onReqOrderDetail] success, account_id: {}, InstrumentID: {}".format(
                    account_id, data.m_strInstrumentID
                )
            )
        else:
            print(
                "[onReqOrderDetail] failed, account_id:",
                account_id,
                ", error_msg:",
                error.errorMsg(),
            )

    # ����ɽ���ϸ
    def reqDealDetail(self, account_id, account_key):
        print("[reqDealDetail]��ѯ�˺�:", account_id, "�ĵ��ճɽ���ϸ")
        self.m_nRequestId += 1
        self.m_api.reqDealDetail(account_id, self.m_nRequestId, account_key)

    # �ɽ���ϸ��ѯ�Ļص�������data��ӦCDetalDetail�ṹ, error��ӦXtError�ṹ
    def onReqDealDetail(self, account_id, request_id, data, is_last, error):
        if error.isSuccess():
            print(
                "[onReqDealDetail] success, account_id:",
                account_id,
                ", is_last:",
                is_last,
            )
        else:
            print(
                "[onReqDealDetail] failed, account_id:",
                account_id,
                ", error_msg:",
                error.errorMsg(),
            )

    # ������ʷ�ɽ���ϸ
    def reqHistoryDealDetail(self, account_id, account_key):
        print(
            "[reqHistoryDealDetail]��ѯ�˺�:",
            account_id,
            "�ĵ��ճɽ���ϸ",
            "account_key",
            account_key,
        )
        self.m_nRequestId += 1
        self.m_api.reqHistoryDealDetail(
            account_id, "20231103", "20231103", self.m_nRequestId, account_key
        )

    # ��ʷ�ɽ���ϸ��ѯ�Ļص�������data��ӦCDetalDetail�ṹ, error��ӦXtError�ṹ
    def onReqHistoryDealDetail(self, account_id, request_id, data, is_last, error):
        if error.isSuccess():
            print(
                "[onReqHistoryDealDetail] success, account_id:",
                account_id,
                ", is_last:",
                is_last,
            )
        else:
            print(
                "[onReqHistoryDealDetail] failed, account_id:",
                account_id,
                ", error_msg:",
                error.errorMsg(),
            )

    # ����ֲ���ϸ
    def reqPositionDetail(self, account_id, account_key):
        print("[reqPositionDetail]��ѯ�˺�:", account_id, "�ĳֲ���ϸ")
        self.m_nRequestId += 1
        self.m_api.reqPositionDetail(account_id, self.m_nRequestId, account_key)

    # ����ֲ���ϸ�Ļص�������data��ӦCPositionDetail�ṹ, error��ӦXtError�ṹ
    def onReqPositionDetail(self, account_id, request_id, data, is_last, error):
        if error.isSuccess():
            print(
                "[onReqPositionDetail] success, account_id:",
                account_id,
                ", is_last: ",
                is_last,
            )
        else:
            print(
                "[onReqPositionDetail] failed, account_id:",
                account_id,
                ", error_msg:",
                error.errorMsg(),
            )

    # ����ֲ�ͳ��
    def reqPositionStatics(self, account_id, account_key):
        print("[reqPositionStatics]��ѯ�˺�:", account_id, "�ĳֲ���ϸ")
        self.m_nRequestId += 1
        self.m_api.reqPositionStatics(account_id, self.m_nRequestId, account_key)

    # ����ֲ�ͳ�ƵĻص�������data��ӦCPositionStatics�ṹ, error��ӦXtError�ṹ
    def onReqPositionStatics(self, account_id, request_id, data, is_last, error):
        if error.isSuccess():
            print(
                "[onReqPositionStatics] success, account_id:",
                account_id,
                ", is_last:",
                is_last,
            )
        else:
            print(
                "[onReqPositionStatics] failed, account_id:",
                account_id,
                ", error_msg:",
                error.errorMsg(),
            )

    # �����˺���ʷ�ֲ�ͳ��
    def reqHistoryPositionStatics(self, account_id, account_key):
        print(
            "[reqHistoryPositionStatics]��ѯ�˺�:",
            account_id,
            "����ʷ�ֲ�ͳ��",
            "account_key: ",
            account_key,
        )
        self.m_nRequestId += 1
        self.m_api.reqHistoryPositionStatics(
            account_id, "20230902", "20230902", self.m_nRequestId, account_key
        )

    # �˺���ʷ�ֲ�ͳ�ƵĻص�������data��ӦCPositionStatics�ṹ, error��ӦXtError�ṹ
    def onReqHistoryPositionStatics(self, account_id, request_id, data, is_last, error):
        if error.isSuccess():
            print(
                "[onReqHistoryPositionStatics] success, account_id:",
                account_id,
                ", is_last:",
                is_last,
                "m_strInstrumentID",
                data.m_strInstrumentID,
            )
        else:
            print(
                "[onReqHistoryPositionStatics] failed, account_id:",
                account_id,
                ", error_msg:",
                error.errorMsg(),
            )

    # ����ծ��Լ�Ļص�����, error��ӦXtError�ṹ
    def onReqStksubjects(self, account_id, request_id, data, is_last, error):
        if error.isSuccess():
            print(
                "[onReqStksubjects] success, account_id:",
                account_id,
                ", is_last:",
                is_last,
            )
        else:
            print(
                "[onReqStksubjects] failed, account_id:",
                account_id,
                ", error_msg:",
                error.errorMsg(),
            )

    # ����������ȯ��Ľӿں�Ļص�����, error��ӦXtError�ṹ
    def onReqStkcompacts(self, account_id, request_id, data, is_last, error):
        if error.isSuccess():
            print(
                "[onReqStkcompacts] success, account_id:",
                account_id,
                ", is_last:",
                is_last,
            )
        else:
            print(
                "[onReqStkcompacts] failed, account_id:",
                account_id,
                ", error_msg:",
                error.errorMsg(),
            )

    # ��ѯ��������
    def reqPriceData(self, market, code):
        self.m_api.reqPriceData(market, code, self.m_nRequestId)
        self.m_nRequestId += 1
        print("[reqPriceData]��ѯ��Լ:", code, "���������")

    # �����������ݵĻص���data��ӦCPriceData�ṹ, error��ӦXtError�ṹ
    def onReqPriceData(self, request_id, data, error):
        if error.isSuccess():
            print("[onReqPriceData] success")
            print("��Լ����", data.m_strInstrumentID)
            print("���¼�", data.m_dLastPrice)

        else:
            print("[onReqPriceData] failed, error_msg:", error.errorMsg())

    def reqCommandsInfo(self):
        self.m_api.reqCommandsInfo(self.m_nRequestId)
        self.m_nRequestId += 1
        print("[reqCommandsInfo] ��ѯָ��:")

    def onReqCommandsInfo(self, nRequestId, data, isLast, error):
        if error.isSuccess():
            print("ָ������ ={}".format(dir(data)))
            # print("orderid: ", data.m_nOrderID)
        else:
            print("errmsg: ", error.errorMsg())

    def reqCommandsInfoSync(self):
        print("[reqCommandsInfoSync] ��ѯָ��:")
        errno = XtError(0, "")
        cmdList = self.m_api.reqCommandsInfoSync(errno)
        if errno.isSuccess():
            for data in cmdList:
                # if(data.m_nOrderID == 811340 ):
                print("��ѯָ��ɹ�,total:  ", len(cmdList))
                print("orderid: ", data.m_nOrderID)
                print("�ɽ���: ", data.m_dTradedVolume)
                print("�ɽ�����: ", data.m_dTradedPrice)
                print("�ɽ����: ", data.m_dTradedAmount)
                print("m_dPrice: ", data.m_dPrice)
                print("m_eOperationType: ", data.m_eOperationType)
                print("m_eStatus: ", data.m_eStatus)
                print("m_nCmdSource: ", data.m_nCmdSource)
        else:
            print("��ѯָ��ʧ�ܣ���", errno.errorMsg())

    # ����ɶ���
    def reqSecuAccount(self, account_id, account_key):
        print("[reqSecuAccount]��ѯ�˺�:", account_id, "�Ĺɶ�����")
        self.m_nRequestId += 1
        self.m_api.reqSecuAccount(account_id, self.m_nRequestId, account_key)

    # �����ʽ����ݵĻص�������data��ӦCAccountDetail�ṹ, error��ӦXtError�ṹ
    def onReqSecuAccount(
        self, account_id, request_id, accountkey, data, is_last, error
    ):
        if error.isSuccess():
            print(
                "[onReqSecuAccount] success, m_strSecuAccount:",
                data.m_strSecuAccount,
                "m_strExchangeID:",
                data.m_strExchangeID,
                "m_eMainFlag",
                data.m_eMainFlag,
                ", is_last:",
                is_last,
            )
        else:
            print(
                "[onReqSecuAccount] failed, account_id:",
                account_id,
                ", error_msg:",
                error.errorMsg(),
            )

    def onRtnMarketAndTradeDay(self, market, tradeDay):
        print("onRtnMarketAndTradeDay market {}, tradeDay {}".format(market, tradeDay))

    def onNamedTimer(self, timerName):
        self.m_nRequestId += 1
        self.m_api.reqAccountDetail(
            "2000154", self.m_nRequestId, "2____11194____11194____49____2000154____"
        )

    def reqOrderDetailBySysIDSync(self, account_id, account_key):
        error = XtError(0, "")
        data = self.m_api.reqOrderDetailBySysIDSync(
            account_id, error, "2024061200002688", "SH", account_key
        )
        if error.isSuccess():
            print(
                "reqOrderDetailBySysIDSync m_strAccountID: {}, m_strInstrumentID: {}".format(
                    data.m_strAccountID, data.m_strInstrumentID
                )
            )

    def reqOrderDetailBySysID(self, account_id, account_key):
        self.m_nRequestId += 1
        data = self.m_api.reqOrderDetailBySysID(
            account_id, self.m_nRequestId, "2024061200002688", "SH", account_key
        )
        print("reqOrderDetailBySysID started")

    def onReqOrderDetailBySysID(
        self, accountID, requestID, accountKey, orderSyeID, exchangeID, data, error
    ):
        if error.isSuccess():
            print("reqOrderDetailBySysID m_strAccountID:", data.m_strAccountID)


if __name__ == "__main__":
    server_addr = "192.168.10.100:65300"  # ͳһ���׷������ĵ�ַ
    username = "�Ʊ�"  # ͬ�ͻ��˵�¼�û�
    password = "yml666888"  # �û����룬�ͻ��˵�¼���룬���ʽ�����
    accountID = "8000138"  # �����˺ţ�ȯ�̹�̨���ʽ��˺�
    accountKey = ""  # �˺Ŷ�Ӧ���˺�key

    cb = CallBack(
        server_addr, username, password, accountID
    )  # ����һ��CallBack���󣬺����������ڸö���
    cb.init()
    cb.joinAsync()
    while not cb.m_bConnected:
        time.sleep(0.1)
    print("���ӳɹ�")
    cb.doLogin()
    while accountID not in cb.m_dictAccountID2Key:
        time.sleep(0.1)
    print("�˺ŵ�¼�ɹ����˺�key��", accountKey)
    for accountID, accountKey in cb.m_dictAccountID2Key.items():
        cb.reqAccountDetailSync(accountID, accountKey)
        cb.reqPositionStaticsSync(accountID, accountKey)
    #
    # cb.reqOrderDetailBySysIDSync(accountID, accountKey)
    # cb.reqOrderDetailBySysID(accountID, accountKey)
    # ��ʱ������
    # cb.m_api.startNamedTimer("test", 10, -1,False)
    # ��ѯ�û���Ӧ��accountKey
    # cb.reqAccountKeySync()
    # ��ѯ��Ʒ��Ϣ
    # cb.reqProductDataSync()

    # # ��ѯ�˺��ʽ���ˮ
    # cb.reqFundFlowSync(accountID, accountKey)
    # ��ѯ�˺��ʽ���Ϣ (����)
    # cb.reqAccountDetailSync(accountID, accountKey)
    # # ��ѯ�˺���ʷ�ʽ���Ϣ��success, record: 0��
    # cb.reqHistoryAccountDetailSync(accountID,accountKey)

    # # ��ѯ�˺�ί����ϸ��Ϣ��success, record: 22��
    # cb.reqOrderDetailSync(accountID,accountKey)
    # ��ѯ�˺���ʷί����ϸ��Ϣ
    # cb.reqHistoryOrderDetailSync(accountID,accountKey)
    # cb.reqHistoryOrderDetail(accountID,accountKey)

    # # ��ѯ�˺ųɽ���ϸ��Ϣ��success, record: 21��
    # cb.reqDealDetailSync(accountID,accountKey)
    # # ��ѯ�˺ųɽ�ͳ����Ϣ�����ã�
    # cb.reqDealStaticsSync(accountID,accountKey)
    # # ��ѯ�˺���ʷ�ɽ���ϸ��Ϣ��success, record: 0��
    # cb.reqHistoryDealDetailSync(accountID,accountKey)

    # # ��ѯ�˺ųֲ���ϸ��Ϣ
    # cb.reqPositionDetailSync(accountID,accountKey)
    # # ��ѯ�˺ųֲ�ͳ����Ϣ
    # cb.reqPositionStaticsSync(accountID,accountKey)
    # # ��ѯ�˺���ʷ�ֲ�ͳ����Ϣ
    # cb.reqHistoryPositionStaticsSync(accountID,accountKey)
    # # ��ѯ�ճ��ֲ�
    # cb.reqInitialPositionStaticsSync(accountID,accountKey)
    # ͬ�����������Ӧ��Լ����
    # cb.reqPriceDataSync("SH", "600000")
    # ��ѯ�û�����ָ����Ϣ
    # cb.reqCommandsInfoSync()
    # ��ѯ�˺�ί����ϸ��Ϣ
    # cb.reqOrderDetailSyncByOrderID(accountID,accountKey)
    # ��ѯ�˺ųɽ���ϸ��Ϣ
    # cb.reqDealDetailSyncByOrderID(accountID,accountKey)
    # ��ѯ���µ���
    # cb.reqCanOrderVolumeSync(accountID, accountKey)
    # ��ѯö������
    # cb.reqEnumItemName()
    # ��ѯδ�˽Ḻծ��Լ
    # cb.reqStkUnCloseCompactsSync(accountID, accountKey)
    # ��ѯδ�˽Ḻծ��Լ
    # cb.reqStkClosedCompactsSync(accountID, accountKey)
    # ���������˺��ʲ�����
    # cb.reqCreditDetailSync(accountID,accountKey)

    # �첽�������demo

    # �����˺��ʲ�����
    # cb.reqAccountDetail(accountID, accountKey)
    # ���������˺��ʲ�����
    # cb.reqCreditDetail(accountID,accountKey)
    # ����ί����ϸ
    # cb.reqOrderDetail(accountID,accountKey)
    # ����ɽ���ϸ
    # cb.reqDealDetail(accountID,accountKey)
    # cb.reqHistoryDealDetail(accountID,accountKey)
    # ����ֲ���ϸ
    # cb.reqPositionDetail(accountID,accountKey)
    # ����ֲ�ͳ��
    # cb.reqPositionStatics(accountID,accountKey)
    # �����˺���ʷ�ֲ�ͳ��
    # cb.reqHistoryPositionStatics(accountID,accountKey)
    # ��ѯ��������
    # cb.reqPriceData(accountID,accountKey)
    # ��ѯ��Ʒ��Ϣ
    # cb.reqProductData()
    # ��ѯ�û�����ָ����Ϣ
    # cb.reqCommandsInfo()

    # ��ѯ�ɶ�
    # cb.reqSecuAccount(accountID, accountKey)

    # ��ѯ���µ���
    # cb.reqCanOrderVolume(accountID, accountKey)
    # ��ѯδ�˽Ḻծ��Լ
    # cb.reqStkUnCloseCompacts(accountID, accountKey)
    # ��ѯ�г�״̬
    # cb.reqExchangeStatus(accountID, accountKey)
    # ˢ��δ�˽Ḻծ��Լ
    # cb.refreshStkUnCloseCompacts(accountID, accountKey)
    # ˢ�����˽Ḻծ��Լ
    # cb.refreshStkClosedCompacts(accountID, accountKey)

    # time.sleep(10000)
