-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- DROP existing tables and views
DROP TABLE IF EXISTS match CASCADE;
DROP TABLE IF EXISTS player CASCADE;

-- create a table 'player' with id and name
CREATE TABLE player (id SERIAL primary key,name TEXT);

-- create a table 'match' with 2 player ids and winner id
-- the IDs should exist in table 'match'
CREATE TABLE match (id1 INTEGER references player(id),
					id2 INTEGER references player(id),
					winner INTEGER);

-- create VIEW for Number of matches played by each player
-- join tables player and match with aggregation on match.id1 (i.e. distinct match.id1)
CREATE VIEW num_matches as select player.id,player.name,count(match.id1) as num from
        player left join match
        on (player.id=match.id1 or player.id=match.id2)
        group by (player.id) order by num desc;

-- create VIEW for Number of wins for each player
-- join tables player and match with aggregation based on winner id
CREATE VIEW num_wins as select player.id,player.name,count(winner) as wins from
        player left join match
        on player.id = winner
        group by (player.id) order by wins desc;

-- create VIEW for player standings
-- join VIEWs num_wins and num_matches based on highest number of wins
CREATE VIEW standings as select num_wins.id, num_wins.name, num_wins.wins, num_matches.num from num_wins,num_matches 
        where num_wins.id = num_matches.id order by num_wins.wins desc;