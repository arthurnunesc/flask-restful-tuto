from flask import Flask, request
from flask_restful import Resource, Api
from pony import orm

app = Flask(__name__)
api = Api(app)
db = orm.Database()


class Game(db.Entity):
    """Defines the database schema, which is a table called Game(entity in PonyORM)"""

    game_id = orm.Required(str, unique=True)
    home_team = orm.Required(str)
    away_team = orm.Required(str)
    home_score = orm.Required(int)
    away_score = orm.Required(int)


# Creates the SQLIte database and if the table doesn't exist, it creates it
db.bind(provider="sqlite", filename="database.sqlite", create_db=True)
db.generate_mapping(create_tables=True)

# API endpoints
class GameList(Resource):
    """API associated with the / endpoint"""

    def get(self):
        """Returns a list of all games in JSON format"""
        with orm.db_session:
            games = orm.select(p for p in Game)
            result = [i.to_dict() for i in games]

        return {"games": result}

    def post(self):
        """Adds a new game to the database"""
        new_game = request.json
        try:
            with orm.db_session:
                Game(
                    game_id=new_game["game_id"],
                    home_team=new_game["home_team"],
                    away_team=new_game["away_team"],
                    home_score=new_game["home_score"],
                    away_score=new_game["away_score"],
                )

            return {"game": new_game}
        except orm.TransactionIntegrityError as err:
            print(err)
            return {"error": "Game ID already exists"}


class GameDetail(Resource):
    """Endpoint to get a single game info by ID"""

    def get(self, game_id):
        try:
            with orm.db_session:
                item = Game.get(game_id=game_id)

            return {"game": item.to_dict()}
        except:
            return {"error": "Game does not exist"}


api.add_resource(GameList, "/")
api.add_resource(GameDetail, "/<string:game_id>")

if __name__ == "__main__":
    app.run(debug=True, port="5555")
