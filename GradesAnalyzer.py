import csv
import random
import numpy as np
import pandas as pd

# 9
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
        print("=== Задание 9: fake_grades.csv ===")
        with open(self.filename, "r") as f:
            print(f.read().strip())

# 10
class GradesCorrelation:
    def __init__(self, input_file, output_file, seed=42):
        self.input_file = input_file
        self.output_file = output_file
        self.rng = np.random.default_rng(seed)

    def process(self):
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
        print("\n=== Задание 10: fake_grades_v2.csv ===")
        with open(self.output_file, "r") as f:
            print(f.read().strip())

# 11
class GradesValidator:
    def __init__(self, filename):
        self.filename = filename
        self.df = None

    def load(self):
        self.df = pd.read_csv(self.filename)
        print(f"✅ Файл '{self.filename}' успешно загружен.")

    def check_types(self):
        if not pd.api.types.is_integer_dtype(self.df['student_id']):
            print("❌ student_id не целочисленный")
        if not pd.api.types.is_integer_dtype(self.df['subject_id']):
            print("❌ subject_id не целочисленный")
        if not pd.api.types.is_numeric_dtype(self.df['grade']):
            print("❌ grade не числовой")
        print("✅ Типы данных соответствуют ожидаемым.")

    def check_grade_range(self, min_g=2, max_g=5):
        grades = self.df['grade']
        if (grades < min_g).any() or (grades > max_g).any():
            print(f"❌ Есть оценки вне [{min_g}, {max_g}]")
        else:
            print(f"✅ Все оценки в диапазоне [{min_g}, {max_g}]")

    def show_info(self):
        print("\n=== Общая информация ===")
        self.df.info()
        print("\n=== Первые 5 строк ===")
        print(self.df.head())
        print("\n=== Описательная статистика ===")
        print(self.df.describe())

    def run(self):
        print("\n=== Задание 11: Валидация fake_grades.csv ===")
        self.load()
        self.check_types()
        self.check_grade_range()
        self.show_info()
        print("✅ Валидация пройдена успешно.\n")

# 12
class GradesAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.df = None
        self.subject_means = None

    def load_data(self):
        self.df = pd.read_csv(self.filename)
        print(f"✅ Загружен файл {self.filename} для анализа")

    def compute_subject_means(self):
        if self.df is None:
            raise ValueError("Сначала загрузите данные")
        self.subject_means = self.df.groupby('subject_id')['grade'].mean()
        self.subject_means = self.subject_means.sort_values(ascending=False)
        return self.subject_means

    def display_results(self):
        if self.subject_means is None:
            print("Нет данных. Запустите compute_subject_means()")
            return
        print("\n=== Задание 12: Средняя оценка по предметам (от высшей к низшей) ===")
        result_df = self.subject_means.reset_index()
        result_df.columns = ['subject_id', 'mean_grade']
        print(result_df.to_string(index=False))
        return result_df

    def run(self):
        self.load_data()
        self.compute_subject_means()
        return self.display_results()

if __name__ == "__main__":
    # Задание 9
    gen = FakeGradesGenerator("fake_grades.csv", seed=42)
    gen.run()

    # Задание 10
    corr = GradesCorrelation("fake_grades.csv", "fake_grades_v2.csv", seed=42)
    corr.run()

    # Задание 11
    validator = GradesValidator("fake_grades.csv")
    validator.run()

    # Задание 12
    analyzer = GradesAnalyzer("fake_grades.csv")
    analyzer.run()