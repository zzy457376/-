from flask import Flask, render_template
from routes.actors import actors_bp
from routes.companies import companies_bp
from routes.directors import directors_bp
from routes.genres import genres_bp
from routes.movies import movies_bp
from routes.roles import roles_bp         
from routes.narrations import narrations_bp

app = Flask(__name__)

app.register_blueprint(actors_bp, url_prefix='/actors')
app.register_blueprint(companies_bp, url_prefix='/companies')
app.register_blueprint(directors_bp, url_prefix='/directors')
app.register_blueprint(genres_bp, url_prefix='/genres')
app.register_blueprint(movies_bp, url_prefix='/movies')
app.register_blueprint(roles_bp, url_prefix='/roles')        
app.register_blueprint(narrations_bp, url_prefix='/narrations')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)




