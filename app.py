import json
from graph import support_graph

def main():

    print("===== AI Support Agent =====")
    print("Type 'exit' to quit.\n")

    while True:

        question = input("Ask: ")

        if question.lower() == "exit":
            break

        result = support_graph.invoke({
            "question": question,
            "retry": 0
        })

        print("\nAnswer:")
        print(result["answer"])

        print("\nJSON Output:")
        print(json.dumps(result, indent=4))

        print("-" * 50)

if __name__ == "__main__":
    main()