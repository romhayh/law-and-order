use [law and order];
go
--create table [cities](
--	[city id] int identity(1, 1),
--	[city name] varchar(30)
--	primary key ([city id])
--);
--go

--create table [people](
--	[person id] int identity(1, 1),
--	[full name] varchar(60),
--	[age] int,
--	[city id] int foreign key references cities([city id]),
--	[birthdate] date
--	primary key ([person id])
--);
--go

--create table [specializations](
--	[specialization id] int identity(1,1) primary key,
--	[area] varchar(40) unique
--);
--go

--create table [bar](
--	[bar id] int identity(1,1) primary key,
--	[person id] int unique foreign key references [people]([person id]),
--	[specialization id] int foreign key references [specializations]([specialization id])
--);
--go

-- create table [firms](
-- 	[firm id] int identity(1,1) primary key,
-- 	[name] varchar(90),
-- 	[city id] int constraint _1 foreign key references [cities]([city id])

-- );
-- go

----! rank is for lawyers
-- create table [ranks](
-- 	[rank id] int identity(1,1) primary key,
-- 	[rank] varchar(40)
-- );
-- go

-- create table [lawyers](
-- 	[person id] int unique foreign key references [people]([person id]),
-- 	[bar id] int unique foreign key references [bar]([bar id]),
-- 	[rank id] int foreign key references [ranks]([rank id]),
-- 	[firm id] int foreign key references [firms]([firm id])
-- 	constraint _pk primary key ([person id], [bar id])

-- );


----! level is for courts
--create table [levels](
--	[level id] int identity(1,1) primary key,
--	[level] varchar(40)
--);
--go

--create table [courts](
--	[court id] int identity(1,1) primary key,
--	[city id] int foreign key references [cities]([city id]),
--	[name] varchar(80) unique,
--	[level id] int foreign key references [levels]([level id])
--)

--go
--create table [judges](
--	[person id] int unique foreign key references [people]([person id]),
--	[court id] int foreign key references [courts]([court id])
--	constraint _ primary key ([person id], [court id])
--)
