

import json
from pathlib import Path
from typing import List

from scraper import scrape_github_aws_samples
from models.arch import Architecture
from encoder import one_hot_encode
from mongo_client import collection

def ingest():
    architectures: List[Architecture] = scrape_github_aws_samples()
    
    # architectures = json.load(Path("architectures.json").open("r"))
    
    for arch in architectures:
        arch.encoded = one_hot_encode(arch)
    collection.insert_many(architectures)
    return len(architectures)
    
print(ingest())