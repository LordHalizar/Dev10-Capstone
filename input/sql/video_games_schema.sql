drop schema if exists video_games cascade;
create schema video_games;
set search_path to video_games;

create table genre (
	genre_id serial primary key,
	genre_name varchar(100) not null unique
);

create table publisher (
	publisher_id serial primary key,
	publisher_name varchar(150) not null unique
);

create table game (
	game_id serial primary key,
	game_title varchar(250) not null unique
);

create table game_genre (
	game_id int not null,
	genre_id int not null,
	foreign key(game_id)
		references game(game_id),
	foreign key(genre_id)
		references genre(genre_id),
	
	constraint uq_game_genre
		unique (game_id, genre_id)
);

create table game_publisher (
	game_id int not null,
	publisher_id int not null,
	foreign key(game_id)
		references game(game_id),
	foreign key(publisher_id)
		references publisher(publisher_id),
		
	constraint uq_game_publisher
		unique (game_id, publisher_id)
);

create table platform (
	platform_id serial primary key,
	platform_name varchar(75) not null unique
);

create table game_platform (
	game_platform_id serial primary key,
	game_id int not null,
	platform_id int not null,
	foreign key(game_id)
		references game(game_id),
	foreign key(platform_id)
		references platform(platform_id),
		
	constraint uq_game_platform
		unique (game_id, platform_id)
);

create table game_platform_release (
	game_platform_release_id serial primary key,
	game_platform_id int not null,
	release_year int not null,
	foreign key(game_platform_id)
		references game_platform(game_platform_id),
		
	constraint uq_game_platform_release
		unique (game_platform_id, release_year)
);

create table sales (
	sales_id serial primary key,
	game_platform_release_id int not null,
	na_sales numeric(6,2) not null,
	jp_sales numeric(6,2) not null,
	foreign key(game_platform_release_id)
		references game_platform_release(game_platform_release_id)
);