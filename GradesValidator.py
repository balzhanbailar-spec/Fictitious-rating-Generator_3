import csv
import random
import numpy as np
import pandas as pd
class FakeGradesGenerator:
    def __init__(self, filename, seed=42):
        self.filename = filename
        self.seed = seed
        self.num_students = 10
        self.num_subjects = 5
    def generate(self):
        random.seed(self.seed)
        with open(self.filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["student_id", "subject_id", "grade"])
            for student_id in range(1, self.num_students + 1):
                for subject_id in range(1, self.num_subjects + 1):
                    grade = random.randint(2, 5)
                    writer.writerow([student_id, subject_id, grade])
    def run(self):
        self.generate()
        print("student_id,subject_id,grade")
        with open(self.filename, "r") as f:
            lines = f.readlines()[1:]
            for line in lines:
                print(line.strip())
class GradesCorrelation:
    def __init__(self, input_file, output_file, seed=42):
        self.input_file = input_file
        self.output_file = output_file
        self.rng = np.random.default_rng(seed)
    def process(self):
        # Чтение исходного файла
        with open(self.input_file, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        output_rows = []
        for row in rows:
            student_id = row['student_id']
            subject_id = row['subject_id']
            grade1 = float(row['grade'])
            noise = self.rng.normal(0, 0.3)
            grade2 = 0.7 * grade1 + noise
            grade2 = np.clip(grade2, 2.0, 5.0)
            output_rows.append([student_id, subject_id, grade1, round(grade2, 2)])
        with open(self.output_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["student_id", "subject_id", "grade1", "grade2"])
            writer.writerows(output_rows)
    def run(self):
        self.process()
        print("student_id,subject_id,grade1,grade2")
        with open(self.output_file, "r") as f:
            lines = f.readlines()[1:]
            for line in lines:
                print(line.strip())
class GradesValidator:
    def __init__(self, filename):
        self.filename = filename
        self.df = None
    def load(self):
        self.df = pd.read_csv(self.filename)
        print(f"✅ Файл '{self.filename}' успешно загружен.")
    def check_types(self):
        expected_int = ['student_id', 'subject_id']
        for col in expected_int:
            if col not in self.df.columns:
                print(f"❌ Колонка '{col}' отсутствует.")
                return
            if not pd.api.types.is_integer_dtype(self.df[col]):
                print(f"❌ Колонка '{col}' должна быть целочисленной.")
                return
        if 'grade' not in self.df.columns:
            print("❌ Колонка 'grade' отсутствует.")
            return
        if not pd.api.types.is_numeric_dtype(self.df['grade']):
            print("❌ Колонка 'grade' должна быть числовой.")
            return
        print("✅ Типы данных соответствуют ожидаемым.")
    def check_grade_range(self, min_grade=2, max_grade=5):
        grades = self.df['grade']
        if (grades < min_grade).any() or (grades > max_grade).any():
            print(f"❌ Есть оценки вне диапазона [{min_grade}, {max_grade}].")
        else:
            print(f"✅ Колонка 'grade': все оценки в диапазоне [{min_grade}, {max_grade}].")
    def show_info(self):
        print("\n=== Общая информация ===")
        self.df.info()
        print("\n=== Первые 5 строк ===")
        print(self.df.head())
        print("\n=== Описательная статистика ===")
        print(self.df.describe())
    def run(self):
        self.load()
        self.check_types()
        self.check_grade_range()
        self.show_info()
        print("\n✅ Валидация пройдена успешно.")
if __name__ == "__main__":
    # Задание 9
    print("=== Задание 9: fake_grades.csv ===\n")
    gen = FakeGradesGenerator("fake_grades.csv", seed=42)
    gen.run()
    # Задание 10
    print("\n=== Задание 10: fake_grades_v2.csv ===\n")
    corr = GradesCorrelation("fake_grades.csv", "fake_grades_v2.csv", seed=42)
    corr.run()
    # Задание 11
    print("\n=== Задание 11: Валидация fake_grades.csv ===\n")
    validator = GradesValidator("fake_grades.csv")
    validator.run()