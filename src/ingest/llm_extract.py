
from services.openai_client import ask_openai

EXTRACTION_PROMPT = """
You are an AWS solutions architect. Given the README of an AWS sample repository,
extract structured architecture metadata.

README:
\"\"\"
{readme_text}
\"\"\"

Return ONLY a valid JSON object with exactly these keys and allowed values:

{{
  "description":              "<one sentence summary, or null>",
  "use_case":                 "web_application | public_api | ecommerce | real_time_analytics | batch_processing | event_processing | media_delivery | internal_tool | iot_ingestion | ml_inference",
  "scale":                    "small | medium | large",
  "traffic_pattern":          "steady | bursty | spiky | scheduled | unpredictable",
  "latency_sensitivity":      "low | medium | high",
  "processing_style":         "request_response | event_driven | batch | streaming",
  "data_intensity":           "low | medium | high",
  "availability_requirement": "standard | high | critical",
  "ops_preference":           "managed_services | balanced | self_managed_ok",
  "budget_sensitivity":       "low | medium | high",
  "services":                 ["<AWS service name>", ...]
}}

Rules:
- Choose exactly ONE value per field from the options listed above.
- For services, extract every AWS service mentioned (e.g. "Amazon S3", "AWS Lambda").
- If you are unsure about a field, pick the most reasonable default.
- Return ONLY the JSON object. No explanation, no markdown fences.
"""


def call_llm(readme_text: str) -> dict:
    """Send README to Claude and get back structured JSON."""

    prompt = EXTRACTION_PROMPT.format(
        readme_text=readme_text[:12000]  # stay within context limits
    )

    return ask_openai(prompt)
