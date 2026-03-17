# since i'v deisnged my system to rely on vector search, 
# and only after iv worte most my code I find out 
#   that the mongodb docker does support vector search.
# So I'v decided to keep the full table lodaed on ram and do a vector search myself.

import numpy as np
from services.mongo_client import collection

class DB:

    def __init__(self):
        self.local_table = {}
        self.vectors = []
        self.doc_ids = []  
        self.vectors_array = None  
        self.vectors_norm = None
        self.load_from_remote()

    def populate_local(self, documents):
        for doc in documents:
            doc["_id"] = str(doc["_id"])
            self.local_table[doc['_id']] = doc
            self.vectors.append(doc['encoded'])
            self.doc_ids.append(doc['_id'])
        
        # Convert to numpy array and compute norms
        self.vectors_array = np.array(self.vectors)
        self.vectors_norm = np.linalg.norm(self.vectors_array, axis=1)

    def load_from_remote(self):
        docs = list(collection.find())
        self.populate_local(docs)

    def insert_many(self, archs):
        result = collection.insert_many(archs)
        # Fetch the inserted documents to get their full data
        inserted_docs = list(collection.find({'_id': {'$in': result.inserted_ids}}))
        self.populate_local(inserted_docs)

    def get_all(self):
        return list(db.local_table.values())
    def search_for_recommendation(self, user_req_encoded, top_k=5):
        user_req_encoded = np.array(user_req_encoded)
        
        user_norm = np.linalg.norm(user_req_encoded)

        dot_products = np.dot(self.vectors_array, user_req_encoded)
        cosine_similarities = dot_products / (self.vectors_norm * user_norm)
        
        top_indices = np.argsort(cosine_similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            doc_id = self.doc_ids[idx]
            doc = self.local_table[doc_id]
            similarity_score = cosine_similarities[idx]
            results.append({
                'document': doc,
                'similarity': float(similarity_score)
            })
        
        return results

db = DB()
