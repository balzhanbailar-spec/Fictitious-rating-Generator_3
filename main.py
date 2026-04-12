import csv
import random
import numpy as np

# ========== 1. Генератор исходных данных (задание 9) ==========
class FakeGradesGenerator:
    def __init__(self, filename, seed=42):
        self.filename = filename
        self.seed = seed
        self.num_students = 10      # student_id 1..10
        self.num_subjects = 5       # subject_id 1..5

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
        print(f"[OK] {self.filename} создан (студентов: {self.num_students}, предметов: {self.num_subjects}, оценки 2-5)")

# ========== 2. Добавление корреляции (задание 10) ==========
class GradesCorrelation:
    def __init__(self, input_file, output_file, seed=42):
        self.input_file = input_file
        self.output_file = output_file
        self.rng = np.random.default_rng(seed)

    def process(self):
        # Читаем исходный файл
        with open(self.input_file, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Нормализуем ключи (на случай пробелов или регистра)
        normalized = []
        for row in rows:
            clean = {k.strip().lower(): v for k, v in row.items()}
            normalized.append(clean)

        output_rows = []
        for row in normalized:
            student_id = row['student_id']
            subject_id = row['subject_id']
            grade1 = float(row['grade'])
            noise = self.rng.normal(0, 0.3)          # шум с нормальным распределением
            grade2 = 0.7 * grade1 + noise
            grade2 = np.clip(grade2, 2.0, 5.0)       # обрезаем до допустимого диапазона
            output_rows.append([student_id, subject_id, grade1, round(grade2, 2)])

        # Записываем новый CSV
        with open(self.output_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["student_id", "subject_id", "grade1", "grade2"])
            writer.writerows(output_rows)

    def run(self):
        self.process()
        print(f"[OK] {self.output_file} создан (grade1 – исходная, grade2 = 0.7*grade1 + шум, диапазон 2-5)")

# ========== 3. Обновление оценок в исходном файле ==========
class GradesUpdater:
    def __init__(self, filename, seed=42):
        self.filename = filename
        self.rng = np.random.default_rng(seed)

    def update_grades(self):
        # Читаем все строки
        with open(self.filename, "r") as f:
            reader = csv.reader(f)
            header = next(reader)           # пропускаем заголовок
            rows = list(reader)

        # Обновляем оценки, оставляя student_id и subject_id неизменными
        updated = []
        for row in rows:
            if len(row) >= 2:
                student_id = row[0]
                subject_id = row[1]
                new_grade = int(self.rng.integers(2, 6))   # 2,3,4,5
                updated.append([student_id, subject_id, new_grade])

        # Перезаписываем файл
        with open(self.filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(updated)

    def run(self):
        self.update_grades()
        print(f"[OK] {self.filename} обновлён (новые случайные оценки 2-5 для тех же студентов и предметов)")

# ========== Главная функция (запуск всех трёх этапов) ==========
def main():
    print("=== Задание 9: генерация исходного CSV ===\n")
    gen = FakeGradesGenerator("fake_grades.csv", seed=42)
    gen.run()

    print("\n=== Задание 10: создание CSV с корреляцией ===\n")
    corr = GradesCorrelation("fake_grades.csv", "fake_grades_v2.csv", seed=42)
    corr.run()

    print("\n=== Задание 11 (дополнительно): обновление исходного CSV ===\n")
    updater = GradesUpdater("fake_grades.csv", seed=42)
    updater.run()

    print("\n✅ Все скрипты выполнены. Файлы созданы/обновлены.")
    print("   - fake_grades.csv      : исходные оценки (студент, предмет, оценка 2-5)")
    print("   - fake_grades_v2.csv   : исходная + скоррелированная оценка grade2")

if __name__ == "__main__":
    main()