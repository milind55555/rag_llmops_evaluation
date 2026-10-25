import argparse
from .pipeline import answer

def main():
    parser = argparse.ArgumentParser(description="Query the offline RAG demo")
    parser.add_argument("question", nargs="+")
    args = parser.parse_args()
    result = answer(" ".join(args.question))
    print(f"Question: {result['question']}")
    print(f"Answer: {result['answer']}")
    print(f"Sources: {', '.join(result['sources']) or 'none'}")
    print(f"Latency: {result['latency_ms']:.2f} ms")

if __name__ == "__main__":
    main()
