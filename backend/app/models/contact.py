from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.models import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(120), nullable=False)
    last_name = Column(String(120), nullable=False)
    email = Column(String(150), index=True, nullable=True)
    phone = Column(String(50), nullable=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    hubspot_id = Column(String(255), nullable=True)
    source = Column(String(50), nullable=True)
    last_synced_at = Column(DateTime, nullable=True)

    company = relationship("Company", back_populates="contacts")
    activities = relationship("Activity", back_populates="contact")
    # Contact -> Deal relationship: a contact can have multiple deals
    deals = relationship("Deal", back_populates="contact")
