from flask import Flask
from heroes_route import heroes_route


__author__ = 'Jonarzz'

ERROR_400 = 'Your request is invalid. If there was a number in your query, try integer instead of floating point.'
ERROR_404 = 'No results matching your query were found.'

app = Flask(__name__)

app.config['DEBUG'] = True
app.config["JSON_SORT_KEYS"] = False

app.register_blueprint(heroes_route)
# appcfg.py -A dota-2-restful-api update app.yaml

@app.route('/v1')
def main():
    return 'Dota 2 RESTful API'


@app.errorhandler(404)
def page_not_found(e):
    return ERROR_404, 404


@app.errorhandler(400)
def page_not_found(e):
    return ERROR_400, 400


if __name__ == '__main__':
    app.run(debug=True)
