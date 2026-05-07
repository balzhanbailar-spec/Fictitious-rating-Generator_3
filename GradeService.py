from fastapi import FastAPI
import pandas as pd
import numpy as np
import os
import uvicorn
app = FastAPI()
class GradeService:
    def __init__(self, seed: int, n_rows: int):
        self.seed = seed
        self.n_rows = n_rows
        self.filename = f"grades_seed_{seed}.csv"
        self.df = None
    def generate_and_save(self):
        rng = np.random.default_rng(self.seed)
        data = {
            'student_id': rng.integers(1, 101, size=self.n_rows),
            'subject_id': rng.integers(1, 11, size=self.n_rows),
            'grade': rng.uniform(2, 5, size=self.n_rows).round(2)
        }
        self.df = pd.DataFrame(data)
        self.df.to_csv(self.filename, index=False)
        return self.filename
    def get_metadata(self):
        if self.df is None: self.generate_and_save()
        return {
            "status": "success",
            "file_info": {"name": self.filename, "path": os.path.abspath(self.filename)},
            "parameters": {"seed": self.seed, "n_rows": self.n_rows},
            "summary": {"mean_grade": float(self.df['grade'].mean().round(2))}
        }
@app.get("/")
def get_grades(seed: int = 42, n_rows: int = 10):
    service = GradeService(seed, n_rows)
    return service.get_metadata()
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)