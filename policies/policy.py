import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def search_policies(query, policy_names=None, k=5):    

    policies_dir = os.path.dirname(os.path.abspath(__file__))
    chroma_store_path = os.path.join(policies_dir, "chroma_store")
    
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    vectorstore = Chroma(
        persist_directory=chroma_store_path,
        embedding_function=embedding_model
    )
    
    if policy_names is None:
        return vectorstore.similarity_search(query, k=k)

    if isinstance(policy_names, str):
        policy_names = [policy_names]

    return vectorstore.similarity_search(
        query, 
        k=k, 
        filter={"policy_name": {"$in": policy_names}}
    )