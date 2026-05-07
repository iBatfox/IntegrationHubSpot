from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.models import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(120), nullable=False)
    payload = Column(Text, nullable=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    deal_id = Column(Integer, ForeignKey("deals.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    contact = relationship("Contact", back_populates="activities")
    # Activity -> Deal relationship: ensure back_populates matches Deal.activities
    deal = relationship("Deal", back_populates="activities")
