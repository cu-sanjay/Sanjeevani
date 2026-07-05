import csv
import os

DATA_DIR = os.path.join(
    os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "data"
)


class MedicineCatalog:
    def __init__(self):
        self.medicines = []
        self._load()

    def _load(self):
        path = os.path.join(DATA_DIR, "kaggle_medicine_details.csv")
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                name = (row.get("Medicine Name") or "").strip()
                if not name:
                    continue
                try:
                    excellent = float(row.get("Excellent Review %") or 0)
                    average = float(row.get("Average Review %") or 0)
                    poor = float(row.get("Poor Review %") or 0)
                except ValueError:
                    excellent = average = poor = 0

                self.medicines.append(
                    {
                        "id": i,
                        "name": name,
                        "composition": (row.get("Composition") or "").strip(),
                        "uses": (row.get("Uses") or "").strip(),
                        "side_effects": (row.get("Side_effects") or "").strip(),
                        "image": (row.get("Image URL") or "").strip(),
                        "manufacturer": (row.get("Manufacturer") or "").strip(),
                        "excellent_review": excellent,
                        "average_review": average,
                        "poor_review": poor,
                    }
                )

    def search(self, query, limit=30):
        query = (query or "").strip().lower()
        if not query:
            return self.medicines[:limit]

        terms = query.split()
        scored = []
        for med in self.medicines:
            haystack = " ".join(
                [med["name"], med["composition"], med["uses"]]
            ).lower()
            score = 0
            for term in terms:
                if term in med["name"].lower():
                    score += 5
                if term in med["composition"].lower():
                    score += 3
                if term in med["uses"].lower():
                    score += 2
                if term in haystack:
                    score += 1
            if score > 0:
                scored.append((score, med))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [m for _, m in scored[:limit]]

    def get_by_id(self, med_id):
        for med in self.medicines:
            if med["id"] == med_id:
                return med
        return None


_catalog_instance = None


def get_catalog():
    global _catalog_instance
    if _catalog_instance is None:
        _catalog_instance = MedicineCatalog()
    return _catalog_instance
