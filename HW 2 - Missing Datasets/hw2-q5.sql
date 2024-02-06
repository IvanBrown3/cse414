--(10 points) Find all airlines that had more than 0.5% (= 0.005) of their flights out of Seattle canceled. 
--Return the name of the airline and the percentage of canceled flights out of Seattle. 
--Percentages should be outputted in percent format (3.5% as 3.5 not 0.035). 
--Order the results by the percentage of canceled flights in ascending order.
--Name the output columns name and percentage, in that order.
--[Output relation cardinality: 6 rows]


select 
    c.name, (avg(f.canceled) * 100) as percentage

from
    flights as f, carriers as c
where
    f.origin_city = 'Seattle WA' and f.carrier_id = c.cid

group by
    c.name

having 
    percentage  > 0.5

order by
    percentage asc;


--output 6 rows