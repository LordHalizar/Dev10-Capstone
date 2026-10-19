set search_path to video_games;

-- genre queries
select * from genre order by genre_name;

select genre_name, count(*) from genre group by genre_name having count(*) > 1;

-- publisher queries
select * from publisher order by publisher_name;

select publisher_name, count(*) from publisher group by publisher_name having count(*) > 1;

-- game queries
select * from game;

select
	g.game_title,
	p.publisher_name
from game g
join publisher p on p.publisher_id = g.publisher_id
where game_title = 'Metal Slug X';

select game_title, count(*) from game group by game_title having count(*) > 1 order by game_title;

-- platform queries
select * from platform order by platform_name;

select game_id, platform_id, count(*) from game_platform group by game_id, platform_id having count(*) > 1;

-- game_platform queries
select * from game_platform;

select
	ga.game_title,
	pl.platform_name,
	ge.genre_name,
	ga.release_year
from game_platform gp
join game ga on ga.game_id = gp.game_id
join genre ge on ge.genre_id = ga.genre_id
join platform pl on pl.platform_id = gp.platform_id
group by ga.game_title, pl.platform_name, ge.genre_name, ga.release_year
order by ga.game_title, pl.platform_name;

-- sales queries
select * from sales;

show config_file;