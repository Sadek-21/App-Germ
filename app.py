import tkinter as tk
from tkinter import messagebox
import json

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hörverstehen Test")
        self.score = 0
        self.current_teil = 1
        self.current_exam = 0  # Start from the first exam

        # Load JSON data
        with open('exams_data.json', 'r') as f:
            self.exams_data = json.load(f)['exams']

        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        self.load_questions()

    def load_questions(self):
        # Get the current exam and teil data
        exam = self.exams_data[self.current_exam]
        teil_key = f"teil{self.current_teil}"
        questions_data = exam['parts'][teil_key]

        # Clear the frame
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.answers = []  # Reset answers

        # Add headers
        tk.Label(self.frame, text="Richtig", font=("Arial", 12)).grid(row=0, column=1, padx=10)
        tk.Label(self.frame, text="Falsch", font=("Arial", 12)).grid(row=0, column=2, padx=10)

        # Create questions and answer options
        for i, question in enumerate(questions_data):
            tk.Label(self.frame, text=f"{i + 1}.", font=("Arial", 12)).grid(row=i + 1, column=0, padx=10)
            tk.Label(self.frame, text=question["question"], wraplength=400, anchor="w", justify="left").grid(row=i + 1, column=3, padx=10, sticky="w")

            # Add Radiobuttons for "Richtig" and "Falsch"
            var = tk.StringVar(value="None")
            self.answers.append((var, question))  # Store both var and question
            tk.Radiobutton(self.frame, variable=var, value="Richtig").grid(row=i + 1, column=1)
            tk.Radiobutton(self.frame, variable=var, value="Falsch").grid(row=i + 1, column=2)

        # Submit Button
        self.submit_button = tk.Button(self.root, text="Submit", command=self.check_answers)
        self.submit_button.pack(pady=20)

    def check_answers(self):
        # Disable the Submit button after submission
        self.submit_button.config(state=tk.DISABLED)

        # Check each answer and color the results
        correct_count = 0
        for i, (var, question) in enumerate(self.answers):
            answer_label = tk.Label(self.frame, text="Your Answer", font=("Arial", 12))

            if var.get() == question["correct"]:
                answer_label = tk.Label(self.frame, text="Correct", font=("Arial", 12), fg="green")
                correct_count += 1
            else:
                answer_label = tk.Label(self.frame, text="Wrong", font=("Arial", 12), fg="red")

            answer_label.grid(row=i + 1, column=4, padx=10)

        # Show message with the score
        messagebox.showinfo("Results", f"You got {correct_count}/{len(self.answers)} correct.")

        # Add a button to move to the next Teil or finish the exam
        if self.current_teil < 3:  # If it's Teil 1 or 2
            next_button = tk.Button(self.root, text=f"Go to Teil {self.current_teil + 1}", command=self.go_to_next_teil)
            next_button.pack(pady=10)
        else:  # If it's Teil 3, show the "Go to Next Exam" or "Finish" button
            if self.current_exam < len(self.exams_data) - 1:
                next_exam_button = tk.Button(self.root, text="Go to Next Exam", command=self.go_to_next_exam)
                next_exam_button.pack(pady=10)
            else:
                finish_button = tk.Button(self.root, text="Finish", command=self.finish_exam)
                finish_button.pack(pady=10)

    def go_to_next_teil(self):
        self.current_teil += 1
        self.submit_button.pack_forget()  # Remove submit button
        self.load_questions()

    def go_to_next_exam(self):
        self.current_exam += 1
        self.current_teil = 1  # Reset Teil to 1 for the next exam
        self.submit_button.pack_forget()  # Remove submit button
        self.load_questions()

    def finish_exam(self):
        messagebox.showinfo("Exam Finished", "You have completed all exams!")
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
