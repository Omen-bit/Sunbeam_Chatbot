from langchain_chroma import Chroma
from langchain.chat_models import init_chat_model
from langchain.embeddings import init_embeddings
from collections import defaultdict

BASE_URL = "http://127.0.0.1:1234/v1"
API_KEY = "lm_studio"

embeddings_model = init_embeddings(
    model="text-embedding-nomic-embed-text-v1.5-embedding",
    provider="openai",
    base_url=BASE_URL,
    api_key=API_KEY,
    check_embedding_ctx_length=False
)

vectordb = Chroma(
    collection_name="sunbeam_knowledge",
    embedding_function=embeddings_model,
    persist_directory="chroma_db"
)

print("Total vectors:", vectordb._collection.count())

llm = init_chat_model(
    model="openai/gpt-oss-20b",
    model_provider="openai",
    base_url=BASE_URL,
    api_key=API_KEY,
    temperature=0.2
)
query = "Give me fees about course data structure and algorithm nothing else"
print("\nUser Question:", query)

docs = vectordb.similarity_search(query, k=12)

grouped = defaultdict(list)

for d in docs:
    content = d.page_content.strip()

    if len(content) < 40:
        continue

    course = d.metadata.get("course", "Unknown Course")
    section = d.metadata.get("section", "General")

    grouped[(course, section)].append(content)

context_blocks = []

for (course, section), texts in grouped.items():
    block = f"{course}\n{section}\n" + "\n".join(texts)
    context_blocks.append(block)

context = "\n\n---\n\n".join(context_blocks)

prompt = f"""
You are an expert course advisor for Sunbeam Institute.

Rules:
- Use ONLY the information provided in the context
- Do NOT add external knowledge
- Do NOT hallucinate
- Answer clearly and professionally

Context:
{context}

Question:
{query}

Answer:
"""

response = llm.invoke(prompt)

print("\n===== FINAL REFINED ANSWER =====\n")
print(response.content)
