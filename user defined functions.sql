create function cityidof (@name varchar(30))
returns int as
begin
    declare @ans int
	set @ans = (select [city id] from cities where [city name] = @name)
    return @ans
end

