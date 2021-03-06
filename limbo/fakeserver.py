from slackrtm.server import User, Bot

class FakeServer(object):
    def __init__(self, slack=None, config=None, hooks=None, db=None):
        self.slack = slack or FakeSlack()
        self.config = config
        self.hooks = hooks
        self.db = db

    def query(self, sql, *params):
        if not self.db:
            return None

        c = self.db.cursor()
        c.execute(sql, params)
        rows = c.fetchall()
        c.close()
        self.db.commit()
        return rows

class FakeSlack(object):
    def __init__(self, server=None, users=None, events=None):
        self.server = server or FakeSlackServer(users=users)
        self.posted_message = None
        self.events = events if events else []

    def post_message(self, channel, message, **kwargs):
        self.posted_message = (message, kwargs)

    def rtm_read(self):
        return self.events.pop() if self.events else []

class FakeSlackServer(object):
    def __init__(self, botname="limbo_test", users=None, bots=None, events=None):
        self.login_data = {
            "self": {
                "name": botname,
            }
        }
        self.username = "replbot"

        self.users = users if users else {
            "1": User(self, "limbo_test", 1, "", 0),
            "2": User(self, "msguser", 2, "", 0),
            "3": User(self, "slackbot", 3, "", 0),
        }

        self.bots = bots if bots else {
            "1": Bot("1", "otherbot", [], False)
        }

