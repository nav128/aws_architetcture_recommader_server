from enum import Enum

from pydantic import BaseModel, Field
from typing import Optional, Any
import datetime



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

class Scale(str, Enum):
    small  = "small"
    medium = "medium"
    large  = "large"

class TrafficPattern(str, Enum):
    steady        = "steady"
    bursty        = "bursty"
    spiky         = "spiky"
    scheduled     = "scheduled"
    unpredictable = "unpredictable"

class LatencySensitivity(str, Enum):
    low    = "low"
    medium = "medium"
    high   = "high"

class ProcessingStyle(str, Enum):
    request_response = "request_response"
    event_driven     = "event_driven"
    batch            = "batch"
    streaming        = "streaming"

class DataIntensity(str, Enum):
    low    = "low"
    medium = "medium"
    high   = "high"

class AvailabilityRequirement(str, Enum):
    standard = "standard"
    high     = "high"
    critical = "critical"

class OpsPreference(str, Enum):
    managed_services = "managed_services"
    balanced         = "balanced"
    self_managed_ok  = "self_managed_ok"

class BudgetSensitivity(str, Enum):
    low    = "low"
    medium = "medium"
    high   = "high"

# ── Architecture Model ────────────────────────────────────────────────────────

class Architecture(BaseModel):
    title:                    str
    description:              Optional[str] = Field(None)
    use_case:                 UseCase
    scale:                    Scale
    traffic_pattern:          TrafficPattern
    latency_sensitivity:      LatencySensitivity
    processing_style:         ProcessingStyle
    data_intensity:           DataIntensity
    availability_requirement: AvailabilityRequirement
    ops_preference:           OpsPreference
    budget_sensitivity:       BudgetSensitivity
    services:                 list[str] = Field(default_factory=list)
# 
    source_url: Optional[str] = None
    # scraped_at: Any = Field(default_factory=datetime.datetime.now().st)

# architecture_json = Architecture.model_dump_json()