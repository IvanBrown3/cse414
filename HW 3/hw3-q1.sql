select distinct f1.origin_city as origin_city, f1.dest_city as dest_city, f1.actual_time as time
from flights as f1
inner join (
    select origin_city, max(actual_time) as maxtime
    from flights
    group by origin_city
) as maxOriginCities
on f1.origin_city = maxOriginCities.origin_city and f1.actual_time = maxOriginCities.maxtime
order by f1.origin_city asc, f1.dest_city asc;