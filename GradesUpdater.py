import csv
import numpy as np
class GradesUpdater:
    def __init__(self, filename, seed=42):
        self.filename = filename
        self.rng = np.random.default_rng(seed)
    def update_grades(self):
        rows = []
        with open(self.filename, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if not row:
                    continue
                student_id = int(self.rng.integers(1, 11))
                subject_id = int(self.rng.integers(1, 6))
                grade = int(self.rng.integers(2, 6))
                rows.append([student_id, subject_id, grade])
        with open(self.filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["student_id", "subject_id", "grade"])
            writer.writerows(rows)
    def run(self):
        self.update_grades()
        print("Оценки обновлены с использованием RNG")
if __name__ == "__main__":
    app = GradesUpdater("fake_grades.csv", seed=42)
    app.run()