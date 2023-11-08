from app import app
from app.models import db
from app.routes import main_bp


app.register_blueprint(main_bp)
#print(app.url_map)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)