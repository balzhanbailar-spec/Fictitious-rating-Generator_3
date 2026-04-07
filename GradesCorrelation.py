import csv
import numpy as np


class GradesCorrelation:
    def __init__(self, input_file, output_file, seed=42):
        self.input_file = input_file
        self.output_file = output_file
        self.rng = np.random.default_rng(seed)

    def process(self):
        rows = []

        # читаем старый файл
        with open(self.input_file, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                grade1 = float(row["grade"])

                # шум
                noise = self.rng.normal(0, 0.3)

                # корреляция
                grade2 = 0.7 * grade1 + noise
                grade2 = np.clip(grade2, 2.0, 5.0)

                rows.append([
                    row["student_id"],
                    row["subject_id"],
                    grade1,
                    round(float(grade2), 2)
                ])

        # сохраняем НОВЫЙ файл
        with open(self.output_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["student_id", "subject_id", "grade1", "grade2"])
            writer.writerows(rows)
    def run(self):
        self.process()
        print("Создан новый файл с корреляцией")
if __name__ == "__main__":
    app = GradesCorrelation("fake_grades.csv", "fake_grades_v2.csv", seed=42)
    app.run()