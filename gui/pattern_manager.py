import json
import os
from pathlib import Path

# --- Patterns prédéfinis ---
PATTERNS = {
    "Glider": [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
    "Blinker": [(1, 0), (1, 1), (1, 2)],
    "Toad": [(1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2)],
    "LWSS": [(0,1),(0,2),(1,0),(1,3),(2,0),(2,3),(3,1),(3,2)],
}

class PatternManager:
    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)

    def get_builtin_patterns(self):
        return list(PATTERNS.keys())

    def get_builtin_pattern(self, name):
        return PATTERNS.get(name, [])

    def save_pattern(self, coords, filename):
        path = self.data_dir / filename
        with open(path, "w") as f:
            json.dump(coords, f)

    def load_pattern(self, filename):
        path = self.data_dir / filename
        if path.exists():
            with open(path, "r") as f:
                return json.load(f)
        return []

    def list_saved_patterns(self):
        return [f.name for f in self.data_dir.glob("*.json")]
