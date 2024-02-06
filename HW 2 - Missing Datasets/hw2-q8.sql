--(10 points) Compute the total departure delay of each airline across all flights. 
--Some departure delays may be negative (indicating an early departure); 
--they should reduce the total, so you don't need to handle them specially. 
--Name the output columns name and delay, in that order. [Output relation cardinality: 22 rows]

select 
    c.name, sum(f.departure_delay) as delay

from 
    flights as f, carriers as c

where 
    f.carrier_id = c.cid

group by 
    f.carrier_id;


--output 22 rows