from sqlalchemy import Column, Text, TIMESTAMP, ForeignKey, String, Boolean
from sqlalchemy.sql import func
from .base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(Text, nullable=False, unique=True)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(Text, ForeignKey("roles.name", ondelete="CASCADE"))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, server_default="true")

    role_obj = relationship("Role", back_populates="users")
class Role(Base):
    __tablename__ = "roles"

    name = Column(Text, primary_key=True)
    description = Column(Text)

    users = relationship("User", back_populates="role_obj", cascade="all, delete")
    permissions = relationship("RolePermission", back_populates="role")
class RolePermission(Base):
    __tablename__ = "role_permissions"

    role_name = Column(Text, ForeignKey("roles.name", ondelete="CASCADE"), primary_key=True)
    permission_name = Column(Text, ForeignKey("permissions.name", ondelete="CASCADE"), primary_key=True)

    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", back_populates="roles")
class Permission(Base):
    __tablename__ = "permissions"

    name = Column(Text, primary_key=True)
    description = Column(Text)

    roles = relationship("RolePermission", back_populates="permission")