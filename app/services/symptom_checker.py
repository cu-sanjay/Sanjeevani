import csv
import os
import re

DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "data")


def _clean(text):
    return re.sub(r"\s+", " ", text or "").strip().lower().replace(" ", "_")


class SymptomChecker:
    def __init__(self):
        self.disease_symptoms = {}
        self.all_symptoms = set()
        self.descriptions = {}
        self.precautions = {}
        self.severity = {}
        self._load()

    def _load(self):
        dataset_path = os.path.join(DATA_DIR, "dataset.csv")
        with open(dataset_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                if not row or not row[0].strip():
                    continue
                disease = row[0].strip()
                symptoms = set()
                for cell in row[1:]:
                    cell = _clean(cell)
                    if cell:
                        symptoms.add(cell)
                        self.all_symptoms.add(cell)
                if disease not in self.disease_symptoms:
                    self.disease_symptoms[disease] = set()
                self.disease_symptoms[disease].update(symptoms)

        desc_path = os.path.join(DATA_DIR, "symptom_Description.csv")
        with open(desc_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.descriptions[row["Disease"].strip()] = row["Description"].strip()

        prec_path = os.path.join(DATA_DIR, "symptom_precaution.csv")
        with open(prec_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                disease = row["Disease"].strip()
                precautions = [
                    row.get(f"Precaution_{i}", "").strip()
                    for i in range(1, 5)
                    if row.get(f"Precaution_{i}", "").strip()
                ]
                self.precautions[disease] = precautions

        sev_path = os.path.join(DATA_DIR, "Symptom-severity.csv")
        with open(sev_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                symptom = _clean(row["Symptom"])
                try:
                    self.severity[symptom] = int(row["weight"])
                except (ValueError, KeyError):
                    pass

    def symptom_list(self):
        return sorted(s.replace("_", " ") for s in self.all_symptoms)

    def check(self, selected_symptoms):
        selected = {_clean(s) for s in selected_symptoms if s.strip()}
        if not selected:
            return []

        results = []
        for disease, symptoms in self.disease_symptoms.items():
            matched = selected & symptoms
            if not matched:
                continue
            match_ratio = len(matched) / len(symptoms) if symptoms else 0
            coverage = len(matched) / len(selected) if selected else 0
            weight = sum(self.severity.get(s, 1) for s in matched)
            score = (match_ratio * 0.5 + coverage * 0.5) * 100

            results.append(
                {
                    "disease": disease,
                    "confidence": round(score, 1),
                    "matched_symptoms": sorted(m.replace("_", " ") for m in matched),
                    "missing_symptoms": sorted(
                        s.replace("_", " ") for s in (symptoms - selected)
                    ),
                    "description": self.descriptions.get(
                        disease, "No description available for this condition yet."
                    ),
                    "precautions": self.precautions.get(disease, []),
                    "severity_score": weight,
                }
            )

        results.sort(key=lambda r: r["confidence"], reverse=True)
        return results[:5]


_checker_instance = None


def get_checker():
    global _checker_instance
    if _checker_instance is None:
        _checker_instance = SymptomChecker()
    return _checker_instance
