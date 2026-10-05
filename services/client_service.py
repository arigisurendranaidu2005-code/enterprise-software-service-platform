from typing import Dict, Optional, List
from core.models import Client
from core.config import settings

class ClientService:
    def __init__(self):
        self._clients: Dict[str, Client] = {}

    def register_client(self, client_id: str, company_name: str, industry_domain: str, contact_email: str) -> Client:
        if not client_id or not company_name:
            raise ValueError("client_id and company_name are mandatory")
        if client_id in self._clients:
            raise ValueError(f"Client with id {client_id} already exists")
        if industry_domain not in settings.SUPPORTED_DOMAINS:
            industry_domain = "Enterprise IT Services"

        client = Client(
            client_id=client_id,
            company_name=company_name,
            industry_domain=industry_domain,
            contact_email=contact_email
        )
        self._clients[client_id] = client
        return client

    def get_client(self, client_id: str) -> Optional[Client]:
        return self._clients.get(client_id)

    def list_clients(self) -> List[Client]:
        return list(self._clients.values())

    def update_status(self, client_id: str, new_status: str) -> Client:
        client = self.get_client(client_id)
        if not client:
            raise KeyError(f"Client {client_id} not found")
        client.status = new_status
        return client
