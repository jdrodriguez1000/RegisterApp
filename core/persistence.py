import json
from pathlib import Path

class Persistence:
    _file_path = Path(__file__).resolve().parent.parent / "configs" / "app_settings.json"

    @classmethod
    def set(cls, key, value):
        data = cls._load_all()
        data[key] = value
        cls._save_all(data)

    @classmethod
    def get(cls, key, default=None):
        data = cls._load_all()
        return data.get(key, default)

    @classmethod
    def _load_all(cls):
        if not cls._file_path.exists():
            return {}
        try:
            return json.loads(cls._file_path.read_text(encoding="utf-8"))
        except:
            return {}

    @classmethod
    def _save_all(cls, data):
        cls._file_path.parent.mkdir(parents=True, exist_ok=True)
        cls._file_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
