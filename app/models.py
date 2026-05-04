from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

class PlateCategory(Base):
    __tablename__ = "plate_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    hardness_range = Column(String)
    
    # Связь с пластинами
    plates = relationship("CuttingPlate", back_populates="category")

class CuttingPlate(Base):
    __tablename__ = "cutting_plates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    material = Column(String, nullable=False)
    coating = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    
    material_group = Column(String)
    max_depth_mm = Column(Float)
    recommended_speed_m_min = Column(Integer)
    
    category_id = Column(Integer, ForeignKey("plate_categories.id"))
    
    # Связи - добавлен lazy="joined" для автоматической загрузки
    category = relationship("PlateCategory", back_populates="plates", lazy="joined")