import csv
import numpy as np
import pandas as pd
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional
import os

class GradesGeneratorAPI:
    """
    Генерирует CSV-файл с оценками на основе seed и n_rows.
    Логика соответствует заданиям 9–10.
    """
    def __init__(self, seed: int, n_rows: int, output_dir: str = "."):
        self.seed = seed
        self.n_rows = n_rows
        self.output_dir = output_dir
        self.rng = np.random.default_rng(seed)
        self.filename = f"grades_seed{seed}_rows{n_rows}.csv"
        self.filepath = os.path.join(output_dir, self.filename)

    def generate(self):
        """Генерирует CSV-файл с колонками student_id, subject_id, grade."""
        with open(self.filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["student_id", "subject_id", "grade"])
            for _ in range(self.n_rows):
                student_id = self.rng.integers(1, 11)      # 1..10
                subject_id = self.rng.integers(1, 6)       # 1..5
                grade = self.rng.integers(2, 6)            # 2..5
                writer.writerow([student_id, subject_id, grade])
        return self.filepath

    def get_metadata(self):
        """Возвращает словарь с метаинформацией (аналогично требованиям JSON)."""
        return {
            "seed": self.seed,
            "n_rows": self.n_rows,
            "file_path": self.filepath,
            "columns": ["student_id", "subject_id", "grade"],
            "grade_range": [2, 5]
        }

app = FastAPI(title="Grades Generator API", description="GET endpoint for task 14")

class GenerateResponse(BaseModel):
    seed: int
    n_rows: int
    file_path: str
    columns: list
    grade_range: list
    status: str

@app.get("/generate", response_model=GenerateResponse)
async def generate_grades(
    seed: int = Query(42, description="Seed для генератора случайных чисел"),
    n_rows: int = Query(50, description="Количество строк в CSV")
):
    """
    GET-эндпоинт: генерирует CSV с оценками и возвращает JSON метаданных.
    Пример: /generate?seed=123&n_rows=100
    """
    # Создаём объект генератора
    generator = GradesGeneratorAPI(seed=seed, n_rows=n_rows)
    # Генерируем файл
    file_path = generator.generate()
    # Получаем метаданные
    metadata = generator.get_metadata()
    # Добавляем статус
    metadata["status"] = "success"
    return metadata

# ========== Для запуска сервера (если файл запущен напрямую) ==========
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)