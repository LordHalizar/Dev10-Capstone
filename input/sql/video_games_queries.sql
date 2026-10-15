set search_path to video_games;

select * from genre;

select * from publisher order by publisher_name;

select * from game;

select game_title, count(*) from game group by game_title having count(*) > 1;

select * from platform order by platform_name;

select * from game_platform;

select * from sales;