from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class Client:
    client_id: str
    company_name: str
    industry_domain: str
    contact_email: str
    status: str = "ACTIVE"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

@dataclass
class ServiceRequest:
    request_id: str
    client_id: str
    service_type: str # Software Development, Cloud Migration, ERP, Digital Transformation
    budget_estimate_inr: float
    status: str = "PENDING"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

@dataclass
class WorkOrder:
    order_id: str
    request_id: str
    client_id: str
    allocated_hours: int
    hourly_rate_inr: float
    total_cost_inr: float
    status: str = "IN_PROGRESS"
