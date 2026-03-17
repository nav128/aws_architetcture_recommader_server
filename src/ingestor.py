
import json
from pathlib import Path
from typing import List

from ingest.scraper import scrape_github_aws_samples
from services.encoder import one_hot_encode
from services.db_service import db

def ingest():
    architectures: List[dict] = scrape_github_aws_samples(max_repos=25)
    
    # architectures = json.load(Path("architectures.json").open("r"))
    
    for arch in architectures:
        arch["encoded"] = one_hot_encode(arch)
    db.insert_many(architectures)
    return architectures
    
if __name__ == "__main__":
    print(ingest)