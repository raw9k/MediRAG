from langchain_huggingface import HuggingFaceEmbeddings


def get_embedding_model():
    """
    Load the HuggingFace embedding model.
    """
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    
    
if __name__ == "__main__":
    embedding_model = get_embedding_model()

    text = "What are the symptoms of diabetes?"
    embedding = embedding_model.embed_query(text)

    print(f"Embedding dimensions: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")