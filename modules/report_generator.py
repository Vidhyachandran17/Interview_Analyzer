# modules/report_generator.py
def generate_report(analysis, fillers, scores):
    with open("report.txt", "w", encoding="utf-8") as file:
        file.write(f"Word Count: {analysis['word_count']}\n")
        file.write(f"Feedback: {analysis['feedback']}\n\n")
        file.write("Filler Words:\n")
        for k, v in fillers.items():
            file.write(f"{k}: {v}\n")
        file.write(f"\nScore: {scores['score']}\n")
