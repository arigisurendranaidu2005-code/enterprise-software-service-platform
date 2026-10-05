from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    PROJECT_NAME: str = "Enterprise Software Service & Workflow Platform"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    SUPPORTED_DOMAINS: tuple = (
        "Banking & Financial Services",
        "Healthcare & Life Sciences",
        "Retail & Consumer Goods",
        "Education & ERP Solutions"
    )

settings = Settings()
