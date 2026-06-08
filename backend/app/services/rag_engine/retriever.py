from langchain_community.vectorstores import Chroma

def retrieve_rag_context(question: str, schema_store: Chroma, examples_store: Chroma, docs_store: Chroma, k_examples: int = 3, k_docs: int = 3) -> dict:
    # Schema: lấy TẤT CẢ bảng (chỉ 14 bảng, không cần similarity search)
    all_schema_docs = schema_store.similarity_search("", k=50)
    example_docs = examples_store.similarity_search(question, k=k_examples)
    knowledge_docs = docs_store.similarity_search(question, k=k_docs)

    schema_context = "\n\n".join(doc.page_content for doc in all_schema_docs)
    examples_text = [f"Câu hỏi: {doc.page_content}\nSQL:\n{doc.metadata['sql']}" for doc in example_docs]
    examples_context = "\n\n---\n\n".join(examples_text)
    docs_context = "\n\n".join(doc.page_content for doc in knowledge_docs)

    return {
        "schema": schema_context,
        "examples": examples_context,
        "docs": docs_context,
        "schema_tables": [doc.metadata.get("table", "Unknown") for doc in all_schema_docs],
    }