select distinct c.name as carrier
from flights as f, carriers as c 
where f.origin_city = 'Seattle WA' and f.dest_city = 'New York NY' and f.carrier_id = c.cid
order by c.name asc;