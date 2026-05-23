from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import uuid


class User(UserMixin):
	"""Lightweight User class compatible with flask-login.

	This is a simple in-memory focused implementation intended for small
	projects or as an example. For production use, back this with a database
	(SQLAlchemy, etc.) and adapt the helpers below.
	"""

	def __init__(self, id=None, username=None, email=None, password_hash=None, active=True):
		self.id = id or str(uuid.uuid4())
		self.username = username
		self.email = email
		self.password_hash = password_hash
		self.active = active

	def set_password(self, password: str) -> None:
		self.password_hash = generate_password_hash(password)

	def check_password(self, password: str) -> bool:
		if not self.password_hash:
			return False
		return check_password_hash(self.password_hash, password)

	def is_active(self) -> bool:  # used by flask-login
		return bool(self.active)

	def get_id(self) -> str:
		return str(self.id)


# --- Tiny in-memory store & helpers (example usage) ---
_USERS = {}


def add_user(user: User) -> User:
	_USERS[user.get_id()] = user
	return user


def get_user(user_id: str):
	return _USERS.get(str(user_id))


def find_by_username(username: str):
	for u in _USERS.values():
		if u.username == username:
			return u
	return None


def create_user(username: str, email: str, password: str) -> User:
	u = User(username=username, email=email)
	u.set_password(password)
	add_user(u)
	return u
