# read HTML content from a URL, send to llm to extract architecture information, and store in MongoDB
import base64
import json
import os
import time
from typing import Optional
import requests
from llm_extract import call_llm
from models.arch import Architecture
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")  # Optional: GitHub PAT to increase rate limits
# ── Helpers ───────────────────────────────────────────────────────────────────

def decode_readme(api_response: dict) -> str:
    content  = api_response.get("content", "")
    encoding = api_response.get("encoding", "base64")
    if encoding == "base64":
        return base64.b64decode(content).decode("utf-8", errors="ignore")
    return content


def get_headers(github_token: Optional[str] = None) -> dict:
    headers = {"Accept": "application/vnd.github+json"}
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"
    return headers

def scrape_github_aws_samples(
    max_repos:         int   = 1,
    min_stars:         int   = 10,
    request_delay:     float = 0.5,
) -> list[Architecture]:
    """
    Scrape aws-samples GitHub org and return fully populated Architecture objects.

    Args:
        anthropic_api_key: Your Anthropic API key for LLM field extraction.
        github_token:      GitHub PAT — raises rate limit from 60 to 5000 req/hour.
        max_repos:         Hard cap on repos to process.
        min_stars:         Skip repos below this star count.
        request_delay:     Seconds to wait between GitHub API calls.

    Returns:
        List of validated Architecture objects.
    """
    session = requests.Session()
    session.headers.update(get_headers(github_token))

    results: list[Architecture] = []
    page = 1

    print(f"[GitHub] Scraping aws-samples (max={max_repos}, min_stars={min_stars})")

    while len(results) < max_repos:

        # ── 1. Fetch repo listing ─────────────────────────────────────────────
        resp = session.get(
            "https://api.github.com/orgs/aws-samples/repos",
            params={"per_page": 100, "page": page, "type": "public"},
            timeout=15,
        )
        resp.raise_for_status()
        repos = resp.json()

        if not repos:
            print(f"[GitHub] No more repos at page {page}.")
            break

        print(f"[GitHub] Page {page} — {len(repos)} repos")

        for repo in repos:
            if len(results) >= max_repos:
                break

            name        = repo.get("name", "")
            stars       = repo.get("stargazers_count", 0)
            description = repo.get("description") or None
            repo_url    = repo.get("html_url", "")

            # ── 2. Filter ─────────────────────────────────────────────────────
            if stars < min_stars:
                continue
            if repo.get("archived"):
                continue

            # ── 3. Fetch README ───────────────────────────────────────────────
            time.sleep(request_delay)
            try:
                readme_resp = session.get(
                    f"https://api.github.com/repos/aws-samples/{name}/readme",
                    timeout=15,
                )
                if readme_resp.status_code == 404:
                    print(f"  [skip] {name} — no README")
                    continue
                readme_resp.raise_for_status()
                readme_text = decode_readme(readme_resp.json())
            except requests.RequestException as e:
                print(f"  [error] {name} — {e}")
                continue

            if len(readme_text.strip()) < 200:
                print(f"  [skip] {name} — README too short")
                continue

            # ── 4. LLM extraction ─────────────────────────────────────────────
            try:
                extracted = call_llm(readme_text)
            except Exception as e:
                print(f"  [error] {name} — LLM failed: {e}")
                continue

            # ── 5. Build and validate Architecture object ─────────────────────
            try:
                architecture = Architecture(
                    title=name.replace("-", " ").replace("_", " ").title(),
                    description=extracted.get("description", description),
                    use_case=extracted["use_case"],
                    scale=extracted["scale"],
                    traffic_pattern=extracted["traffic_pattern"],
                    latency_sensitivity=extracted["latency_sensitivity"],
                    processing_style=extracted["processing_style"],
                    data_intensity=extracted["data_intensity"],
                    availability_requirement=extracted["availability_requirement"],
                    ops_preference=extracted["ops_preference"],
                    budget_sensitivity=extracted["budget_sensitivity"],
                    services=extracted.get("services", []),
                    source_url=repo_url
                )
                results.append(architecture)
                print(f"  [ok] {name} ★{stars} → use_case={architecture.use_case}, scale={architecture.scale}")

            except Exception as e:
                print(f"  [error] {name} — validation failed: {e}")
                continue

        page += 1
        time.sleep(request_delay)

    print(f"[GitHub] Done — {len(results)} architectures collected")
    json.dump([arch.model_dump() for arch in results], Path("architectures.json").open("w"), indent=2   )
    return results


scrape_github_aws_samples(max_repos=5)