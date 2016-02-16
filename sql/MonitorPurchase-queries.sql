------------
select * from tPurchase;
select * from tPurchaseData;

alter table tPurchase  add column contractAmountT varchar(36), /* Начальная (максимальная) цена контракта строкой */
alter table tPurchase  drop column customerName 
alter table tPurchase  add column customerName varchar(512), /* Начальная (максимальная) цена контракта строкой */

--    select * from tPurchaseFiles
-- 
-- select * from tErrorLog

select keyName, count(*) from tPurchaseRawData where keyname like '%Дата%' group by keyName order by 2 desc;
select * from tMapping;
select * from tPurchaseData where purchaseId=100;




insert into tPurchaseDetails (purchaseId) 
	(select purchaseId from  tPurchase tp 
	where not exists (select * from tPurchaseDetails  tpd1 where tpd1.purchaseId = tp.purchaseId))
	

update tPurchaseDetails p
set title = (
	select textValue512
	from tPurchaseRawData pd join tMapping mp
	on pd.keyName=mp.title and mp.tag='purchase_title' 
	where pd.purchaseId=p.purchaseId), 
responsible = (
	select textValue512
	from tPurchaseRawData pd join tMapping mp
	on pd.keyName=mp.title and mp.tag='contact_person' 
	where pd.purchaseId=p.purchaseId),
contractAmountT = (
	select textValue512
	from tPurchaseRawData pd join tMapping mp
	on pd.keyName=mp.title and mp.tag='purchase_amount' 
	where pd.purchaseId=p.purchaseId),
customerName = (
	select textValue512
	from tPurchaseRawData pd join tMapping mp
	on pd.keyName=mp.title and mp.tag='purchase_customer' 
	where pd.purchaseId=p.purchaseId limit 1), 
stage = (
	select textValue512
	from tPurchaseRawData pd join tMapping mp
	on pd.keyName=mp.title and mp.tag='purchase_stage' 
	where pd.purchaseId=p.purchaseId limit 1),
purchaseType = (
	select textValue512
	from tPurchaseRawData pd join tMapping mp
	on pd.keyName=mp.title and mp.tag='purchase_type' 
	where pd.purchaseId=p.purchaseId limit 1), 
submitStartT = (
	select textValue512
	from tPurchaseRawData pd join tMapping mp
	on pd.keyName like mp.title||'%' and mp.tag='submit_start' 
	where pd.purchaseId=p.purchaseId limit 1), 
submitFinishT = (
	select textValue512
	from tPurchaseRawData pd join tMapping mp
	on pd.keyName like mp.title||'%' and mp.tag='submit_end' 
	where pd.purchaseId=p.purchaseId limit 1),
requestPublishedT = (
	select textValue512
	from tPurchaseRawData pd join tMapping mp
	on pd.keyName like mp.title||'%' and mp.tag='request_published' 
	where pd.purchaseId=p.purchaseId limit 1)
;	



SELECT pp.purchaseId,
       orderId,
       customerName,
       title,
       purchaseType,
       stage ,
       contractAmountT,
	requestPublishedT,
       submitStartT,
       submitFinishT,
       responsible,
       _url,
       _loaddate
FROM tPurchase pp
JOIN tPurchaseDetails ppd ON pp.purchaseId = ppd.purchaseId
WHERE ppd.title IS NOT NULL
	
select * from tPurchaseRawData where purchaseId=2131


select * from tPurchaseRawData limit 4
select count(1) from tPurchaseRawData 

SELECT purchaseId, orderId, _url, _loadDate FROM tPurchase WHERE lastRun is null



select * from tPurchaseContracts;

select winnerName, count(1) from tPurchaseContracts 
where purchaseId in (select purchaseId from tPurchaseTags WHERE tagLabel in ('Гагаринский', 'ВоробьевыГоры'))
group by winnerName order by 2 desc
;

select * from tPurchase vp  
	join tPurchaseContracts pcc on vp.purchaseId = pcc.purchaseId 
	join tPurchaseDetails ppd on vp.purchaseId =ppd.purchaseId 
where  vp.purchaseId in (select purchaseId from tPurchaseTags WHERE tagLabel in ('Гагаринский', 'ВоробьевыГоры'))
;
where lower(winnerName) like '%вангард%'

;


select * from tMapping


SELECT
    table_schema || '.' || table_name AS table_full_name,
    pg_size_pretty(pg_total_relation_size('"' || table_schema || '"."' || table_name || '"')) AS size
FROM information_schema.tables
ORDER BY
    pg_total_relation_size('"' || table_schema || '"."' || table_name || '"') DESC




select * from tPurchase where purchaseId not in (select purchaseId from tPurchaseContracts)

--update tPurchase set lastRun=null where purchaseId not in (select purchaseId from tPurchaseContracts)

insert into tPurchaseTags (purchaseId, tagLabel)
select purchaseId, 'Гагаринский' from tPurchaseDetails pd
where (lower(title) like '%москв%' OR lower(customername) like '%москв%') AND
	(lower(title) like '%гагаринск%' OR lower(customername) like '%гагаринск%')
and not exists (select 1 from tPurchaseTags ptg where pd.purchaseId=ptg.purchaseId and ptg.tagLabel='Гагаринский');



insert into tPurchaseTags (purchaseId, tagLabel)
select purchaseId, 'ВоробьевыГоры' from tPurchaseDetails pd
where (lower(title) like '%москв%' OR lower(customername) like '%москв%') AND
	(lower(title) like '%вороб%' OR lower(customername) like '%вороб%')
and not exists (select 1 from tPurchaseTags ptg where pd.purchaseId=ptg.purchaseId and ptg.tagLabel='ВоробьевыГоры');


insert into tPurchaseTags (purchaseId, tagLabel)
select purchaseId, 'Раменки' from tPurchaseDetails pd
where (lower(title) like '%москв%' OR lower(customername) like '%москв%') AND
	(lower(title) like '%рамен%' OR lower(customername) like '%рамен%')
and not exists (select 1 from tPurchaseTags ptg where pd.purchaseId=ptg.purchaseId and ptg.tagLabel='Раменки');

