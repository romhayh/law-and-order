create function cityidof (@name varchar(30))
returns int as
begin
    declare @ans int
	set @ans = (select [city id] from cities where [city name] = @name)
    return @ans
end;
go

drop function dbo.cityidof;

create function specializationidof (@area varchar(30))
returns int as
begin
    declare @ans int
	set @ans = (select s.[area] from specializations s where [area] = @area)
    return @ans
end


insert into [people]([full name], [gender], [birthdate], [city id])
values ('alik kohan', 'Male', '03/03/2002', dbo.cityidof('Bat Yam'))