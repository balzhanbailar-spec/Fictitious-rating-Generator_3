import csv
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json
from pathlib import Path

# 1. Генерация (универсальная)

class GradeGenerator:
    def __init__(self, seed: int, n_rows: int, file_name="fake_grades.csv"):
        self.seed = seed
        self.n_rows = n_rows
        self.file_name = file_name
        self.rng = np.random.default_rng(seed)

    def generate(self):
        df = pd.DataFrame({
            "student_id": self.rng.integers(1, 11, self.n_rows),
            "subject_id": self.rng.integers(1, 6, self.n_rows),
            "grade": self.rng.integers(2, 6, self.n_rows)
        })

        df.to_csv(self.file_name, index=False)
        return df


# 2. Корреляция (задание 10)

class GradesCorrelation:
    def __init__(self, seed=42):
        self.rng = np.random.default_rng(seed)

    def add(self, df: pd.DataFrame):
        noise = self.rng.normal(0, 0.3, len(df))
        df["grade2"] = np.clip(0.7 * df["grade"] + noise, 2, 5)
        return df

# 3. Валидация (задание 11)

class GradesValidator:
    def validate(self, df: pd.DataFrame):
        print("\n=== Валидация ===")
        print(df.dtypes)

        valid = df["grade"].between(2, 5).all()

        if valid:
            print("✅ Оценки корректны")
        else:
            print("❌ Ошибка диапазона")

        return valid

# 4. Анализ (задание 12)

class GradesAnalyzer:
    def analyze(self, df: pd.DataFrame):
        print("\n=== Средние по предметам ===")
        means = df.groupby("subject_id")["grade"].mean().sort_values(ascending=False)
        print(means)
        return means

# 5. Визуализация (задание 13)

class GradeVisualizer:
    def plot(self, df: pd.DataFrame):
        sns.set_theme(style="whitegrid")

        plt.figure()
        sns.boxplot(x="subject_id", y="grade", data=df)
        plt.savefig("boxplot.png")
        plt.close()

        plt.figure()
        sns.histplot(df["grade"], bins=10, kde=True)
        plt.savefig("hist.png")
        plt.close()

        print("✅ Графики сохранены")

# 6. СЕРВИС (объединяет 9–13)

class GradeService:
    def __init__(self, seed: int, n_rows: int):
        self.seed = seed
        self.n_rows = n_rows
        self.file_name = "fake_grades.csv"

        self.generator = GradeGenerator(seed, n_rows, self.file_name)
        self.correlation = GradesCorrelation(seed)
        self.validator = GradesValidator()
        self.analyzer = GradesAnalyzer()
        self.visualizer = GradeVisualizer()

    def run_pipeline(self):
        df = self.generator.generate()
        df = self.correlation.add(df)

        df.to_csv(self.file_name, index=False)

        valid = self.validator.validate(df)
        self.analyzer.analyze(df)
        self.visualizer.plot(df)

        return df, valid

    def get_metadata(self):
        df, valid = self.run_pipeline()

        return {
            "seed": self.seed,
            "n_rows": self.n_rows,
            "file": self.file_name,
            "path": str(Path(self.file_name).absolute()),
            "valid": bool(valid),
            "columns": list(df.columns)
        }


# 7. API (задание 14)

class GradeAPI:
    def get(self, seed: int, n_rows: int):
        service = GradeService(seed, n_rows)
        return service.get_metadata()
if __name__ == "__main__":

    print("=== Запуск заданий 9–13 ===")
    service = GradeService(seed=42, n_rows=50)
    result = service.get_metadata()

    print("\nJSON RESULT:")
    print(json.dumps(result, indent=4, ensure_ascii=False))

    print("\n=== Задание 14 (API имитация) ===")
    api = GradeAPI()
    response = api.get(seed=100, n_rows=20)

    print(json.dumps(response, indent=4, ensure_ascii=False))