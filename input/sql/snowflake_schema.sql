use role sysadmin;
use database demo_db;
create schema if not exists video_games;
use schema video_games;

create or replace table genre (
	genre_id int autoincrement primary key,
	genre_name varchar(100) not null unique
);

create or replace table publisher (
	publisher_id int autoincrement primary key,
	publisher_name varchar(150) not null unique
);

create or replace table game (
	game_id int autoincrement primary key,
	game_title varchar(250) not null unique
);

create or replace table game_genre (
	game_id int not null,
	genre_id int not null,
	foreign key(game_id)
		references game(game_id),
	foreign key(genre_id)
		references genre(genre_id),
	
	constraint uq_game_genre
		unique (game_id, genre_id)
);

create or replace table game_publisher (
	game_id int not null,
	publisher_id int not null,
	foreign key(game_id)
		references game(game_id),
	foreign key(publisher_id)
		references publisher(publisher_id),
		
	constraint uq_game_publisher
		unique (game_id, publisher_id)
);

create or replace table platform (
	platform_id int autoincrement primary key,
	platform_name varchar(75) not null unique
);

create or replace table game_platform (
	game_platform_id int autoincrement primary key,
	game_id int not null,
	platform_id int not null,
	foreign key(game_id)
		references game(game_id),
	foreign key(platform_id)
		references platform(platform_id),
		
	constraint uq_game_platform
		unique (game_id, platform_id)
);

create or replace table game_platform_release (
	game_platform_release_id int autoincrement primary key,
	game_platform_id int not null,
	release_year int not null,
	foreign key(game_platform_id)
		references game_platform(game_platform_id),
		
	constraint uq_game_platform_release
		unique (game_platform_id, release_year)
);

create or replace table sales (
	sales_id int autoincrement primary key,
	game_platform_release_id int not null,
	na_sales numeric(6,2) not null,
	jp_sales numeric(6,2) not null,
	foreign key(game_platform_release_id)
		references game_platform_release(game_platform_release_id)
);