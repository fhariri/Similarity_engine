from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
import sqlite3

app = Flask(__name__)
api = Api(app)  # api is a collection of objects, where each object contains a specific functionality (GET, POST, etc)

'''
    A small api that takes two strings (pseudonym and real) and return the similarity score.
    Get simScores.db from score_matrix.csv using SQLite3:
    $ sqlite3 simScores.db
    sqlite> .mode csv simScores
    sqlite> .import score_matrix.csv simScores
    sqlite> .quit
    '''
class score(Resource):
    def get(self, name1, name2):
        conn = sqlite3.connect('simScores.db')
        c = conn.cursor()
        selection=c.execute('SELECT pseudo FROM simScores')
        result=selection.fetchall()
        pseudoList=[i[0] for i in result]
        # Find whether name1 or name2 are pseudonyms then extract the score
        if (name1 in pseudoList):
            command="SELECT  \""+name2+"\" FROM simScores WHERE pseudo= \""+name1+"\""
        else:
            command="SELECT  \""+name1+"\" FROM simScores WHERE pseudo= \""+name2+"\""
        score=c.execute(command)
        result=score.fetchall()
        return  {'score': [i[0] for i in result]}



class multiply(Resource):
    '''dummy function to test apis'''
    def get(self, number):  # param must match url identifier
        return number * 2

api.add_resource(multiply, '/multiply/<int:number>')  # whatever the number is, multiply by 2
api.add_resource(score, '/score/<string:name1>/<string:name2>')

if __name__ == '__main__':
    app.run(debug=True)
