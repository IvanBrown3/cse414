--(10 points) List the distinct flight numbers of all flights from Seattle to Boston by Alaska Airlines Inc. on Mondays. 
--Also notice that, in the database, the city names include the state. So Seattle appears as Seattle WA. 
--Please use the flight_num column instead of fid. Name the output column flight_num.
--[Hint: Output relation cardinality: 3 rows]

select distinct 
    f.flight_num as flight_num

from 
    flights as f

where 
    f.origin_city = 'Seattle WA' and 
    f.dest_city = 'Boston MA' and 
    f.day_of_week_id = 1 and 
    f.carrier_id = 'AS';

--output 3 rows 