------------
select * from tSourceQueries order by 1;

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

delete from tPurchaseTags


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


select * from tPurchaseBid  order by _loadDate desc


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



select * from tPurchaseRawData where purchaseId=39075
select *
            from tPurchaseRawData pd 
            WHERE pd.keyName in ('Наименование закупки', 'Наименование объекта закупки')
            AND purchaseId=39075

select * from tPurchase where purchaseId=39075

select count(1)  from tPurchaseRawData
delete from tPurchaseFiles
delete from tPurchaseContracts

select * from tHTTPProxyResult order by _loadDate desc


with stats as (
	select proxy, avg(timeout) as avg_ok, count(timeout) as count_ok, 0 as avg_err, 0 as count_err from tHTTPProxyResult where result='Success' group by proxy 
	union all
	select proxy, 0 as avg_ok, 0 as count_ok, avg(timeout)  as avg_err, count(timeout) as  count_err from tHTTPProxyResult where result is NULL OR result <>'Success' group by proxy 
	union all 
	select proxy, 10000 as avg_ok, 1 as count_ok, 10000 as avg_err, 1 as count_err from tHTTPProxies where proxy not in (select distinct proxy from tHTTPProxyResult)
), stats1 as (
	select proxy, sum(avg_ok) as avg_ok, sum(count_ok) as count_ok, sum(avg_err) as avg_err, sum(count_err) as count_err from stats group by proxy
), weighted as 
(
	select proxy, avg_ok, count_ok, avg_err, count_err, (count_err)/(count_ok) as error_rate, 1000000/(avg_ok+avg_err)  as weight
	from stats1 
	where count_ok > 0
) select proxy , (weight/( 1 + error_rate))^2 as weight1, avg_ok , * from weighted 
where proxy <> 'No_Proxy'
order by  weight1 desc



--#update tPurchase set lastUpdate=NULL where not exists (select purchaseId from tPurchaseRawData where tPurchaseRawData.purchaseId=tPurchase.purchaseId)--
select * from tPurchase where purchaseId=39459

delete from tPurchaseTags



select * from tPartner where partnerId in (143460, 101229)

select * from tPartnerRelation

select distinct tagLabel from tPurchaseTags



select * from tPartner where inn in (
select distinct winnerINN from tPurchaseTags tpt 
join tPurchaseDetails  tpd  on tpd.purchaseId=tpt.purchaseId
left join tPurchaseContracts tpc on tpc.purchaseId=tpd.purchaseId
where tpt.tagLabel in ('Гагаринский', 'ВоробьевыГоры','Академический') 
and winnerINN is not null
)

--join tPurchaseDetails  tpd1  on tpd1.customerName=tpd.customerName
/*, ,'ПрефектураЮЗАО' /*,'Вернадского','Университетский','Раменки','Ленинский')*/

select * from tPurchaseContracts limit 100
select * from tPurchase limit 100
select * from tPurchaseDetails limit 100
select * from tPartner limit 100
select * from tOrganization limit 100
select * from tContractRawData limit 100

select * from tPurchase pp  JOIN tPurchaseDetails ppd ON pp.purchaseId = ppd.purchaseId where pp.purchaseId=6225
select * from tPurchaseContracts  where purchaseId=6225
select * from tPartner where inn='7736192449'


update tPurchaseContracts p
        set winnerINN = (
            select textValue512
            from tContractRawData crd join tMapping mp
            on crd.purchaseContractId=p.purchaseContractId and keyName='participantInfoTable:ИНН:' limit 1)
        where winnerINN  is null

select * from tContractRawData where purchaseContractId=171877

select * from tOrganization where partnerId=101505


select * from tPurchaseBid where partnerId is not null
select * from tPurchaseBidRawData

select distinct textValue512 
from tPurchaseBidRawData tbrd join tPurchaseBid tb ON tbrd.bidId=tb.bidId
WHERE keyName='ИНН'




select * from tPurchaseContracts tpc where winnerINN is not null
and not exists (select 1 from tPurchaseBid           tpb where tpc.purchaseId=tpb.purchaseId)
and lower(customerName) like '%моск%'


SELECT bidId, purchaseId, url, partnerId FROM tPurchaseBid
                WHERE 
                 partnerId IS NULL                    
                 OR 
                bidId NOT IN (SELECT DISTINCT bidId FROM tPurchaseBidRawData)


SELECT purchaseId, bidId, tpb.partnerId , inn, p_name, category 
FROM tPurchaseBid tpb join tPartner tp on tpb.partnerId=tp.partnerId


select * from tPurchase where purchaseId=110
select * from tPurchaseDetails where purchaseId=110
select * from tPurchaseBid order by bidId desc limit 1000 -- where purchaseId=110
--update tPurchase set lastUpdate=Null where purchaseId not in (select purchaseId from tPurchaseBid )


select * from tPurchase where lastUpdate is null




select cast(_loadDate as date), count(1)  from tPurchase
group by cast(_loadDate as date) order by 1 desc

