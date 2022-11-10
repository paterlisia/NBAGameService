import pymysql

import os
import json


class Game:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():
        user = os.environ.get("DBUSER")
        pwd = os.environ.get("DBPWD")
        host = os.environ.get("DBHOST")
        conn = pymysql.connect(
            user="root",
            password="dbuserdbuser",
            host="cc6156.cthaaibiwku7.us-east-2.rds.amazonaws.com",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    # get the game date type by date
    @staticmethod
    def get_by_date(key):
        sql_connect = "use game;"
        sql_games = """
                        select * from ((select distinct game_id, Team_Abbrev, Team_Score, Opponent_Score, Opponent_Abbrev, Team_Loc as location
                            from (nba_game join nba_team on nba_team.Team_ID = substr(game_id, 10))
                            where substr(game_id, 1, 8) =  %s
                            ) as t1 join (select Team_ID, Team_Logo from nba_team) as t2 on t1.Team_Abbrev=t2.Team_ID);"""
        sql_mvp = """select game_id, player, max(pts) as pts, team from
                    (select game_id, player, pts, Team_Abbrev as team from nba_game where substr(game_id, 1, 8) =  %s and Team_Abbrev = substr(game_id, 10)
                    union
                    select game_id, player, pts, Team_Abbrev as team from nba_game where substr(game_id, 1, 8) =  %s and Opponent_Abbrev = substr(game_id, 10)) as stats group by team;"""
        
        conn = Game._get_connection()
        cur = conn.cursor()
        cur.execute(sql_connect)
        cur.execute(sql_games, args=key)
        result_games = cur.fetchall()
        cur.execute(sql_mvp, args=[key, key])
        result_mvp = cur.fetchall()
        result = {}
        # format query result and combine
        # step1: get games details for each team
        for game in result_games:
            game_id = game["game_id"]
            # create a new game object by game_id if not created
            if game_id not in result:
                result[game_id] = {}
            # create a new team object list by game_id if not created
            if "teams" not in result[game_id]:
                # print("create")
                result[game_id]["teams"] = []

            # fill data in the team object
            team_object = {}
            team_object["name"] = game["Team_Abbrev"]
            team_object["score"] = game["Team_Score"]
            team_object["logo"] = game["Team_Logo"]

            result[game_id]["teams"].append(team_object)

            result[game_id]["place"] = game["location"]
        
        # step2: get mvp for each team
        for player in result_mvp:
            game_id = player["game_id"]
            for team in result[game_id]["teams"]:
                if player["team"] == team["name"]:
                    team["mvp"] = {}
                    team["mvp"]["name"] = player["player"]
                    team["mvp"]["pts"] = player["pts"]

        return result

