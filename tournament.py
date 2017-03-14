#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
# all methods follow this template:
# 1) connect to the database
# 2) get a cursor
# 3) execute query
# 4) commit to database
# 5) close connection

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    # Query: delete from match;
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM match;")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    # Query: delete from player;
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM player;")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    # Query: select count(*) from player;
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT count(*) FROM player;")
    count = c.fetchone()
    return count[0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    # Query: insert into player(name) values (%s),(name,)
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO player(name) VALUES (%s);",(name,)) # avoids SQL injection
    conn.commit()
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    # Query: select * from standings; # standings is a VIEW
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM standings;")
    rows = c.fetchall() # get all rows as tuples
    conn.close()
    return rows

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # Query: ("insert into match (id1,id2,winner) values (%s,%s,%s)",(winner,loser,winner))
    # input validation
    if winner==loser:
        raise ValueError("winner and loser cannot be the same player")

    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO match VALUES (%s,%s,%s);",(winner,loser,winner)) # avoids SQL injection
    conn.commit()
    conn.close()
     
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    # get player standings
    standings = playerStandings()
    swissPairings = []

    # merge adjacent rows in standings
    for index,row in enumerate(standings):
        if index%2==0:
            # row[0] and row[1] has current player's id and name
            # standings[index+1] is the next ranked player
            pair = (row[0],row[1],standings[index+1][0],standings[index+1][1])
            swissPairings.append(pair)

    return swissPairings


