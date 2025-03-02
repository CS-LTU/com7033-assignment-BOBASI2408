# from main import app

# if __name__ == '__main__':
#     app.run(debug=True)

from main import create_app, db
from config import Config

# Create the app
app = create_app(Config)

# Create database tables
with app.app_context():
    db.create_all()
app.run(debug=True)
# Run the app if this file is executed directly
#if __name__ == '__main__':
#   app.run(debug=True)

