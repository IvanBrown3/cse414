--(10 points) Find the maximum price of tickets between Seattle and New York, NY (i.e. Seattle to NY or NY to Seattle). 
--Show the maximum price for each airline separately.
--Name the output columns carrier and max_price, in that order.
--[Output relation cardinality: 3 rows]


select carrier_id as carrier, max(price) as max_price

from 
    flights as f

where 
    (f.origin_city = 'Seattle WA' or f.origin_city = 'New York NY') and 
    (f.dest_city = 'New York NY' or f.dest_city = 'Seattle WA') --wont be any flights that go seattle to seattle

group by
    f.carrier_id;

--output 3 rows 