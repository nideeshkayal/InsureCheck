import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def search_policies(query, policy_names=None, k=5, chroma_store_path="./chroma_store"):    

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    vectorstore = Chroma(
        persist_directory=chroma_store_path,
        embedding_function=embedding_model
    )

    if policy_names is None:
        return vectorstore.similarity_search(query, k=k)

    return vectorstore.similarity_search(
        query, 
        k=k, 
        filter={"policy_name": policy_names}
    )