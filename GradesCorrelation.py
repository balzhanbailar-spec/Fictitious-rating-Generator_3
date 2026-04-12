import csv
import numpy as np
class GradesCorrelation:
    def __init__(self, input_file, output_file, seed=42):
        self.input_file = input_file
        self.output_file = output_file
        self.rng = np.random.default_rng(seed)
    def process(self):
        with open(self.input_file, "r") as file:
            sample = file.readline()
            file.seek(0)
            if 'student' in sample.lower() and 'subject' in sample.lower():
                reader = csv.DictReader(file)
                rows = []
                for row in reader:
                    # Приводим ключи к нижнему регистру и убираем пробелы
                    clean_row = {k.strip().lower(): v for k, v in row.items()}
                    rows.append(clean_row)
            else:
                reader = csv.reader(file)
                rows = []
                for row in reader:
                    if len(row) >= 3:
                        rows.append({
                            'student': row[0],
                            'subject': row[1],
                            'grade': row[2]
                        })
        output_rows = []
        for row in rows:
            try:
                grade1 = float(row['grade'])
                student = row['student']   # теперь используем 'student'
                subject = row['subject']   # теперь используем 'subject'
            except KeyError as e:
                print("Доступные колонки:", list(row.keys()))
                raise KeyError(f"Не найдена колонка {e}. Проверьте имена колонок в CSV.")
            noise = self.rng.normal(0, 0.3)
            grade2 = 0.7 * grade1 + noise
            grade2 = np.clip(grade2, 2.0, 5.0)
            output_rows.append([student, subject, grade1, round(grade2, 2)])
        with open(self.output_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["student_id", "subject_id", "grade1", "grade2"])
            writer.writerows(output_rows)
    def run(self):
        self.process()
        print(f"Создан файл {self.output_file} с корреляцией (grade2 = 0.7*grade1 + шум)")
if __name__ == "__main__":
    app = GradesCorrelation("fake_grades.csv", "fake_grades_v2.csv", seed=42)
    app.run()