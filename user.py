import secrets

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(UserMixin, db.Model):
	"""User model backed by SQLAlchemy database.
	
	Compatible with flask-login and maps to the users table in PostgreSQL.
	"""
	__tablename__ = "users"
	
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255), unique=True, nullable=False)
	password = db.Column(db.String(255), nullable=False)
	password_salt = db.Column(db.String(255))
	otp = db.Column(db.String(255))
	otp_salt = db.Column(db.String(255))
	account_verified = db.Column(db.Boolean, nullable=False, default=False)

	def set_password(self, password: str) -> None:
		"""Hash and store the password with a per-user salt."""
		self.password_salt = secrets.token_hex(16)
		self.password = generate_password_hash(password + self.password_salt)

	def check_password(self, password: str) -> bool:
		"""Verify the provided password against the stored hash and salt."""
		if not self.password or not self.password_salt:
			return False
		return check_password_hash(self.password, password + self.password_salt)

	def is_active(self) -> bool:
		"""User is active if account is verified (used by flask-login)."""
		return bool(self.account_verified)

	def get_id(self) -> str:
		"""Return user ID as string (required by flask-login)."""
		return str(self.id)


def get_user(user_id: int) -> User | None:
	"""Retrieve a user by ID from the database."""
	return User.query.get(user_id)


def find_by_email(email: str) -> User | None:
	"""Find a user by email address."""
	return User.query.filter_by(email=email).first()


def create_user(email: str, password: str) -> User:
	"""Create a new user with email and password."""
	user = User(email=email, account_verified=False)
	user.set_password(password)
	db.session.add(user)
	db.session.commit()
	return user

