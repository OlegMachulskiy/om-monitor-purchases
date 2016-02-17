
DROP SEQUENCE idGen ;
CREATE SEQUENCE idGen START 100 ;

--DROP VIEW vPurchases;

DROP TABLE tPurchaseTags;
DROP TABLE tPurchase2Query;
DROP TABLE tErrorLog;
DROP TABLE tOrganization;
DROP TABLE tPurchaseRawData;-- DROP TABLE tPurchaseData;
DROP TABLE tPurchaseFiles;
DROP TABLE tPurchaseContracts;
DROP TABLE tPurchaseDetails;
DROP TABLE tPurchase ;
DROP TABLE tMapping ;
DROP TABLE tSourceQueries;
	
CREATE TABLE tErrorLog (
	message VARCHAR(512) NULL, 
	exc_type  VARCHAR(512) NULL, 
	exc_value VARCHAR(512) NULL, 
	exc_traceback TEXT ,
	loadDate     timestamp default now()
);

CREATE TABLE  tSourceQueries (
	queryId numeric(36) NOT NULL, 
	qText 	varchar(512),
	lastRun	timestamp ,
	_loadDate  timestamp default now(),
	PRIMARY KEY (queryId)
);


CREATE TABLE  tPurchase (
	purchaseId numeric(36) NOT NULL, 
	orderId	VARCHAR(36) NULL, 
	lastRun	timestamp ,
	_url	varchar(512),
	_loadDate  timestamp default now(),
	PRIMARY KEY (purchaseId)
);


CREATE TABLE tPurchase2Query (
	purchaseId numeric(36) NOT NULL, 
	queryId numeric(36) NOT NULL, 
	_loadDate  timestamp default now(),
	PRIMARY KEY (purchaseId, queryId),
	FOREIGN KEY (purchaseId) REFERENCES tPurchase ON DELETE CASCADE,
	FOREIGN KEY (queryId) REFERENCES tSourceQueries ON DELETE CASCADE
);

CREATE TABLE tPurchaseDetails (
	purchaseId numeric(36) NOT NULL, 
	orderDate date,
	purchaseType VARCHAR(512) NULL, /* Способ определения поставщика  */
	customer_orgId numeric(512), /* Закупку осуществляет */
	customerName varchar(512),
	title	varchar(512), /* Наименование объекта закупки */
	stage VARCHAR(36) , /* Этап закупки */
	responsible VARCHAR(128) NULL, /* Ответственное должностное лицо  */
	respons_email VARCHAR(128) NULL, /* Адрес электронной почты  */
	respons_phone VARCHAR(128) NULL, /* Номер контактного телефона  */
	contractMgr VARCHAR(128) NULL, /* Информация о контрактной службе, контрактном управляющем  */
	requestPublished timestamp, /* дата публикации */
	requestPublishedT varchar(36), /* дата публикации */
	submitStart timestamp, /* Дата и время начала подачи котировочных заявок */
	submitStartT varchar(36), /* Дата и время начала подачи котировочных заявок */
	submitFinish timestamp, /* Дата и время окончания подачи котировочных заявок */
	submitFinishT varchar(36), /* Дата и время окончания подачи котировочных заявок */
	submitPlace VARCHAR(512) NULL, /* Место подачи котировочных заявок */
	submitConditions TEXT NULL, /* Порядок подачи котировочных заявок */
	contractAmount NUMERIC(20,2), /* Начальная (максимальная) цена контракта */
	contractAmountT varchar(36), /* Начальная (максимальная) цена контракта строкой */
	contractCurrency VARCHAR(36) NULL, 
	PRIMARY KEY (purchaseId), 
	FOREIGN KEY (purchaseId) REFERENCES tPurchase ON DELETE CASCADE
);

CREATE TABLE  tPurchaseRawData (
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

CREATE TABLE  tPurchaseContracts (
	purchaseContractId numeric(36) NOT NULL, 
	purchaseId numeric(36) NOT NULL, 
	url	VARCHAR(512) NOT NULL, 
	contractNo VARCHAR(128) ,
	customerName	VARCHAR(512), 
	winnerName VARCHAR(512), 
	priceT VARCHAR(128) ,
	pushishDateT VARCHAR(128) ,
	_loadDate  timestamp default now(),
	PRIMARY KEY (purchaseContractId),
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

create table tPurchaseTags (
	purchaseId numeric(36) NOT NULL, 
	tagLabel 	varchar(36) NOT NULL, 
	PRIMARY KEY (purchaseId, tagLabel),
	FOREIGN KEY (purchaseId) REFERENCES tPurchase ON DELETE CASCADE
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
insert into tMapping (title, tag) values ('Этап закупки','purchase_stage');
insert into tMapping (title, tag) values ('Способ размещения закупки','purchase_type');
insert into tMapping (title, tag) values ('Способ определения поставщика (подрядчика, исполнителя)','purchase_type');
insert into tMapping (title, tag) values ('Дата и время начала подачи котировочных заявок','submit_start');
insert into tMapping (title, tag) values ('Дата и время начала подачи заявок','submit_start');
insert into tMapping (title, tag) values ('Дата и время начала подачи заявок (по местному времени)','submit_start');
insert into tMapping (title, tag) values ('Дата и время окончания подачи котировочных заявок','submit_end');
insert into tMapping (title, tag) values ('Дата и время окончания подачи заявок','submit_end');
insert into tMapping (title, tag) values ('Дата и время окончания подачи заявок (по местному времени заказчика)','submit_end');
insert into tMapping (title, tag) values ('Дата и время окончания подачи заявок (по местному времени)','submit_end');
insert into tMapping (title, tag) values ('Дата размещения текущей редакции извещения','request_published');
insert into tMapping (title, tag) values ('Дата размещения извещения','request_published');

delete from  tSourceQueries;

INSERT INTO tSourceQueries (queryId , qText) VALUES (nextval('idGen'), 'Жилищник Гагаринского');
INSERT INTO tSourceQueries (queryId , qText) VALUES (nextval('idGen'), 'Управа Гагаринского');
INSERT INTO tSourceQueries (queryId , qText) VALUES (nextval('idGen'), 'Проспект Вернадского');
INSERT INTO tSourceQueries (queryId , qText) VALUES (nextval('idGen'), 'Улица Косыгина');
INSERT INTO tSourceQueries (queryId , qText) VALUES (nextval('idGen'), 'Воробьевы горы');
INSERT INTO tSourceQueries (queryId , qText) VALUES (nextval('idGen'), 'Ломоносовский проспект');
INSERT INTO tSourceQueries (queryId , qText) VALUES (nextval('idGen'), 'Район Раменки');
INSERT INTO tSourceQueries (queryId , qText) VALUES (nextval('idGen'), 'Жилищник района Академический');
INSERT INTO tSourceQueries (queryId , qText) VALUES (nextval('idGen'), 'Ленинский проспект');
INSERT INTO tSourceQueries (queryId , qText) VALUES (nextval('idGen'), 'ЮЗАО');
INSERT INTO tSourceQueries (queryId , qText) VALUES (nextval('idGen'), 'дворец пионеров');
INSERT INTO tSourceQueries (queryId , qText) VALUES (nextval('idGen'), 'природопользования');
INSERT INTO tSourceQueries (queryId , qText) VALUES (nextval('idGen'), 'Университетский');
INSERT INTO tSourceQueries (queryId , qText) VALUES (nextval('idGen'), 'Вавилова');
INSERT INTO tSourceQueries (queryId , qText) VALUES (nextval('idGen'), 'Ляпунова');
INSERT INTO tSourceQueries (queryId , qText) VALUES (nextval('idGen'), 'Бардина');



--------------
--    select * from tPurchase
--    select * from tPurchaseData
--    select * from tPurchaseFiles
-- select keyName, count(*) from tPurchaseData group by keyName
-- select * from tErrorLog

