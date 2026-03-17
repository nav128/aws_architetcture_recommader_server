from enum import Enum

from pydantic import BaseModel, Field
from typing import Optional, Any
import datetime

def stringifible_enum(cls):
    def enum_value_to_string(self):
        return str(self.value)
    cls.__repr__ = enum_value_to_string
    return cls

@stringifible_enum
class UseCase(str, Enum):
    web_application     = "web_application"
    public_api          = "public_api"
    ecommerce           = "ecommerce"
    real_time_analytics = "real_time_analytics"
    batch_processing    = "batch_processing"
    event_processing    = "event_processing"
    media_delivery      = "media_delivery"
    internal_tool       = "internal_tool"
    iot_ingestion       = "iot_ingestion"
    ml_inference        = "ml_inference"

@stringifible_enum
class Scale(str, Enum):
    small  = "small"
    medium = "medium"
    large  = "large"

@stringifible_enum
class TrafficPattern(str, Enum):
    steady        = "steady"
    bursty        = "bursty"
    spiky         = "spiky"
    scheduled     = "scheduled"
    unpredictable = "unpredictable"

@stringifible_enum
class LatencySensitivity(str, Enum):
    low    = "low"
    medium = "medium"
    high   = "high"

@stringifible_enum
class ProcessingStyle(str, Enum):
    request_response = "request_response"
    event_driven     = "event_driven"
    batch            = "batch"
    streaming        = "streaming"

@stringifible_enum
class DataIntensity(str, Enum):
    low    = "low"
    medium = "medium"
    high   = "high"

@stringifible_enum
class AvailabilityRequirement(str, Enum):
    standard = "standard"
    high     = "high"
    critical = "critical"

@stringifible_enum
class OpsPreference(str, Enum):
    managed_services = "managed_services"
    balanced         = "balanced"
    self_managed_ok  = "self_managed_ok"

@stringifible_enum
class BudgetSensitivity(str, Enum):
    low    = "low"
    medium = "medium"
    high   = "high"

# ── Architecture Model ────────────────────────────────────────────────────────
def add_timestamp() -> str:
    return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")

class ArchitectureRequest(BaseModel):
    use_case:                 UseCase
    scale:                    Scale
    traffic_pattern:          TrafficPattern
    latency_sensitivity:      LatencySensitivity
    processing_style:         ProcessingStyle
    data_intensity:           DataIntensity
    availability_requirement: AvailabilityRequirement
    ops_preference:           OpsPreference
    budget_sensitivity:       BudgetSensitivity

class Architecture(ArchitectureRequest):
    title:                    str
    description:              Optional[str] = Field(None)
    services:                 list[str] = Field(default_factory=list)
    source_url: Optional[str] = None
    encoded: list[int] = Field(default_factory=list)
    scraped_at: str = Field(default_factory=add_timestamp)

if __name__ == "__main__":
    print(Architecture(
        title="",
        description="",
        use_case=UseCase.batch_processing,
        scale=Scale.large,
        traffic_pattern=TrafficPattern.bursty,
        latency_sensitivity=LatencySensitivity.high,
        processing_style=ProcessingStyle.batch,
        data_intensity=DataIntensity.high,
        availability_requirement=AvailabilityRequirement.high,
        ops_preference=OpsPreference.balanced,
        budget_sensitivity=BudgetSensitivity.high,
        
    ))