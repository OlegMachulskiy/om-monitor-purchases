
DROP SEQUENCE idGen ;
CREATE SEQUENCE idGen START 100 ;

DROP TABLE tErrorLog;
DROP TABLE tPurchase ;
DROP TABLE tOrganization ;

CREATE TABLE tErrorLog (
	message VARCHAR(512) NULL, 
	exc_type  VARCHAR(512) NULL, 
	exc_value VARCHAR(512) NULL, 
	exc_traceback TEXT ,
	loadDate     timestamp default now()
);

CREATE TABLE  tPurchase (
	purchaseId numeric(36) NOT NULL, 
	orderId	VARCHAR(36) NULL, 
	orderDate date,
	purchaseType VARCHAR(36) NULL, /* Способ определения поставщика  */
	customer_orgId numeric(36), /* Закупку осуществляет */
	title	varchar(512), /* Наименование объекта закупки */
	stage VARCHAR(36) , /* Этап закупки */
	responsible VARCHAR(128) NULL, /* Ответственное должностное лицо  */
	respons_email VARCHAR(128) NULL, /* Адрес электронной почты  */
	respons_phone VARCHAR(128) NULL, /* Номер контактного телефона  */
	contractMgr VARCHAR(128) NULL, /* Информация о контрактной службе, контрактном управляющем  */
	submitStart timestamp, /* Дата и время начала подачи котировочных заявок */
	submitFinish timestamp, /* Дата и время окончания подачи котировочных заявок */
	submitPlace VARCHAR(512) NULL, /* Место подачи котировочных заявок */
	submitConditions TEXT NULL, /* Порядок подачи котировочных заявок */
	contractAmount NUMERIC(20,2), /* Начальная (максимальная) цена контракта */
	contractCurrency VARCHAR(36) NULL, 
	_url	varchar(512),
	_loadDate  timestamp default now(),
	PRIMARY KEY (purchaseId)
);

CREATE TABLE  tOrganization (
	orgId numeric(36) NOT NULL, 
	competence varchar(100) , /* Полномочия организации */
	title VARCHAR(512) NULL, /* Полное наименование */
	
	_loadDate  timestamp default now(),
	_url	varchar(512),
	PRIMARY KEY (orgId)
);


--------------
--    select * from tPurchase