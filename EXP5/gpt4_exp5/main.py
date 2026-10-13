from preprocessing import preprocess_text
from prompt import create_prompt
from legal_analyzer import analyze_document


def read_document():
    print("\n========== LEGAL DOCUMENT INPUT ==========")
    print("1. Enter document manually")
    print("2. Read document from TXT file")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        print("\nEnter the legal document.")
        print("Type END on a new line when finished.\n")

        lines = []

        while True:
            line = input()

            if line == "END":
                break

            lines.append(line)

        return "\n".join(lines)

    elif choice == "2":
        filename = input("Enter TXT file name: ")

        try:
            with open(filename, "r", encoding="utf-8") as file:
                return file.read()

        except FileNotFoundError:
            print("File not found.")
            return None

    else:
        print("Invalid choice.")
        return None


def save_report(analysis):
    with open("outputs/legal_analysis.txt", "w", encoding="utf-8") as file:
        file.write(analysis)

    print("\nReport saved successfully!")
    print("Location: outputs/legal_analysis.txt")


def main():
    print("\n==============================================")
    print("   AUTOMATED LEGAL DOCUMENT ANALYZER")
    print("==============================================")

    document = read_document()

    if document is None:
        return

    if document.strip() == "":
        print("No document content provided.")
        return

    print("\nPreprocessing document...")
    cleaned_document = preprocess_text(document)

    print("Creating analysis prompt...")
    prompt = create_prompt(cleaned_document)

    print("Analyzing document using AI...")
    analysis = analyze_document(prompt)

    print("\n==============================================")
    print("          LEGAL DOCUMENT ANALYSIS")
    print("==============================================")

    print(analysis)

    save_report(analysis)

    print("\nAnalysis completed successfully!")


if __name__ == "__main__":
    main()