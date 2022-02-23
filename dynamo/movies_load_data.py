from decimal import Decimal
import json
import boto3

table_name = 'mvdb-dev'
table_data = 'moviedata.json'

def load_movies(movies, dynamodb=None):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table(table_name)
    for movie in movies:
        year = int(movie['year'])
        title = movie['title']
        print("Adding movie:", year, title)
        table.put_item(Item=movie)


if __name__ == '__main__':
    with open(table_data) as json_file:
        movie_list = json.load(json_file, parse_float=Decimal)
    load_movies(movie_list)
