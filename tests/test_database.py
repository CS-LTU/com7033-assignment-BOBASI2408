
import unittest
import mongomock
from main import create_app, db
from config import Config
from sqlalchemy import text  # added import

class TestDatabases(unittest.TestCase):
    def setUp(self):
        self.app = create_app(Config)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        # Set up test databases
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        
        # Mock MongoDB client
        self.mongo_mock = mongomock.MongoClient()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_sqlite_connection(self):
        with self.app.app_context():
            try:
                db.session.execute(text('SELECT 1'))  # wrapped SQL string with text()
                self.assertTrue(True)
            except Exception as e:
                self.fail(f"SQLite connection failed: {str(e)}")

    def test_mongodb_connection(self):
        db = self.mongo_mock.db
        collection = db.test_collection
        test_doc = {"name": "Test"}
        result = collection.insert_one(test_doc)
        self.assertTrue(result.inserted_id)

if __name__ == '__main__':
    unittest.main()