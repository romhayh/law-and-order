create function cityidof (@name varchar(30))
returns int as
begin
    declare @ans int
	set @ans = (select [city id] from cities where [city name] = @name)
    return @ans
end;
go

create function specializationidof (@area varchar(30))
returns int as
begin
    declare @ans int
	set @ans = (select s.[area] from specializations s where [area] = @area)
    return @ans
end
