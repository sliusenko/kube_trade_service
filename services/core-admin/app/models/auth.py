from sqlalchemy import Column, Text, TIMESTAMP, ForeignKey, String
from sqlalchemy.sql import func
from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column("user_id", String, primary_key=True, index=True)
    username = Column(Text, nullable=False, unique=True)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(Text, ForeignKey("roles.name", ondelete="CASCADE"))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    password_hash = Column(String(255), nullable=False)


class Role(Base):
    __tablename__ = "roles"

    name = Column(Text, primary_key=True)
    description = Column(Text)


class Permission(Base):
    __tablename__ = "permissions"

    name = Column(Text, primary_key=True)
    description = Column(Text)


class RolePermission(Base):
    __tablename__ = "role_permissions"

    role_name = Column(Text, ForeignKey("roles.name", ondelete="CASCADE"), primary_key=True)
    permission_name = Column(Text, ForeignKey("permissions.name", ondelete="CASCADE"), primary_key=True)
