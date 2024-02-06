select f.origin_city as city
from flights as f
where f.canceled = 0
group by f.origin_city
having max(f.actual_time) < 240
order by f.origin_city asc;