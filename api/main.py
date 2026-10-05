from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from core.config import settings
from services.client_service import ClientService
from services.workflow_service import WorkflowService

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise Software Development, Client Lifecycle & Workflow Management API for IT Services"
)

client_service = ClientService()
workflow_service = WorkflowService()

# Seed baseline enterprise clients (Banking, Healthcare, Retail)
client_service.register_client("CL-001", "HDFC Banking Corp", "Banking & Financial Services", "contact@hdfcbank.com")
client_service.register_client("CL-002", "Apollo Care Systems", "Healthcare & Life Sciences", "it@apollocare.org")
client_service.register_client("CL-003", "Pie Global Retail", "Retail & Consumer Goods", "dev@pieretail.com")

class ClientCreateDTO(BaseModel):
    client_id: str
    company_name: str
    industry_domain: str
    contact_email: EmailStr

class ServiceRequestCreateDTO(BaseModel):
    client_id: str
    service_type: str
    budget_estimate_inr: float

class WorkOrderCreateDTO(BaseModel):
    request_id: str
    allocated_hours: int
    hourly_rate_inr: Optional[float] = 1200.0

@app.get("/", tags=["Health Check"])
def root():
    return {
        "status": "ONLINE",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs"
    }

@app.post("/api/v1/clients", status_code=status.HTTP_201_CREATED, tags=["Clients"])
def create_client(dto: ClientCreateDTO):
    try:
        c = client_service.register_client(dto.client_id, dto.company_name, dto.industry_domain, dto.contact_email)
        return c.__dict__
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/clients", tags=["Clients"])
def list_clients():
    return [c.__dict__ for c in client_service.list_clients()]

@app.post("/api/v1/requests", status_code=status.HTTP_201_CREATED, tags=["Workflows"])
def create_request(dto: ServiceRequestCreateDTO):
    if not client_service.get_client(dto.client_id):
        raise HTTPException(status_code=404, detail=f"Client {dto.client_id} does not exist")
    try:
        req = workflow_service.create_service_request(dto.client_id, dto.service_type, dto.budget_estimate_inr)
        return req.__dict__
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/orders", status_code=status.HTTP_201_CREATED, tags=["Workflows"])
def generate_order(dto: WorkOrderCreateDTO):
    try:
        order = workflow_service.approve_and_generate_order(dto.request_id, dto.allocated_hours, dto.hourly_rate_inr)
        return order.__dict__
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))
