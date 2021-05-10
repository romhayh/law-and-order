use [law and order];
go

-- the firm with most defendants found innocent:
select top 1 o.[name], max(o.[defendants found innocent]) as [defendants found innocent]
from 
	-- how many defendants found innocent in each firm
	(select f.[name], count(dfi.[person id]) as [defendants found innocent]
	from [firms] f, [lawyers] l,
		-- dfi stands for defendants found innocent
		(select distinct d1.[person id], d1.[trial id]
		 from [defendants] d1
		 where d1.conclusion = 'innocent') dfi,

		-- lid stands for lawyers in defense
		(select l1.[bar id], l1.[person id], l1.[trial id]
		 from [lawyers in trial] l1
		 where l1.[team] = 'Defense') lid
	where l.[bar id] = lid.[bar id] and l.[person id] = lid.[person id] and
		  l.[firm id] = f.[firm id] and 
		  lid.[trial id] = dfi.[trial id]
	group by f.[name]) o

group by o.[name]
order by [defendants found innocent] desc;


-- the worst person from Bat Yam:
select top 1 p.[full name], count(d.[trial id]) as [# of convictions]
from [people] p, [cities] c, [defendants] d
where d.[person id] = p.[person id] and
	  p.[city id] = c.[city id] and
	  c.[city name] = 'Bat Yam' and
	  d.conclusion <> 'innocent'
group by p.[full name]
order by [# of convictions] desc;


-- the most suspicious person:
-- (the person with most trials found innocent,
-- with no trials found guilty)
select distinct  top 1 p.[full name], dfi.[# of trials found innocent], c.[city name]

from [people] p,
	  -- dfi stands for defendants found innocent
	 (select d1.[person id], count(d1.[trial id]) as [# of trials found innocent]
	  from [defendants] d1
	  where d1.[conclusion] = 'innocent'
	  group by d1.[person id]) dfi,

	  -- dfg stands for defendants found guilty
	 (select distinct d2.[person id]
	  from [defendants] d2 
	  where d2.conclusion <> 'innocent') dfg,
	  [cities] c

where p.[person id] = dfi.[person id] and dfi.[person id] <> dfg.[person id] and p.[city id] = c.[city id]

order by dfi.[# of trials found innocent] desc



-- delete people that have no track record, not judges or lawyers:
delete from [people]
where [person id] not in(
	 select distinct p.[person id]
	 from [people] p,
	 (select distinct d1.[person id] from [defendants] d1) d,
	 (select distinct j1.[person id] from [judges] j1) j,
	 (select distinct l1.[person id] from [lawyers] l1) l
	 where p.[person id] = l.[person id] or p.[person id] = j.[person id] or p.[person id] = d.[person id])
;
go
print(@@servername);

-- the description for trials that took place in 'High Justice' courts, and the number of
-- judges, defendants, lawyers:
select o.[subject], o.[# of judges], o.[# of defendants], o.[defense], o.offense, t.[description]

from [trials] t,
	(select	t.[trial id], c.[name], d.[# of defendants], jit.[# of judges],
			s.[area] as [subject], lio.[offense], lid.[defense]

	from	[trials] t, [courts] c,
			[specializations] s, [levels] l,

			-- lawyers in Offense
			(select lito.[trial id],  count(lito.[person id]) as [offense]
			 from [lawyers in trial] lito
			 where lito.[team] = 'Offense'
			 group by lito.[trial id]) lio, 

			-- lawyers in Defense:
			(select litd.[trial id],  count(litd.[person id]) as [defense]
			 from [lawyers in trial] litd
			 where litd.[team] = 'Defense'
			 group by litd.[trial id]) lid,

			-- judges in trial:
			(select jit1.[trial id], count(jit1.[person id]) as [# of judges]
			 from [judges in trial] jit1
			 group by jit1.[trial id]) jit,
		 
			-- defendants in trial:
			(select d1.[trial id], count(d1.[person id]) as [# of defendants] 
			 from [defendants] d1
			 group by d1.[trial id]) d


	where	t.[trial id] = lid.[trial id] and t.[trial id] = lio.[trial id] and t.[trial id] = jit.[trial id] and  t.[trial id] = d.[trial id] 
			and
			c.[court id] = t.[court id] and c.[level id] = l.[level id] 
			and l.[level] = 'High Justice' and t.[subject id] = s.[specialization id]) o	
where t.[trial id] = o.[trial id]


-- the trials with more than 10 people participating in them:
select  t.[trial id], sum(lit.[# of lawyers] + jit.[# of judges] + d.[# of defendants]) as [# of people]

from [trials] t,
	-- lawyers in trial
	(select lit1.[trial id], count(lit1.[person id]) as [# of lawyers]
	 from [lawyers in trial] lit1
	 group by lit1.[trial id]) lit,
	
	-- judges in trial
	(select jit1.[trial id], count(jit1.[person id]) as [# of judges]
	 from [judges in trial] jit1
	 group by jit1.[trial id]) jit,
		 
	-- defendants in trial:
	(select d1.[trial id], count(d1.[person id]) as [# of defendants] 
	 from [defendants] d1
	 group by d1.[trial id]) d
where t.[trial id] = d.[trial id] and t.[trial id] = jit.[trial id] and t.[trial id] = lit.[trial id]

group by t.[trial id]

having sum(lit.[# of lawyers] + jit.[# of judges] + d.[# of defendants]) > 10

order by 2 asc;


-- the firm with most lawyers:
select top 1 f.[name], count(distinct l.[person id]) as [# of lawyers]
from [firms] f, [lawyers] l
where l.[firm id] = f.[firm id]
group by f.[name]
order by 2 desc

-- add column population to cities
alter table [cities]
add [population] int;

-- fill the population with 0:
update [cities]
set [population] = 0

-- fill the population of the database
update c
set [population] =  (
					select count(distinct p.[person id])
					from [people] p
					where p.[city id] = c.[city id]
					)
from [cities] c
go

-- show all rows in cities in descending order:
select * from [cities]
order by [population] desc;

-- show all people with the letters r.o.m letters in their names in this order - rom
select * from [people] p
where p.[full name] like '%r%o%m%';

-- this query returns the age of female judges
select top 50 p.[full name] as [name], datediff(day,p.birthdate, getdate())/365 as [age]
from [judges] j, [people] p
where j.[person id] = p.[person id]
	  and p.[gender] = 'female' 
order by 2 desc

-- a query that finds out what gender ages better as a judge
-- by giving us both gender`s ages
select females.age as [female avg age],  males.age as [male avg age]
from 
	-- this query returns the avg female age as a judge
	(select avg(datediff(year,p.birthdate, getdate())) as [age]
	 from [judges] j, [people] p
	 where j.[person id] = p.[person id]
	  	   and p.[gender] = 'female') females,
	-- this query returns the avg male age as a judge
	(select avg(datediff(year,p.birthdate, getdate())) as [age]
	 from [judges] j, [people] p
	 where j.[person id] = p.[person id]
	  	   and p.[gender] = 'male') males