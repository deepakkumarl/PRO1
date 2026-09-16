import json
import os
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.config import settings
from app.rag.loader import DocumentLoader
from app.rag.splitter import TextSplitter
from app.rag.vectorstore import VectorStoreManager
from app.rag.retriever import DocumentRetriever
from app.rag.generator import OllamaGenerator


def run_evaluation():
    print("=" * 70)
    print("BMW SERVICE KNOWLEDGE RAG ASSISTANT - EVALUATION HARNESS")
    print("=" * 70)

    # Load dataset
    dataset_path = Path(__file__).resolve().parent / "eval_dataset.json"
    with open(dataset_path, "r", encoding="utf-8") as f:
        queries = json.load(f)

    print(f"Loaded {len(queries)} test queries from evaluation dataset.\n")

    # Initialize components
    doc_loader = DocumentLoader(settings.DOCUMENTS_DIR)
    raw_docs = doc_loader.load_all_documents()
    if not raw_docs:
        print("Error: No PDF documents found to evaluate against.")
        return

    text_splitter = TextSplitter()
    chunks = text_splitter.split_documents(raw_docs)

    vectorstore = VectorStoreManager()
    if not vectorstore.is_index_ready():
        print("Building vector index for evaluation...")
        vectorstore.build_index(chunks)

    retriever = DocumentRetriever(vectorstore)
    generator = OllamaGenerator()

    results = []
    correct_retrievals = 0
    correct_fallbacks = 0

    for item in queries:
        q_id = item["id"]
        question = item["question"]
        exp_doc = item["expected_document"]
        in_domain = item["is_in_domain"]

        docs, sources, confidence = retriever.retrieve(question)

        retrieved_docs = [s.document for s in sources]
        
        # Check retrieval success
        retrieval_pass = False
        if in_domain:
            if any(exp_doc.lower() in d.lower() for d in retrieved_docs):
                retrieval_pass = True
                correct_retrievals += 1
        else:
            if not confidence or len(sources) == 0:
                retrieval_pass = True
                correct_fallbacks += 1

        print(f"Query #{q_id}: '{question}'")
        print(f"  - In-Domain: {in_domain}")
        print(f"  - Expected Doc: {exp_doc}")
        print(f"  - Retrieved Docs: {retrieved_docs}")
        print(f"  - Top Confidence Met: {confidence}")
        print(f"  - Retrieval Result: {'[PASS]' if retrieval_pass else '[FAIL]'}")

        answer = generator.generate_answer(
            question=question,
            documents=docs,
            sources=sources,
            confidence_met=confidence
        )
        print(f"  - Answer Snippet: {answer[:120]}...\n")

        results.append({
            "id": q_id,
            "question": question,
            "retrieval_pass": retrieval_pass,
            "retrieved_sources": [s.dict() for s in sources],
            "confidence_met": confidence,
            "answer": answer
        })

    in_domain_total = sum(1 for q in queries if q["is_in_domain"])
    out_domain_total = len(queries) - in_domain_total

    retrieval_accuracy = (correct_retrievals / max(1, in_domain_total)) * 100
    fallback_accuracy = (correct_fallbacks / max(1, out_domain_total)) * 100

    print("=" * 70)
    print("EVALUATION METRICS SUMMARY:")
    print(f"Total Test Cases Evaluated: {len(queries)}")
    print(f"In-Domain Retrieval Accuracy: {retrieval_accuracy:.1f}% ({correct_retrievals}/{in_domain_total})")
    print(f"Out-of-Domain No-Answer Fallback Accuracy: {fallback_accuracy:.1f}% ({correct_fallbacks}/{out_domain_total})")
    print("=" * 70)

    output_report = Path(__file__).resolve().parent / "eval_report.json"
    with open(output_report, "w", encoding="utf-8") as f:
        json.dump({
            "in_domain_accuracy_pct": retrieval_accuracy,
            "fallback_accuracy_pct": fallback_accuracy,
            "results": results
        }, f, indent=2)

    print(f"Saved evaluation report to {output_report.name}")

if __name__ == "__main__":
    run_evaluation()
