select distinct c.name as carrier 
from carriers as c 
where c.cid in (select f.carrier_id from flights as f where f.origin_city = 'Seattle WA' and f.dest_city = 'New York NY')
order by c.name asc;