with 
	longDuration as 
	(select f1.origin_city, count(*) as cnt1
	from flights as f1
	where f1.canceled = 0
	group by f1.origin_city), 
	
	shortDuration as
	(select f2.origin_city, count(*) as cnt2
	from flights as f2
	where f2.canceled = 0 and f2.actual_time < 90
	group by f2.origin_city)

select longDuration.origin_city as origin_city, ISNULL(shortDuration.cnt2 * 100.0 / NULLIF(longDuration.cnt1, 0), 0) as percentage
from longDuration left join shortDuration on shortDuration.origin_city = longDuration.origin_city
order by percentage asc, longDuration.origin_city asc;