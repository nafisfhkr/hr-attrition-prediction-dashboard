
from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_MODEL_PATH = BASE_DIR / "model" / "attrition_model.pkl"
DROP_COLUMNS = ["EmployeeId", "EmployeeCount", "Over18", "StandardHours"]


def predict_file(input_path: Path, model_path: Path) -> pd.DataFrame:
    """Load employee records and return predictions with attrition probabilities."""
    data = pd.read_csv(input_path)
    model = joblib.load(model_path)

    features = data.drop(columns=["Attrition", *DROP_COLUMNS], errors="ignore")
    expected_features = getattr(model, "feature_names_in_", None)
    if expected_features is not None:
        missing = sorted(set(expected_features) - set(features.columns))
        if missing:
            raise ValueError(
                "Input CSV is missing model features: " + ", ".join(missing)
            )
        features = features.loc[:, expected_features]

    predictions = model.predict(features).astype(int)
    result = data.copy()
    result["Prediction"] = predictions
    result["PredictionLabel"] = result["Prediction"].map(
        {0: "Tidak Attrition", 1: "Attrition"}
    )

    if hasattr(model, "predict_proba"):
        result["AttritionProbability"] = model.predict_proba(features)[:, 1]

    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Input employee CSV")
    parser.add_argument(
        "--model", type=Path, default=DEFAULT_MODEL_PATH, help="Saved model path"
    )
    parser.add_argument("--output", type=Path, help="Optional output CSV path")
    args = parser.parse_args()

    if not args.input.exists():
        parser.error(f"Input file not found: {args.input}")
    if not args.model.exists():
        parser.error(f"Model file not found: {args.model}")

    result = predict_file(args.input, args.model)
    if args.output:
        result.to_csv(args.output, index=False)
        print(f"Predictions saved to {args.output}")
    else:
        output_columns = ["Prediction", "PredictionLabel"]
        if "AttritionProbability" in result:
            output_columns.append("AttritionProbability")
        print(result[output_columns].to_string(index=False))


if __name__ == "__main__":
    main()
