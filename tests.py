import unittest

from server import app
from model import db, connect_to_db


class EventsTests(unittest.TestCase):
    """Tests for my events site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn(b"Welcome", result.data)

    # def test_events_most_commented(self):
    #     #test events most commented show on the homepage
    #     result = self.client.get("/")
    #     self.assertIn(b"2400 3rd Ave S, Minneapolis, MN 55404", result.data)
    #     # self.assertNotIn(b"Zoo", result.data)

    # def test_log_in(self):
    #     result = self.client.post("/handle-login",
    #                               data={"email": "user1@test.com",
    #                                     "password": "test"},
    #                               follow_redirects=True)
    #     # FIXME: Once we sign up, we should see the homepage and our name at the top.
    #     self.assertIn(b"Maria", result.data)
    #     self.assertNotIn(b"log in", result.data)        

       


if __name__ == "__main__":
    unittest.main()
