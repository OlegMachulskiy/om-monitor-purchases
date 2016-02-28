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

  insert into tPurchaseTags (purchaseId, tagLabel)
    select purchaseId, 'Якутск' from tPurchaseDetails pd
    where (lower(title) not like '%москв%' AND lower(customername) not like '%москв%') AND
	(lower(title) like '%якут%' OR lower(customername) like '%якут%')
    and not exists (select 1 from tPurchaseTags ptg where pd.purchaseId=ptg.purchaseId and ptg.tagLabel='Якутск');


  insert into tPurchaseTags (purchaseId, tagLabel)
    select purchaseId, 'Красноярск' from tPurchaseDetails pd
    where (lower(title) not like '%москв%' AND lower(customername) not like '%москв%') AND
	(lower(title) like '%красноярск%' OR lower(customername) like '%красноярск%')
    and not exists (select 1 from tPurchaseTags ptg where pd.purchaseId=ptg.purchaseId and ptg.tagLabel='Красноярск');


  insert into tPurchaseTags (purchaseId, tagLabel)
    select purchaseId, 'Челябинск' from tPurchaseDetails pd
    where (lower(title) not like '%москв%' AND lower(customername) not like '%москв%') AND
	(lower(title) like '%челябинск%' OR lower(customername) like '%челябинск%')
    and not exists (select 1 from tPurchaseTags ptg where pd.purchaseId=ptg.purchaseId and ptg.tagLabel='Челябинск');

  insert into tPurchaseTags (purchaseId, tagLabel)
    select purchaseId, 'МарийЭл' from tPurchaseDetails pd
    where (lower(title) not like '%москв%' AND lower(customername) not like '%москв%') AND
	(lower(title) like '%марий%эл%' OR lower(customername) like '%марий%эл%' OR lower(title) like '%йошкар%ола%' OR lower(customername) like '%йошкар%ола%')
    and not exists (select 1 from tPurchaseTags ptg where pd.purchaseId=ptg.purchaseId and ptg.tagLabel='МарийЭл');

  insert into tPurchaseTags (purchaseId, tagLabel)
    select purchaseId, 'Челябинск' from tPurchaseDetails pd
    where (lower(title) not like '%москв%' AND lower(customername) not like '%москв%') AND
	(lower(title) like '%челябинск%' OR lower(customername) like '%челябинск%')
    and not exists (select 1 from tPurchaseTags ptg where pd.purchaseId=ptg.purchaseId and ptg.tagLabel='Челябинск');
    
select * from tPurchaseDetails where purchaseId not in  (select purchaseId from tPurchaseTags WHERE tagLabel in ('Якутск', 'Красноярск', 'Челябинск', 'МарийЭл'))
and lower(customerName) not like '%моск%'


select * from tPurchaseContracts cnt join tContractRawData cdd on cnt.purchaseContractId = cdd.purchaseContractId order by 1, keyName

select * from tPurchaseContracts  where winnerInn is not Null





select * from tOrganization

select * from tPurchaseContracts where lower(customerName) like '%гагаринск%'


select distinct winnerINN from tPurchaseContracts

delete from tOrganization 

insert into tOrganization (orgId, inn) 
(select nextval('idGen'), winnerINN from  tPurchaseContracts tpc where not exists (select * from tOrganization  tpd1 where tpd1.inn = tpc.winnerINN) and winnerINN is not null)


update tOrganization set winnerName=


select * from tHTTPProxies
select * from tSourceQueries order by 1
update tSourceQueries set lastRun = NULL

insert into tPartner (partnerId, inn, category)
(select nextval('idGen'), winnerINN, 'O' from  (select distinct winnerINN from tPurchaseContracts) tpc 
where not exists (select * from tPartner  tpd1 where tpd1.inn = tpc.winnerINN) and winnerINN is not null)

select pp.partnerId , pp.inn, pp.p_name, pp._loadDate, oo.orgFullName, oo.directorName, oo.directorPosition, oo.address, oo.description, oo.url_sbis
from tPartner pp join tOrganization oo on  pp.partnerId = oo.partnerId

select * from tPartnerRelation
select * from tOrganization
delete from tPartner
SELECT DISTINCT url_sbis FROM tPartnerURLQueue WHERE url_sbis IS NOT NULL


with qq as (
select distinct  /*partnerId1, partnerId2, */ title, p1.p_name as name1, p2.p_name as name2
from tPartnerRelation tpr
join tPartner p1 on tpr.partnerId1 = p1.partnerId
join tPartner p2 on tpr.partnerId2 = p2.partnerId
)
select name2, count(1) 
from qq group by name2
order by 2 desc

select *
from tPartnerRelation tpr
join tPartner p1 on tpr.partnerId1 = p1.partnerId
join tPartner p2 on tpr.partnerId2 = p2.partnerId
where p2.p_name='Ермолаев Вячеслав Вячеславович'


select * from tPurchaseBid


        insert into tPurchaseTags (purchaseId, tagLabel)
        select purchaseId, 'Гагаринский' from tPurchaseDetails pd
        where (lower(title) like '%москв%' OR lower(customername) like '%москв%') AND
            (lower(title) like '%гагаринск%' OR lower(customername) like '%гагаринск%')
        and not exists (select 1 from tPurchaseTags ptg where pd.purchaseId=ptg.purchaseId and ptg.tagLabel='Гагаринский');

select * from tPurchaseDetails pd
        where (lower(title) like '%москв%' OR lower(customername) like '%москв%') AND
            (lower(title) like '%гагаринск%' OR lower(customername) like '%гагаринск%')

update tPurchase set lastUpdate = null where purchaseId in (
select purchaseId from         tPurchaseDetails   where title is null);

select distinct keyname, textvalue from         tPurchaseRawData where (lower(textValue) like '%москв%' OR lower(textValue) like '%москв%') AND
            (lower(textValue) like '%гагаринск%' OR lower(textValue) like '%гагаринск%')

select * from tPurchaseRawData where purchaseId=29091
select * from tPurchaseDetails
select count(1) from tPurchaseRawData union all
select count(1)  from tPurchaseDetails WHERE purchaseId not in (select distinct purchaseId from tPurchaseRawData)

select distinct exc_value from tErrorLog            