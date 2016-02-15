
DROP SEQUENCE idGen ;
CREATE SEQUENCE idGen START 100 ;

DROP TABLE tErrorLog;
DROP TABLE tOrganization;
DROP TABLE tPurchaseData;
DROP TABLE tPurchaseFiles;
DROP TABLE tPurchase ;
	
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
	customerName varchar(512),
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
	contractAmountT varchar(36), /* Начальная (максимальная) цена контракта строкой */
	contractCurrency VARCHAR(36) NULL, 
	_url	varchar(512),
	_loadDate  timestamp default now(),
	PRIMARY KEY (purchaseId)
);

CREATE TABLE  tPurchaseData (
	purchaseId numeric(36) NOT NULL, 
	keyName	VARCHAR(512) NOT NULL, 
	textValue	text,
	textValue512	varchar(512),
	_loadDate  timestamp default now(),
	PRIMARY KEY (purchaseId, keyName),
	FOREIGN KEY (purchaseId) REFERENCES tPurchase ON DELETE CASCADE
);

CREATE TABLE  tPurchaseFiles (
	purchaseFileId numeric(36) NOT NULL, 
	purchaseId numeric(36) NOT NULL, 
	url	VARCHAR(512) NOT NULL, 
	title	VARCHAR(512) NOT NULL, 
	filename	VARCHAR(512), 
	_loadDate  timestamp default now(),
	PRIMARY KEY (purchaseFileId),
	FOREIGN KEY (purchaseId) REFERENCES tPurchase ON DELETE CASCADE
);



CREATE TABLE  tOrganization (
	orgId numeric(36) NOT NULL, 
	competence varchar(100) , /* Полномочия организации */
	title VARCHAR(512) NULL, /* Полное наименование */
	
	_loadDate  timestamp default now(),
	_url	varchar(512),
	PRIMARY KEY (orgId)
);

create table tMapping (
	title	VARCHAR(512) NOT NULL, 
	tag	VARCHAR(512) NOT NULL, 
	primary key (title,tag)
	);

delete from tMapping;
insert into tMapping (title, tag) values ('Наименование закупки','purchase_title');
insert into tMapping (title, tag) values ('Наименование объекта закупки','purchase_title');
insert into tMapping (title, tag) values ('Заказчик','purchase_customer');
insert into tMapping (title, tag) values ('Организация','contact_org');
insert into tMapping (title, tag) values ('Контактное лицо','contact_person');
insert into tMapping (title, tag) values ('Ответственное должностное лицо','contact_person');
insert into tMapping (title, tag) values ('Электронная почта','contact_email');
insert into tMapping (title, tag) values ('Телефон','contact_phone');
insert into tMapping (title, tag) values ('Начальная (максимальная) цена контракта','purchase_amount');
insert into tMapping (title, tag) values ('Организация, осуществляющая закупку','purchase_customer');
insert into tMapping (title, tag) values ('Закупку осуществляет','purchase_customer');




--------------
--    select * from tPurchase
--    select * from tPurchaseData
--    select * from tPurchaseFiles
-- select keyName, count(*) from tPurchaseData group by keyName
-- select * from tErrorLog