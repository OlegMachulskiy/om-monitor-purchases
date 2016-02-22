class Purchase:
    def __init__(self):
        self._url = None
        self._loadDate = None
        self.purchaseId = None
        self.orderId = None
        # self.orderDate = None
        # self.purchaseType = None
        # self.customer_orgId = None
        # self.title = None
        # self.stage = None
        # self.responsible = None
        # self.respons_email = None
        # self.respons_phone = None
        # self.contractMgr = None
        # self.submitStart = None
        # self.submitFinish = None
        # self.submitPlace = None
        # self.submitConditions = None
        # self.contractAmount = None
        # self.contractCurrency = None

    # def __init__(self, orderId, url):
    #     self.__init__()
    #     self.orderId = orderId;
    #     self._url = url
    def __repr__(self):
        rv = "<Purchase:";
        rv += str(self.purchaseId) + ', ';
        rv += self.orderId + ', ';
        rv += str(self._loadDate) + ', ';
        rv += self._url.encode('utf-8') + '>';
        return rv


class PurchaseFile:
    def __init__(self, purchaseId, purchaseFileId, url, title, filename):
        self.purchaseId = purchaseId
        self.purchaseFileId = purchaseFileId
        self.url = url
        self.title = title
        self.filename = filename

    def __repr__(self):
        rv = "<PurchaseFile:";
        rv += str(self.purchaseId) + ', ';
        rv += str(self.purchaseFileId) + ', ';
        if self.url != None:
            rv += self.url.encode('utf-8') + ', ';
        if self.title != None:
            rv += self.title.encode('utf-8') + ', ';
        if self.filename != None:
            rv += self.filename.encode('utf-8') + '>';
        return rv


class PurchaseContract:
    def __init__(self, purchaseId, url, contractNo, customerName, winnerName, priceT, pushishDateT):
        self.purchaseId = purchaseId
        self.purchaseContractId = None
        self.url = url
        self.contractNo = contractNo
        self.customerName = customerName
        self.priceT = priceT
        self.winnerName = winnerName
        self.pushishDateT = pushishDateT

    def __repr__(self):
        rv = "<PurchaseContract:"
        rv += str(self.purchaseId) + ', '
        rv += str(self.purchaseContractId) + ', '
        if self.url != None:
            rv += (self.url) + ', '
        # if self.contractNo != None:
        #     rv += (self.contractNo) + ', '
        # if self.customerName != None:
        #     rv += (self.customerName) + ','
        # if self.winnerName != None:
        #     rv += (self.winnerName) + ','
        # if self.pushishDateT != None:
        #     rv += (self.pushishDateT) + '>'
        return rv.encode('utf-8')


class Organization:
    def __init__(self):
        self.orgId = None
        self.inn = None
        self.title = None
        self.url_sbis = None

    def __repr__(self):
        rv = "<Organization:";
        rv += str(self.orgId) + ', ';
        if self.inn != None:
            rv += self.inn + ', ';
        if self.title != None:
            rv += self.title + ', ';
        if self.url_sbis != None:
            rv += self.url_sbis + '>';
        return rv
