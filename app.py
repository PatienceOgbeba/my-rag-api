from fastapi import FastAPI
import chromadb
import ollama 

app = FastAPI()
chromadb_client = chromadb.PersistentClient(path="./db")
collection = chromadb_client.get_or_create_collection("docs")

@app.post("/query/")
def query(q: str):
    results = collection.query(query_texts=[q], n_results=1)
    context = results['documents'][0][0] if results["documents"] else ""

    answer = ollama.generate(model ="tinyllama", prompt=f"Context:\n{context}\n\nQuestion: {q}\n\nAnswer clearly and concisely:")

    return {"answer": answer["response"]}