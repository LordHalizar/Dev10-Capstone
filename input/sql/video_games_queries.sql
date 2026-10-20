set search_path to video_games;

-- genre queries

select * from genre order by genre_name;

select genre_name, count(*) from genre group by genre_name having count(*) > 1;

-- publisher queries

select * from publisher order by publisher_name;

select publisher_name, count(*) from publisher group by publisher_name having count(*) > 1;

-- game queries

select * from game;

select game_title, count(*) from game group by game_title having count(*) > 1 order by game_title;

-- platform queries

select * from platform order by platform_name;

-- game genre queries

select * from game_genre;

-- game platform queries

select * from game_platform;

-- game publisher queries

select * from game_publisher;

-- game platform release queries

select * from game_platform_release;

-- sales queries

select * from sales;

select
	ga.game_title,
	gaplr.release_year,
	string_agg(distinct ge.genre_name, ', ') as genres,
	string_agg(distinct pu.publisher_name, ', ') as publishers,
	pl.platform_name,
	s.na_sales,
	s.jp_sales
from game_platform_release gaplr
join game_platform gapl on gapl.game_platform_id = gaplr.game_platform_id
join game ga on ga.game_id = gapl.game_id
join game_genre gage on gage.game_id = ga.game_id
join game_publisher gapu on gapu.game_id = ga.game_id
join genre ge on ge.genre_id = gage.genre_id
join platform pl on pl.platform_id = gapl.platform_id
join publisher pu on pu.publisher_id = gapu.publisher_id
join sales s on s.game_platform_release_id = gaplr.game_platform_release_id
group by 
	ga.game_title,
	gaplr.release_year,
	pl.platform_name,
	s.na_sales,
	s.jp_sales
order by gaplr.release_year, ga.game_title, pl.platform_name;

select
	ga.game_title,
	gaplr.release_year,
	string_agg(distinct ge.genre_name, ', ') as genres,
	string_agg(distinct pu.publisher_name, ', ') as publishers,
	pl.platform_name,
	s.na_sales,
	s.jp_sales
from game_platform_release gaplr
join game_platform gapl on gapl.game_platform_id = gaplr.game_platform_id
join game ga on ga.game_id = gapl.game_id
join game_genre gage on gage.game_id = ga.game_id
join game_publisher gapu on gapu.game_id = ga.game_id
join genre ge on ge.genre_id = gage.genre_id
join platform pl on pl.platform_id = gapl.platform_id
join publisher pu on pu.publisher_id = gapu.publisher_id
join sales s on s.game_platform_release_id = gaplr.game_platform_release_id
where ga.game_title like '%sales)'
group by 
	ga.game_title,
	gaplr.release_year,
	pl.platform_name,
	s.na_sales,
	s.jp_sales
order by ga.game_title, pl.platform_name;

with multi_year_titles as (
    select
        ga.game_title,
        pl.platform_name
    from game_platform_release gaplr
    join game_platform gapl on gapl.game_platform_id = gaplr.game_platform_id
    join game ga on ga.game_id = gapl.game_id
    join platform pl on pl.platform_id = gapl.platform_id
    group by ga.game_title, pl.platform_name
    having count(distinct gaplr.release_year) > 1
)
select
    ga.game_title,
    gaplr.release_year,
    string_agg(distinct ge.genre_name, ', ') as genres,
    string_agg(distinct pu.publisher_name, ', ') as publishers,
    pl.platform_name,
    s.na_sales,
    s.jp_sales
from game_platform_release gaplr
join game_platform gapl on gapl.game_platform_id = gaplr.game_platform_id
join game ga on ga.game_id = gapl.game_id
join game_genre gage on gage.game_id = ga.game_id
join game_publisher gapu on gapu.game_id = ga.game_id
join genre ge on ge.genre_id = gage.genre_id
join platform pl on pl.platform_id = gapl.platform_id
join publisher pu on pu.publisher_id = gapu.publisher_id
join sales s on s.game_platform_release_id = gaplr.game_platform_release_id
join multi_year_titles my
    on my.game_title = ga.game_title
   and my.platform_name = pl.platform_name
group by
    ga.game_title,
    gaplr.release_year,
    pl.platform_name,
    s.na_sales,
    s.jp_sales
order by ga.game_title, pl.platform_name, gaplr.release_year;

show config_file;