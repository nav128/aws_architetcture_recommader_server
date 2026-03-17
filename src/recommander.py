
from services.openai_client import ask_openai
from services.db_service import db
from services.encoder import one_hot_encode
from models.arch import Architecture

SCORE_THRESHOLD = 0.6

PROMPT_TEMPLATE = """You are an AWS architecture recommendation expert. Analyze the user requirements against the following 5 architecture options.

USER REQUIREMENTS:
{requirements}

ARCHITECTURE OPTIONS:
{options}

Your task:
1. considre the similarity scores of the options to the user requirements
2. recommend the top architectures that meet or exceed a match score of {threshold} out of 1

For each recommended architecture, provide:
- Architecture name/type
- Match score (0-1)
- Key strengths that align with requirements
- Brief explanation (2-3 sentences) why it was selected
- Stick to the facts in the provided options, do not make up details
- Relevant AWS services to implement it

Format your response as a structured list with clear sections for each recommended architecture.
Only include architectures with scores of {threshold} or higher."""


def recommander(requirements: Architecture):
    encoded = one_hot_encode(requirements.model_dump())
    options = db.search_for_recommendation(encoded)

    prompt = PROMPT_TEMPLATE.format(
        requirements=requirements.model_dump(),
        options=options,
        threshold=SCORE_THRESHOLD
    )

    return ask_openai(prompt)


if __name__ == "__main__":
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
    print(recommander(json_example))
    