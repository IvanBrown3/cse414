with SeattleOneStopFlights as (
select distinct f.dest_city as directCity
from flights as f
where f.origin_city = 'Seattle WA'),

interFlights as (
select distinct f2.dest_city as interCity
from flights as f1, flights as f2
where f1.origin_city = 'Seattle WA' and f1.dest_city = f2.origin_city and f2.dest_city <> f1.origin_city)


select distinct f3.dest_city as city
from flights as f3
where f3.dest_city not in (select interCity from interflights) and f3.dest_city not in (select directCity from SeattleOneStopFlights) and 
f3.dest_city <> 'Seattle WA'
order by f3.dest_city asc;