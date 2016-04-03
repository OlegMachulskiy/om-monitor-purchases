import simplejson


class Purchase():
    def __init__(self):
        self._url = None
        self._loadDate = None
        self.purchaseId = None
        self.orderId = None
        self.bids = []  # PurchaseBid
        self.purchaseContract = None

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
    def __init__(self, purchaseId, url, purchaseContractId = None, contractNo = None, customerName = None, priceT = None, winnerName = None, pushishDateT = None):
        self.purchaseId = purchaseId
        self.url = url
        self.purchaseContractId = purchaseContractId
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


class Partner:
    def __init__(self):
        self.partnerId = None
        self.inn = None
        self.p_name = None

    def __repr__(self):
        rv = "<" + type(self).__name__ + ":"
        rv += str(self.partnerId) + ', '
        if self.inn != None:
            rv += self.inn + ', '
        if self.p_name != None:
            rv += self.p_name + '>'
        return rv


class Person(Partner):
    def __init__(self):
        Partner.__init__(self)


class Organization(Partner):
    def __init__(self):
        Partner.__init__(self)
        self.url_sbis = None


class PurchaseBid:
    def __init__(self, bidId=None, purchaseId=None, partnerId=None, url=None, participantName=None):
        self.bidId = bidId
        self.purchaseId = purchaseId
        self.partnerId = partnerId
        self.url = url
        self.participantName = participantName

    def __repr__(self):
        rv = "<PurchaseBid:"
        rv += str(self.bidId) + ', '
        rv += str(self.url) + '>'
        return rv.encode('utf-8')


class PurchaseProtocol:
    def __init__(self, purchaseId, protocol_url, purchaseProtocolId=None):
        self.purchaseId = purchaseId
        self.protocol_url = protocol_url
        self.purchaseProtocolId = purchaseProtocolId


class MyEncoder(simplejson.JSONEncoder):
    def default(self, o):
        return o.__dict__


if __name__ == '__main__':
    pb = PurchaseBid()
    print simplejson.dumps(pb, cls=MyEncoder)
