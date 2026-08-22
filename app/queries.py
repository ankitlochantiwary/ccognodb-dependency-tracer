from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / 'queries'


def load_query(name: str) -> str:
    return (BASE / name).read_text(encoding='utf-8')
