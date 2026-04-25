import csv
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


# ========== 9. FakeGradesGenerator ==========
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


# ========== 10. GradesCorrelation ==========
class GradesCorrelation:
    def __init__(self, input_file, output_file, seed=42):
        self.input_file = input_file
        self.output_file = output_file
        self.rng = np.random.default_rng(seed)

    def process(self):
        if not os.path.exists(self.input_file): return
        with open(self.input_file, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        output_rows = []
        for row in rows:
            sid, subid, g1 = row['student_id'], row['subject_id'], float(row['grade'])
            noise = self.rng.normal(0, 0.3)
            grade2 = np.clip(0.7 * g1 + noise, 2.0, 5.0)
            output_rows.append([sid, subid, g1, round(grade2, 2)])

        with open(self.output_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["student_id", "subject_id", "grade1", "grade2"])
            writer.writerows(output_rows)

    def run(self):
        self.process()
        print(f"=== Задание 10: Файл '{self.output_file}' создан ===")


# ========== 11. GradesValidator ==========
class GradesValidator:
    def __init__(self, filename):
        self.filename = filename

    def run(self):
        print("\n=== Задание 11: Валидация ===")
        df = pd.read_csv(self.filename)
        print(f"✅ Файл '{self.filename}' загружен.")
        if (df['grade'] < 2).any() or (df['grade'] > 5).any():
            print("❌ Ошибка: оценки вне диапазона!")
        else:
            print("✅ Все оценки в норме.")
        print(df['grade'].describe())


# ========== 12. GradesAnalyzer ==========
class GradesAnalyzer:
    def __init__(self, filename):
        self.filename = filename

    def run(self):
        print("\n=== Задание 12: Анализ ===")
        df = pd.read_csv(self.filename)
        means = df.groupby('subject_id')['grade'].mean().sort_values(ascending=False)
        print(means.reset_index())


# ========== 13. GradeVisualizer (ИСПРАВЛЕНО) ==========
class GradeVisualizer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        sns.set_theme(style="whitegrid")
        self._load_data()

    def _load_data(self):
        if os.path.exists(self.file_path):
            self.df = pd.read_csv(self.file_path)

    def plot_top_subjects_boxplot(self, n_subjects=5, save_path='grades_boxplot.png'):
        if self.df is None: return
        selected = self.df['subject_id'].unique()[:n_subjects]
        subset = self.df[self.df['subject_id'].isin(selected)]

        plt.figure(figsize=(10, 6))
        # ИСПРАВЛЕНИЕ: Добавлен hue и legend=False для устранения FutureWarning
        sns.boxplot(
            x='subject_id',
            y='grade',
            data=subset,
            palette='Set3',
            hue='subject_id',
            legend=False
        )

        plt.title(f'Задача 13: Распределение оценок ({len(selected)} предметов)')
        plt.savefig(save_path, dpi=300)
        plt.show()
        plt.close()
        print(f"✅ Boxplot сохранен: {save_path}")

    def plot_grade_histogram(self, save_path='grades_hist.png'):
        if self.df is None: return
        plt.figure(figsize=(8, 5))
        sns.histplot(self.df['grade'], bins=10, kde=True, color='skyblue')
        plt.title('Задача 13: Общее распределение оценок')
        plt.savefig(save_path, dpi=300)
        plt.show()
        plt.close()
        print(f"✅ Гистограмма сохранена: {save_path}")


# ========== ГЛАВНЫЙ ЗАПУСК ==========
if __name__ == "__main__":
    # Выполняем все задачи по порядку
    FakeGradesGenerator("fake_grades.csv").run()
    GradesCorrelation("fake_grades.csv", "fake_grades_v2.csv").run()
    GradesValidator("fake_grades.csv").run()
    GradesAnalyzer("fake_grades.csv").run()

    print("\n" + "=" * 35)
    print("ВЫПОЛНЕНИЕ ЗАДАНИЯ 13 (ВИЗУАЛИЗАЦИЯ)")
    print("=" * 35)

    vis = GradeVisualizer("fake_grades.csv")
    vis.plot_top_subjects_boxplot()
    vis.plot_grade_histogram()

    print("\n✅ Скрипт успешно завершил работу.")