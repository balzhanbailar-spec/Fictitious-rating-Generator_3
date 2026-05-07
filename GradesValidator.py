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
        print(f"'{self.filename}' файлы сәтті сақталды")
    def check_types(self):
        expected_int = ['student_id', 'subject_id']
        for col in expected_int:
            if col not in self.df.columns:
                print(f"'{col}' бағаны жоқ")
                return
            if not pd.api.types.is_integer_dtype(self.df[col]):
                print(f"'{col}' бағаны бүтін сан болуы тиіс")
                return
        if 'grade' not in self.df.columns:
            print("'grade' бағаны жоқ ")
            return
        if not pd.api.types.is_numeric_dtype(self.df['grade']):
            print("'grade' бағанды сандық болуы тиіс")
            return
        print("Деректер күтілгенге сәйкес келеді")
    def check_grade_range(self, min_grade=2, max_grade=5):
        grades = self.df['grade']
        if (grades < min_grade).any() or (grades > max_grade).any():
            print(f" Бағалар[{min_grade}, {max_grade}] диапазонында емес")
        else:
            print(f"'grade' бағаны: барлық бағалар[{min_grade}, {max_grade}] диапазонында")
    def show_info(self):
        print("Жалпы ақпарат")
        self.df.info()
        print("Алғашқы 5 жол")
        print(self.df.head())
        print("Сипаттамалық статистика")
        print(self.df.describe())
    def run(self):
        self.load()
        self.check_types()
        self.check_grade_range()
        self.show_info()
        print("Валидация сәтті орындалды")
if __name__ == "__main__":
    # 9
    print("9-тапсырма: fake_grades.csv ")
    gen = FakeGradesGenerator("fake_grades.csv", seed=42)
    gen.run()
    # 10
    print("10-тапсырма: fake_grades_v2.csv")
    corr = GradesCorrelation("fake_grades.csv", "fake_grades_v2.csv", seed=42)
    corr.run()
    # 11
    print("11-тапсырма: Валидация fake_grades.csv")
    validator = GradesValidator("fake_grades.csv")
    validator.run()