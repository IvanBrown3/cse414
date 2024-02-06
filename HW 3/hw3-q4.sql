with SeattleDirectDestinations as (
    select distinct dest_city
    from flights
    where origin_city = 'Seattle WA'
),
SeattleToIntermediate as (
    select distinct f1.dest_city as intermediate_city
    from flights as f1
    where f1.origin_city = 'Seattle WA'
),
IntermediateToDestinations as (
    select distinct f2.dest_city as final_dest
    from flights as f2
    where f2.origin_city in (select intermediate_city from SeattleToIntermediate)
)

select final_dest as city
from IntermediateToDestinations
where final_dest not in (select dest_city from SeattleDirectDestinations)
and final_dest != 'Seattle WA'
order by final_dest asc;