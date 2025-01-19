from pinecone import Pinecone, ServerlessSpec
import os

api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=api_key)

index_name = "quickstart"
# ==================================
pc.create_index(
    name=index_name,
    dimension=1024, # Replace with your model dimensions
    metric="cosine", # Replace with your model metric
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    ) 
)

query = "Tell me about the tech company known as Apple."

embedding = pc.inference.embed(
    model="multilingual-e5-large",
    inputs=[query],
    parameters={
        "input_type": "query"
    }
)

# ================
results = index.query(
    namespace="ns1",
    vector=embedding[0].values,
    top_k=3,
    include_values=False,
    include_metadata=True
)

print(results)