import argparse
from langchain.vectorstores.chroma import Chroma
from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer this question based on the above context: {question}
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, help="query text", required=True)
    args = parser.parse_args()
    query = args.query

    # Prepare the DB with embedding function
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=HuggingFaceEmbeddings())

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query, k=3)
    if len(results) == 0 or results[0][1] < -0.1:
        print(f"Unable to find matching results.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query)

    model = Ollama(model="llama2-uncensored")
    response_text = model.stream(prompt)
    for text in response_text:
        print(text)


if __name__ == "__main__":
    main()