from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, Table, Text, text
from sqlalchemy.dialects.mysql import TINYINT, TINYTEXT
from sqlalchemy.orm import relationship
from app import db

class User(db.Model):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True)
    email = Column(String(50, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    slug = Column(String(50, 'utf8mb4_unicode_ci'), nullable=False)
    registeredAt = Column(DateTime, nullable=False)
    firstName = Column(String(50, 'utf8mb4_unicode_ci'))
    lastName = Column(String(50, 'utf8mb4_unicode_ci'))
    lastLogin = Column(DateTime)
    avatarLink = Column(String(100, 'utf8mb4_unicode_ci'))
    intro = Column(TINYTEXT)

    post = relationship('Post', back_populates='user')
    post_ = relationship('Post', secondary='user_like_post', back_populates='user_')
    post_comment = relationship('PostComment', back_populates='user')


class Post(db.Model):
    __tablename__ = 'post'

    id = Column(BigInteger, primary_key=True)
    authorId = Column(ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    title = Column(String(75, 'utf8mb4_unicode_ci'), nullable=False)
    subtitle = Column(String(75, 'utf8mb4_unicode_ci'), nullable=False)
    slug = Column(String(100, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    summary = Column(TINYTEXT, nullable=False)
    published = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    createdAt = Column(DateTime, nullable=False)
    like = Column(Integer, nullable=False, server_default=text("'0'"))
    bannerLink = Column(String(100, 'utf8mb4_unicode_ci'))
    updatedAt = Column(DateTime)
    publishedAt = Column(DateTime)
    content = Column(Text(collation='utf8mb4_unicode_ci'))

    user = relationship('User', back_populates='post')
    user_ = relationship('User', secondary='user_like_post', back_populates='post_')
    post_comment = relationship('PostComment', back_populates='post')


class PostComment(db.Model):
    __tablename__ = 'post_comment'

    id = Column(BigInteger, primary_key=True)
    postId = Column(ForeignKey('post.id', ondelete='CASCADE'), nullable=False, index=True)
    authorId = Column(ForeignKey('user.id'), nullable=False, index=True)
    title = Column(String(100, 'utf8mb4_unicode_ci'), nullable=False)
    createdAt = Column(DateTime, nullable=False)
    parentId = Column(ForeignKey('post_comment.id', ondelete='CASCADE'), index=True)
    content = Column(Text(collation='utf8mb4_unicode_ci'))

    user = relationship('User', back_populates='post_comment')
    post_comment = relationship('PostComment', remote_side=[id], back_populates='post_comment_reverse')
    post_comment_reverse = relationship('PostComment', remote_side=[parentId], back_populates='post_comment')
    post = relationship('Post', back_populates='post_comment')


t_user_like_post = Table(
    'user_like_post', db.metadata,
    Column('userId', ForeignKey('user.id', ondelete='CASCADE'), primary_key=True, nullable=False),
    Column('postId', ForeignKey('post.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
)
