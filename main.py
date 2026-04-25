import csv
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


# ========== Задание 9: Генератор исходных данных ==========
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
        print(f"=== Задание 9: Файл '{self.filename}' создан ===")


# ========== Задание 10: Генерация скоррелированных данных ==========
class GradesCorrelation:
    def __init__(self, input_file, output_file, seed=42):
        self.input_file = input_file
        self.output_file = output_file
        self.rng = np.random.default_rng(seed)

    def process(self):
        if not os.path.exists(self.input_file):
            print(f"Ошибка: {self.input_file} не найден")
            return

        with open(self.input_file, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        output_rows = []
        for row in rows:
            sid = row['student_id']
            subid = row['subject_id']
            grade1 = float(row['grade'])

            # grade2 = 0.7 * grade1 + шум
            noise = self.rng.normal(0, 0.3)
            grade2 = np.clip(0.7 * grade1 + noise, 2.0, 5.0)
            output_rows.append([sid, subid, grade1, round(grade2, 2)])

        with open(self.output_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["student_id", "subject_id", "grade1", "grade2"])
            writer.writerows(output_rows)

    def run(self):
        self.process()
        print(f"=== Задание 10: Файл '{self.output_file}' с корреляцией создан ===")


# ========== Задание 11: Валидация данных (Pandas) ==========
class GradesValidator:
    def __init__(self, filename):
        self.filename = filename
        self.df = None

    def run(self):
        print("\n=== Задание 11: Валидация данных ===")
        if not os.path.exists(self.filename):
            print("Файл не найден.")
            return

        self.df = pd.read_csv(self.filename)
        print(f"✅ Файл '{self.filename}' загружен.")

        # Проверка типов данных
        print(f"Типы колонок:\n{self.df.dtypes}")

        # Проверка диапазона оценок [2, 5]
        grades = self.df['grade']
        if (grades < 2).any() or (grades > 5).any():
            print("❌ Ошибка: Есть оценки вне диапазона 2-5!")
        else:
            print("✅ Все оценки в корректном диапазоне [2, 5].")

        print("\n--- Описательная статистика ---")
        print(self.df.describe())


# ========== Задание 12: Анализ средних баллов ==========
class GradesAnalyzer:
    def __init__(self, filename):
        self.filename = filename

    def run(self):
        print("\n=== Задание 12: Анализ средних баллов по предметам ===")
        df = pd.read_csv(self.filename)
        # Группировка по ID предмета и расчет среднего
        means = df.groupby('subject_id')['grade'].mean().sort_values(ascending=False)
        print(means.reset_index().to_string(index=False))
        return means


# ========== Задание 13: Визуализация (ООП) ==========
class GradeVisualizer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        sns.set_theme(style="whitegrid")
        self._load_data()

    def _load_data(self):
        if os.path.exists(self.file_path):
            self.df = pd.read_csv(self.file_path)
            print(f"\n[INFO] Данные загружены для визуализации из '{self.file_path}'")

    def plot_boxplot(self, n_subjects=5, save_path='grades_boxplot.png'):
        if self.df is None: return

        # Берем уникальные предметы
        subjects = self.df['subject_id'].unique()[:n_subjects]
        subset = self.df[self.df['subject_id'].isin(subjects)]

        plt.figure(figsize=(10, 6))
        # Исправлено: добавили hue и legend=False для тишины в консоли
        sns.boxplot(
            x='subject_id',
            y='grade',
            data=subset,
            palette='Set3',
            hue='subject_id',
            legend=False
        )
        plt.title(f'Задание 13: Распределение оценок (топ-{n_subjects} предметов)')
        plt.savefig(save_path, dpi=300)
        plt.show()
        plt.close()
        print(f"✅ График Boxplot сохранен: {save_path}")

    def plot_histogram(self, save_path='grades_hist.png'):
        if self.df is None: return
        plt.figure(figsize=(8, 5))
        sns.histplot(self.df['grade'], bins=10, kde=True, color='skyblue')
        plt.title('Задание 13: Общая гистограмма оценок')
        plt.savefig(save_path, dpi=300)
        plt.show()
        plt.close()
        print(f"✅ Гистограмма сохранена: {save_path}")


# ============================================================
# ГЛАВНЫЙ БЛОК ЗАПУСКА (MAIN)
# ============================================================
if __name__ == "__main__":
    # 1. Генерация данных (9)
    generator = FakeGradesGenerator("fake_grades.csv")
    generator.run()

    # 2. Создание коррелированных данных (10)
    correlation = GradesCorrelation("fake_grades.csv", "fake_grades_v2.csv")
    correlation.run()

    # 3. Валидация (11)
    validator = GradesValidator("fake_grades.csv")
    validator.run()

    # 4. Анализ (12)
    analyzer = GradesAnalyzer("fake_grades.csv")
    analyzer.run()

    # 5. Визуализация (13)
    print("\n" + "=" * 40)
    print("ВЫПОЛНЕНИЕ ВИЗУАЛИЗАЦИИ")
    print("=" * 40)
    visualizer = GradeVisualizer("fake_grades.csv")
    visualizer.plot_boxplot(n_subjects=5)
    visualizer.plot_histogram()

    print("\n✅ Весь проект (задания 9-13) выполнен успешно!")