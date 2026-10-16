set search_path to video_games;

select * from genre;

select genre_name, count(*) from genre group by genre_name having count(*) > 1;

select * from publisher order by publisher_name;

select publisher_name, count(*) from publisher group by publisher_name having count(*) > 1;

select * from game order by game_title;

select game_title, count(*) from game group by game_title having count(*) > 1;

select * from platform order by platform_name;

select * from game_platform;

select * from sales;