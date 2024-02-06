--(10 points) Find the names of all airlines that ever flew more than 1000 flights in one day 
--(i.e., a specific day/month, but not any 24-hour period). Return only the names of the airlines. 
--Do not return any duplicates (i.e., airlines with the exact same name).
--Name the output column name.
--[Output relation cardinality: 12 rows]

select distinct --have to use distinct cuz there is multiple times when a airline had more than 1000 flights in one day
    c.name as name

from 
    flights as f1, carriers as c 

where
    f1.carrier_id = c.cid

group by c.name, f1.month_id, f1.day_of_month -- groups by name and any given day, which is why a self join with flights is not needed

having 
    count(c.name) > 1000; -- count the instances where a flight occured and filter after groupby to allow only names with more than 1000 flights


-- output 12 rows








