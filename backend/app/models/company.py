from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.models import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    industry = Column(String(120), nullable=True)
    website = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    hubspot_id = Column(String(255), nullable=True)
    source = Column(String(50), nullable=True)
    last_synced_at = Column(DateTime, nullable=True)

    contacts = relationship("Contact", back_populates="company")
    deals = relationship("Deal", back_populates="company")
