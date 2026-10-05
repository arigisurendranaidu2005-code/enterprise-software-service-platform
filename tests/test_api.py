import unittest
from services.client_service import ClientService
from services.workflow_service import WorkflowService

class TestAPIComponents(unittest.TestCase):
    def test_domain_fallback(self):
        svc = ClientService()
        c = svc.register_client("UN-01", "Unknown Org", "Custom Hardware", "test@test.com")
        self.assertEqual(c.industry_domain, "Enterprise IT Services")

    def test_status_update(self):
        svc = ClientService()
        c = svc.register_client("ST-01", "Status Org", "Banking & Financial Services", "s@test.com")
        updated = svc.update_status("ST-01", "MAINTENANCE")
        self.assertEqual(updated.status, "MAINTENANCE")

if __name__ == "__main__":
    unittest.main()
