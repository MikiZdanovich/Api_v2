from .. import db


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "git_repositories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list_repositories = db.Column(db.String())
    requested_on = db.Column(db.DateTime)
    username = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return "<User '{}', was requested on {}>".format(self.username, self.requested_on)
