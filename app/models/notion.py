from config.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey


# class Tree(Base):
#     __tablename__ = "trees"
#
#     id = Column(Integer, primary_key=True)
#     data = Column(String)
#     parent_id = Column(Integer, ForeignKey("trees.id"), nullable=True)
#
#     parent = relationship("Tree", remote_side=[id])