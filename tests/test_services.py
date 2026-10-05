import unittest
from services.client_service import ClientService
from services.workflow_service import WorkflowService

class TestEnterpriseServices(unittest.TestCase):
    def setUp(self):
        self.client_svc = ClientService()
        self.workflow_svc = WorkflowService()

    def test_client_registration_and_lookup(self):
        client = self.client_svc.register_client(
            client_id="TEST-01",
            company_name="Apex Financials",
            industry_domain="Banking & Financial Services",
            contact_email="it@apexfin.com"
        )
        self.assertEqual(client.company_name, "Apex Financials")
        self.assertEqual(client.status, "ACTIVE")
        self.assertIsNotNone(self.client_svc.get_client("TEST-01"))

    def test_duplicate_client_rejection(self):
        self.client_svc.register_client("DUP-01", "Corp A", "Retail & Consumer Goods", "a@corp.com")
        with self.assertRaises(ValueError):
            self.client_svc.register_client("DUP-01", "Corp B", "Retail & Consumer Goods", "b@corp.com")

    def test_workflow_request_and_order_generation(self):
        req = self.workflow_svc.create_service_request("TEST-01", "Custom ERP Development", 150000.0)
        self.assertEqual(req.status, "PENDING")
        self.assertEqual(req.budget_estimate_inr, 150000.0)

        order = self.workflow_svc.approve_and_generate_order(req.request_id, allocated_hours=120, hourly_rate_inr=1000.0)
        self.assertEqual(order.total_cost_inr, 120000.0)
        self.assertEqual(order.status, "IN_PROGRESS")
        self.assertEqual(req.status, "APPROVED")

    def test_invalid_budget_validation(self):
        with self.assertRaises(ValueError):
            self.workflow_svc.create_service_request("TEST-01", "Mobile App", -500.0)

if __name__ == "__main__":
    unittest.main()
