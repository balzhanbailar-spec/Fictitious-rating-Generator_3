import numpy as np
import pandas as pd
import json
from pathlib import Path


class GradeGenerator:
    def __init__(self, seed: int, n_rows: int):
        self.seed = seed
        self.n_rows = n_rows
        self.rng = np.random.default_rng(seed)
        self.file_name = "fake_grades.csv"

    def generate(self):
        df = pd.DataFrame({
            "student_id": self.rng.integers(1, 101, self.n_rows),
            "subject_id": self.rng.integers(1, 11, self.n_rows),
            "grade": self.rng.integers(2, 6, self.n_rows)
        })

        df.to_csv(self.file_name, index=False)

        result = {
            "seed": self.seed,
            "n_rows": self.n_rows,
            "file_name": self.file_name,
            "path": str(Path(self.file_name).absolute())
        }

        return result


class GradeAPI:
    def get(self, seed: int, n_rows: int):
        generator = GradeGenerator(seed, n_rows)
        return generator.generate()


if __name__ == "__main__":
    api = GradeAPI()

    response = api.get(seed=42, n_rows=20)

    print(json.dumps(response, indent=4, ensure_ascii=False))