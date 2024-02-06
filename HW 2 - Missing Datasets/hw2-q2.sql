--(10 points) Find all itineraries from Seattle to Boston on July 15th. Search only for itineraries that have one stop 
--(i.e., flight 1: Seattle -> [somewhere], flight2: [somewhere] -> Boston). 
--Both flights must depart on the same day (same day here means the date of flight) and must be with the same carrier. 
--It's fine if the landing date is different from the departing date (i.e., in the case of an overnight flight). 
--You don't need to check whether the first flight overlaps with the second one since the departing and 
--arriving time of the flights are not provided.
--The total flight time (actual_time) of the entire itinerary should be fewer than 7 hours (but notice that actual_time is in minutes). 
--For each itinerary, the query should return the name of the carrier, the first flight number, 
--the origin and destination of that first flight, the flight time, the second flight number, 
--the origin and destination of the second flight, the second flight time, and finally the total flight time. 
--Only count flight times here; do not include any layover time.

select 
    c.name, f1.flight_num, f1.origin_city, f1.dest_city, f1.actual_time, f2.flight_num, f2.origin_city, f2.dest_city, f2.actual_time, (f2.actual_time + f1.actual_time ) as totaltime
    
from 
    flights as f1, flights as f2, carriers as c
where 
    f1.month_id = 7 and f1.day_of_month = 15 and f1.carrier_id = f2.carrier_id and
    f1.origin_city = 'Seattle WA' and f2.dest_city = 'Boston MA' and f1.carrier_id = c.cid and 
    f1.dest_city = f2.origin_city and f1.month_id = f2.month_id and f1.day_of_month = f2.day_of_month and totaltime < 420;


--output 1472 rows