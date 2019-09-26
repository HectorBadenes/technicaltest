"""
REST technical test

@Autor:  - Hector Badenes Tur
@Date:   26/09/2019
@Version 1.0

@Python_version = 3.6.8
"""

from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
import mysql.connector

app = Flask(__name__)
api = Api(app)

""" Get the list of suggested names that match the characters the user have typed so far.

\param   (String) query       Characters the user have typed so far.
\param   (String) species     Name of the target species.
\param   (String) limit       Maximum number of suggestions to return.

\returns (List)               List of suggestions.
"""
def getSuggestions(query, species, limit):
    

    sql = "SELECT display_label FROM gene_autocomplete WHERE display_label LIKE '{0}%' AND species = '{1}' LIMIT {2}"

    mydb = mysql.connector.connect(
        host="ensembldb.ensembl.org",
        user="anonymous",
        database="ensembl_website_97"
    )

    mycursor = mydb.cursor()
    mycursor.execute(sql.format(query, species, limit))
    
    return mycursor.fetchall()


""" Class used as a model of the endpoint 'gene_suggest'
"""
class Suggestions(Resource):

    """ Get a list of suggetions in json fomat.

        \param   (Object) self      Instance of the class.

        \returns (json)             List of suggetions in json fomat.         
    """
    def get(self):

        query = request.args.get('q', default = "", type = str)
        species = request.args.get('species', default = "", type = str)
        limit = request.args.get('limit', default = "10", type = str)

        sugestions = getSuggestions(query, species, limit)
        
        return { "data": [i[0] for i in sugestions] }



api.add_resource(Suggestions, "/gene_suggest") # Registers the path to the resource 'Suggestions'


if __name__ == "__main__":

    app.run(port='5002') # Run the api in the port 5002.

