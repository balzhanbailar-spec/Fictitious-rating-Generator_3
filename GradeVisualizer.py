import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class GradeVisualizer:
    def __init__(self, file_path):
        """Инициализация класса и загрузка данных."""
        self.file_path = file_path
        self.df = None
        self._load_data()

    def _load_data(self):
        """Внутренний метод для загрузки CSV."""
        try:
            self.df = pd.read_csv(self.file_path)
            print(f"Файл {self.file_path} успешно загружен.")
        except FileNotFoundError:
            print("Ошибка: Файл не найден.")

    def plot_top_subjects_boxplot(self, n_subjects=5, save_path='grades_boxplot.png'):
        """Построение Boxplot для топ-N предметов по количеству оценок или ID."""
        if self.df is None:
            return

        # Выбираем первые 5 уникальных предметов для визуализации
        selected_subjects = self.df['subject_id'].unique()[:n_subjects]
        subset = self.df[self.df['subject_id'].isin(selected_subjects)]

        plt.figure(figsize=(10, 6))
        sns.boxplot(x='subject_id', y='grade', data=subset, palette='Set3')

        plt.title(f'Распределение оценок для {len(selected_subjects)} предметов')
        plt.xlabel('ID Предмета')
        plt.ylabel('Оценка')
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        plt.savefig(save_path)
        plt.show()
        print(f"График Boxplot сохранен как {save_path}")

    def plot_grade_histogram(self, save_path='grades_hist.png'):
        """Построение гистограммы распределения всех оценок."""
        if self.df is None:
            return

        plt.figure(figsize=(8, 5))
        sns.histplot(self.df['grade'], bins=10, kde=True, color='skyblue')

        plt.title('Общее распределение оценок')
        plt.xlabel('Оценка')
        plt.ylabel('Частота')

        plt.savefig(save_path)
        plt.show()
        print(f"Гистограмма сохранена как {save_path}")


# Пример использования:
if __name__ == "__main__":
    # Предполагаем, что файл fake_grades.csv был создан в задачах 9-10
    visualizer = GradeVisualizer('fake_grades.csv')

    # Визуализируем распределение по предметам (Boxplot)
    visualizer.plot_top_subjects_boxplot(n_subjects=5)

    # Визуализируем общую гистограмму
    visualizer.plot_grade_histogram()