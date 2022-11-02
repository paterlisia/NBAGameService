import json
from games import Game


# test 1: get data entry by game_id
def query_by_gid():

    res = Game.get_by_key('202204100BRK')
    print(json.dumps(res, indent=2, default=str))


if __name__ == "__main__":
    print("\n\n Use test_rest.py instead of this file. \n\n")
    query_by_gid()
