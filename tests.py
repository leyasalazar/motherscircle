from unittest import TestCase

from server import app
from model import connect_to_db, db, example_data
from flask import session

class EventsTests(TestCase):
    """Tests for my events site."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True


    # def test_homepage(self):
    #     result = self.client.get("/")
    #     self.assertIn(b"Welcome", result.data)

    
    def test_index(self):
        result = self.client.get('/')
        self.assertIn(b"<h1 class='display-3 logo'>MOTHERS' CIRCLE</h1>", result.data)

    def test_signup(self):
        result = self.client.get('/signup')
        self.assertIn(b"<h2 class='mb-1'>Create an account</h2>", result.data)

    # def test_log_in(self):
    #     result = self.client.post("/handle-login",
    #                               data={"email": "user1@test.com",
    #                                     "password": "test"},
    #                               follow_redirects=True)
    #     # FIXME: Once we sign up, we should see the homepage and our name at the top.
    #     self.assertIn(b"Find a community for you and your kids", result.data)
    #     # self.assertNotIn(b"<div id='emailHelp' class='form-text'>We'll never share your email with anyone else.</div>", result.data)        

class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()
    
    def test_login(self):
        """Test login page."""

        result = self.client.post("/handle-login",
                                  data={"email": "rachel@test.com", "password": "123"},
                                  follow_redirects=True)
        self.assertIn(b"Mother's Circle", result.data)

    # def test_departments_list(self):
    #     """Test departments page."""

    #     result = self.client.get("/departments")
    #     self.assertIn(b"Legal", result.data)

    def test_event_details(self):
        """Test event page."""

        result = self.client.get("/events/1")
        self.assertIn(b"zoo", result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()
