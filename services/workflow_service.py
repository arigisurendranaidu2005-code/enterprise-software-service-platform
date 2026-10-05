import uuid
from typing import Dict, List, Optional
from core.models import ServiceRequest, WorkOrder

class WorkflowService:
    def __init__(self):
        self._requests: Dict[str, ServiceRequest] = {}
        self._work_orders: Dict[str, WorkOrder] = {}

    def create_service_request(self, client_id: str, service_type: str, budget_inr: float) -> ServiceRequest:
        if budget_inr <= 0:
            raise ValueError("Budget estimate must be positive")
        req_id = f"REQ-{uuid.uuid4().hex[:8].upper()}"
        req = ServiceRequest(
            request_id=req_id,
            client_id=client_id,
            service_type=service_type,
            budget_estimate_inr=budget_inr
        )
        self._requests[req_id] = req
        return req

    def approve_and_generate_order(self, request_id: str, allocated_hours: int, hourly_rate_inr: float = 1200.0) -> WorkOrder:
        req = self._requests.get(request_id)
        if not req:
            raise KeyError(f"Service request {request_id} not found")
        if allocated_hours <= 0:
            raise ValueError("Allocated hours must be greater than zero")

        total_cost = allocated_hours * hourly_rate_inr
        order_id = f"WO-{uuid.uuid4().hex[:8].upper()}"
        order = WorkOrder(
            order_id=order_id,
            request_id=request_id,
            client_id=req.client_id,
            allocated_hours=allocated_hours,
            hourly_rate_inr=hourly_rate_inr,
            total_cost_inr=total_cost
        )
        req.status = "APPROVED"
        self._work_orders[order_id] = order
        return order

    def get_work_order(self, order_id: str) -> Optional[WorkOrder]:
        return self._work_orders.get(order_id)
