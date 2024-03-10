import sqlalchemy

def double_double_counter(player_name):
    update_dd_query = sqlalchemy.text(
            f"""UPDATE players.`{player_name}`
            SET DD = CASE
                WHEN (
                    (PTS >= 10) +
                    (REB >= 10) +
                    (AST >= 10) +
                    (STL >= 10) +
                    (BLK >= 10)
                ) >= 2 THEN 1
                ELSE 0
            END;"""
        )
    return update_dd_query


def triple_double_counter(player_name):
    update_td_query = sqlalchemy.text(
            f"""UPDATE players.`{player_name}`
            SET TD = CASE
                WHEN (
                    (PTS >= 10) +
                    (REB >= 10) +
                    (AST >= 10) +
                    (STL >= 10) +
                    (BLK >= 10)
                ) >= 3 THEN 1
                ELSE 0
            END;"""
        )
    return update_td_query

def fantasypts_counter(player_name):
    update_fantasypts_query = sqlalchemy.text(
            f"""UPDATE players.`{player_name}`
            SET FAN_PTS = 
                (PTS + 
                (REB * 1.2) + 
                (AST * 1.5) + 
                (BLK * 3) + 
                (STL * 3) + 
                (TOV * (-2)) + 
                FG3M + 
                DD + 
                TD);"""
        )
    return update_fantasypts_query

def get_all_players():
    get_players = sqlalchemy.text(
        f"SELECT id, full_name FROM players_index"
    )
    return get_players


def get_player_info(player_name):
    player_info = sqlalchemy.text(
        f"""SELECT
            CONCAT(GAME_DATE, ' ', MATCHUP) AS MATCHUP_DATE, FAN_PTS, MIN
            FROM players.`{player_name}`;"""
    )
    return player_info

def alter_table(player_name, column_name, column_type):
    alter = sqlalchemy.text(
        f"""ALTER TABLE players.`{player_name}`
        ADD {column_name} {column_type} DEFAULT 0"""
    )
    return alter
