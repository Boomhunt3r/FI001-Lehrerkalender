from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, email, password, is_active):
        self.email = email
        self.password = password
        self.is_active = is_active
