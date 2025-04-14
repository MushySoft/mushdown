from sqlalchemy import Column, String, Boolean, Text, ForeignKey, DateTime, Table
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import expression
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Association tables
note_tag = Table(
    'note_tag',
    Base.metadata,
    Column('note_id', UUID(as_uuid=True), ForeignKey('note.id'), primary_key=True),
    Column('tag_id', UUID(as_uuid=True), ForeignKey('tag.id'), primary_key=True)
)

note_category = Table(
    'note_category',
    Base.metadata,
    Column('note_id', UUID(as_uuid=True), ForeignKey('note.id'), primary_key=True),
    Column('category_id', UUID(as_uuid=True), ForeignKey('category.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'user'
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    notes = relationship("Note", back_populates="user")
    tags = relationship("Tag", back_populates="user")
    categories = relationship("Category", back_populates="user")
    sync_logs = relationship("SyncLog", back_populates="user")

class Tag(Base):
    __tablename__ = 'tag'
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    name = Column(String(255), nullable=False)
    
    user = relationship("User", back_populates="tags")
    notes = relationship("Note", secondary=note_tag, back_populates="tags")

class Note(Base):
    __tablename__ = 'note'
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    is_archive = Column(Boolean, server_default=expression.false())
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates="notes")
    tags = relationship("Tag", secondary=note_tag, back_populates="notes")
    categories = relationship("Category", secondary=note_category, back_populates="notes")
    versions = relationship("NoteVersion", back_populates="note")
    sync_logs = relationship("SyncLog", back_populates="note")

class NoteVersion(Base):
    __tablename__ = 'note_version'
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    note_id = Column(UUID(as_uuid=True), ForeignKey('note.id'), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    note = relationship("Note", back_populates="versions")

class Category(Base):
    __tablename__ = 'category'
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    name = Column(String(255), nullable=False)
    
    user = relationship("User", back_populates="categories")
    notes = relationship("Note", secondary=note_category, back_populates="categories")

class SyncLog(Base):
    __tablename__ = 'sync_log'
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    note_id = Column(UUID(as_uuid=True), ForeignKey('note.id'), nullable=False)
    action = Column(String(50), nullable=False)
    timestamp = Column(DateTime, server_default=func.now())
    
    user = relationship("User", back_populates="sync_logs")
    note = relationship("Note", back_populates="sync_logs")

class OnlineEdit(Base):
    __tablename__ = 'online_chat'
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    note_id = Column(UUID(as_uuid=True), ForeignKey('note.id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    last_activity = Column(DateTime, server_default=func.now())
    
    note = relationship("Note")
    user = relationship("User")