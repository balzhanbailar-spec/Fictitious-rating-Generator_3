import csv
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


# ========== 9. FakeGradesGenerator (Генерация данных) ==========
class FakeGradesGenerator:
    def __init__(self, filename, seed=42):
        self.filename = filename
        self.seed = seed
        self.num_students = 10
        self.num_subjects = 5

    def generate(self):
        random.seed(self.seed)
        try:
            with open(self.filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["student_id", "subject_id", "grade"])
                for student_id in range(1, self.num_students + 1):
                    for subject_id in range(1, self.num_subjects + 1):
                        grade = random.randint(2, 5)
                        writer.writerow([student_id, subject_id, grade])
            print(f"=== Задание 9: Файл '{self.filename}' успешно создан ===")
        except Exception as e:
            print(f"Ошибка при создании файла: {e}")

    def run(self):
        self.generate()


# ========== 10. GradesCorrelation (Работа с шумом и корреляцией) ==========
class GradesCorrelation:
    def __init__(self, input_file, output_file, seed=42):
        self.input_file = input_file
        self.output_file = output_file
        self.rng = np.random.default_rng(seed)

    def process(self):
        if not os.path.exists(self.input_file):
            print(f"Ошибка: Входной файл {self.input_file} не найден.")
            return

        df_in = pd.read_csv(self.input_file)
        # Создаем коррелированную оценку: 70% от оригинала + случайный шум
        noise = self.rng.normal(0, 0.3, size=len(df_in))
        df_in['grade2'] = (0.7 * df_in['grade'] + noise).clip(2.0, 5.0).round(2)

        df_in.to_csv(self.output_file, index=False)
        print(f"=== Задание 10: Файл '{self.output_file}' с корреляцией создан ===")

    def run(self):
        self.process()


# ========== 11. GradesValidator (Валидация Pandas) ==========
class GradesValidator:
    def __init__(self, filename):
        self.filename = filename

    def run(self):
        print("\n=== Задание 11: Валидация ===")
        try:
            df = pd.read_csv(self.filename)
            print(f"✅ Файл '{self.filename}' загружен.")

            # Проверка типов и диапазона
            if not np.issubdtype(df['grade'].dtype, np.number):
                print("❌ Ошибка: колонка 'grade' не является числовой!")
            elif (df['grade'] < 2).any() or (df['grade'] > 5).any():
                print("❌ Ошибка: Обнаружены оценки вне диапазона [2, 5]!")
            else:
                print("✅ Валидация пройдена: все оценки в норме.")

            print("\nКраткая статистика:")
            print(df['grade'].describe())
        except Exception as e:
            print(f"Ошибка при валидации: {e}")


# ========== 12. GradesAnalyzer (Анализ средних баллов) ==========
class GradesAnalyzer:
    def __init__(self, filename):
        self.filename = filename

    def run(self):
        print("\n=== Задание 12: Анализ средних баллов ===")
        df = pd.read_csv(self.filename)
        # Группировка по предметам и сортировка
        means = df.groupby('subject_id')['grade'].mean().sort_values(ascending=False)
        print("Средние оценки по ID предметов:")
        print(means.reset_index().to_string(index=False))


# ========== 13. GradeVisualizer (Визуализация ООП) ==========
class GradeVisualizer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        sns.set_theme(style="whitegrid")
        self._load_data()

    def _load_data(self):
        if os.path.exists(self.file_path):
            self.df = pd.read_csv(self.file_path)
            print(f"\n[INFO] Данные из '{self.file_path}' подгружены для графиков.")

    def plot_top_subjects_boxplot(self, n_subjects=5, save_path='grades_boxplot.png'):
        if self.df is None: return

        # Берем первые N уникальных предметов
        selected_ids = self.df['subject_id'].unique()[:n_subjects]
        subset = self.df[self.df['subject_id'].isin(selected_ids)]

        plt.figure(figsize=(10, 6))
        # Исправленный вызов без предупреждений (hue задан явно)
        sns.boxplot(
            x='subject_id',
            y='grade',
            data=subset,
            palette='Set3',
            hue='subject_id',
            legend=False
        )

        plt.title(f'Задача 13: Распределение оценок (топ-{n_subjects} предметов)')
        plt.xlabel('ID Предмета')
        plt.ylabel('Оценка')
        plt.savefig(save_path, dpi=300)
        plt.show()
        plt.close()
        print(f"✅ Boxplot сохранен: {save_path}")

    def plot_grade_histogram(self, save_path='grades_hist.png'):
        if self.df is None: return

        plt.figure(figsize=(8, 5))
        sns.histplot(self.df['grade'], bins=10, kde=True, color='skyblue')
        plt.title('Задача 13: Общее распределение оценок (Histogram)')
        plt.xlabel('Оценка')
        plt.ylabel('Частота')
        plt.savefig(save_path, dpi=300)
        plt.show()
        plt.close()
        print(f"✅ Гистограмма сохранена: {save_path}")


# ============================================================
# ГЛАВНЫЙ БЛОК УПРАВЛЕНИЯ (MAIN)
# ============================================================
if __name__ == "__main__":
    # Названия файлов
    base_file = "fake_grades.csv"
    corr_file = "fake_grades_v2.csv"

    # Шаг 9: Генерация
    FakeGradesGenerator(base_file).run()

    # Шаг 10: Корреляция
    GradesCorrelation(base_file, corr_file).run()

    # Шаг 11: Валидация
    validator = GradesValidator(base_file)
    validator.run()

    # Шаг 12: Анализ
    analyzer = GradesAnalyzer(base_file)
    analyzer.run()

    # Шаг 13: Визуализация
    print("\n" + "=" * 40)
    print("ЗАПУСК ВИЗУАЛИЗАЦИИ ДАННЫХ")
    print("=" * 40)

    vis = GradeVisualizer(base_file)
    vis.plot_top_subjects_boxplot(n_subjects=5)
    vis.plot_grade_histogram()

    print("\n✅ Весь цикл задач (9-13) выполнен успешно.")