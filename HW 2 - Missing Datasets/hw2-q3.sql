--(10 points) Find the day of the week with the longest average arrival delay. Return the name of the day and the average delay.
 --Name the output columns day_of_week and delay, in that order. (Hint: consider 　using LIMIT. Look up what it does!)
 --[Output relation cardinality: 1 row]

select 
    wd.day_of_week as day_of_week, avg(f.arrival_delay) as delay

from 
    flights as f, weekdays as wd

where 
    f.day_of_week_id = wd.did

group by 
    f.day_of_week_id

order by delay desc

limit 1;

--output 1 row