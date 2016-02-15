------------
select * from tPurchase;
select * from tPurchaseData;

alter table tPurchase  add column contractAmountT varchar(36), /* Начальная (максимальная) цена контракта строкой */
alter table tPurchase  drop column customerName 
alter table tPurchase  add column customerName varchar(512), /* Начальная (максимальная) цена контракта строкой */

--    select * from tPurchaseFiles
-- 
-- select * from tErrorLog

select keyName, count(*) from tPurchaseData group by keyName order by 2 desc;
select * from tMapping;
select * from tPurchaseData where purchaseId=100;

update tPurchase p
set title = (
	select textValue512
	from tPurchaseData pd join tMapping mp
	on pd.keyName=mp.title and mp.tag='purchase_title' 
	where pd.purchaseId=p.purchaseId), 
responsible = (
	select textValue512
	from tPurchaseData pd join tMapping mp
	on pd.keyName=mp.title and mp.tag='contact_person' 
	where pd.purchaseId=p.purchaseId),
contractAmountT = (
	select textValue512
	from tPurchaseData pd join tMapping mp
	on pd.keyName=mp.title and mp.tag='purchase_amount' 
	where pd.purchaseId=p.purchaseId),
customerName = (
	select textValue512
	from tPurchaseData pd join tMapping mp
	on pd.keyName=mp.title and mp.tag='purchase_customer' 
	where pd.purchaseId=p.purchaseId limit 1)
	
;	
	
select * from tPurchase