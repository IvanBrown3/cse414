--(10 points) Find the total capacity of all direct flights that fly between Seattle and San Francisco, CA on July 10th 
--(i.e. Seattle to SF or SF to Seattle).
--Name the output column capacity.
--[Output relation cardinality: 1 row]

select sum(capacity) as capacity

from flights as f

where 
    (f.origin_city = 'Seattle WA' or f.origin_city = 'San Francisco CA') and 
    (f.dest_city = 'San Francisco' or f.dest_city = 'Seattle WA') and
    f.month_id = 7 and f.day_of_month = 10;

--output 1 row
