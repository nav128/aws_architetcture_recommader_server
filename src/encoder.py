from typing import Dict, List




# Define possible values for categorical fields
CATEGORIES = {
    "use_case": [
        "web_application", "public_api", "ecommerce", "real_time_analytics",
        "batch_processing", "event_processing", "media_delivery",
        "internal_tool", "iot_ingestion", "ml_inference"
    ],
    "scale": ["small", "medium", "large"],
    "traffic_pattern": ["steady", "bursty", "spiky", "scheduled", "unpredictable"],
    "latency_sensitivity": ["low", "medium", "high"],
    "processing_style": ["request_response", "event_driven", "batch", "streaming"],
    "data_intensity": ["low", "medium", "high"],
    "availability_requirement": ["standard", "high", "critical"],
    "ops_preference": ["managed_services", "balanced", "self_managed_ok"],
    "budget_sensitivity": ["low", "medium", "high"],
}

biases = {
    # Core operational priorities
    "availability_requirement": 3.0,   # very important, higher weight if reliability matters
    "latency_sensitivity": 2.5,        # important for apps that need low response times
    "traffic_pattern": 2.0,            # affects scaling strategy

    # Workload characteristics
    "processing_style": 1.8,           # event-driven vs batch affects service choice
    "data_intensity": 1.5,             # high data intensity favors storage/compute optimized services
    "scale": 1.5,                       # small/medium/large scale

    # Business / ops considerations
    "budget_sensitivity": 1.2,          # higher weight if budget matters
    "ops_preference": 1.0,              # managed vs self-managed

    # Use case specifics
    "use_case": 2.0,                    # certain services fit better for specific use cases
}

def one_hot_encode(json_obj: Dict) -> List[float]:
    """
    Encodes the JSON object into a numeric vector with optional biases.
    
    :param json_obj: Input JSON with the fields
    :param biases: Optional dictionary of field weights, e.g., {'use_case': 2.0}
    :return: Encoded vector
    """
    vector = []

    for field, options in CATEGORIES.items():
        value = json_obj.get(field)
        bias = biases.get(field, 1.0)  # default weight = 1.0
        # One-hot encoding
        for option in options:
            vector.append(bias if value == option else 0.0)

    return vector




if __name__ == "main":
    # Example usage
    json_example = {
        "use_case": "web_application",
        "scale": "medium",
        "traffic_pattern": "burst",
        "latency_sensitivity": "high",
        "processing_style": "request_response",
        "data_intensity": "medium",
        "availability_requirement": "high",
        "ops_preference": "balanced",
        "budget_sensitivity": "medium"
    }
    vector = one_hot_encode(json_example)
    print(vector)
    print("Vector length:", len(vector))