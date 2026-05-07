from typing import Dict
from pydantic import BaseModel


class AnalyticsOverview(BaseModel):
    deals_by_stage: Dict[str, int]
    revenue: float
    conversion_rate: float
    active_contacts: int
