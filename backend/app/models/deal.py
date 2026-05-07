from datetime import datetime

from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.models import Base


class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(220), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False, default=0)
    stage = Column(String(120), nullable=False, default="Lead")
    status = Column(String(50), nullable=False, default="Open")
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    hubspot_id = Column(String(255), nullable=True)
    source = Column(String(50), nullable=True)
    last_synced_at = Column(DateTime, nullable=True)

    # Link to Contact: a contact can have multiple deals, so use back_populates
    contact = relationship("Contact", back_populates="deals")
    company = relationship("Company", back_populates="deals")
    activities = relationship("Activity", back_populates="deal")
