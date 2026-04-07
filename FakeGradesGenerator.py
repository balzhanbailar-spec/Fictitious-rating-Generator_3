import csv
import random
class FakeGradesGenerator:
    def __init__(self, filename, seed=42):
        self.filename = filename
        self.seed = seed
        self.students = ["Ali", "Aruzhan", "Dias", "Dana", "Nursultan"]
        self.subjects = ["Math", "Physics", "History", "English"]
    def generate(self):
        random.seed(self.seed)
        with open(self.filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["student", "subject", "grade"])
            for student in self.students:
                for subject in self.subjects:
                    grade = random.randint(50, 100)
                    writer.writerow([student, subject, grade])
    def run(self):
        self.generate()
        print(f"{self.filename} файл создан")
if __name__ == "__main__":
    app = FakeGradesGenerator("fake_grades.csv", seed=42)
    app.run()