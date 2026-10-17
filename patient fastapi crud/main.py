from pathlib import Path
import json
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Patient CRUD API", version="1.0.0")

DATA_FILE = Path(__file__).with_name("patients.json")


class Patient(BaseModel):
    name: str = Field(..., min_length=1)
    city: str
    age: int = Field(..., ge=0, le=130)
    gender: str
    height: float = Field(..., gt=0, description="Height in metres")
    weight: float = Field(..., gt=0, description="Weight in kilograms")
    married: bool = False


class PatientUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    city: Optional[str] = None
    age: Optional[int] = Field(default=None, ge=0, le=130)
    gender: Optional[str] = None
    height: Optional[float] = Field(default=None, gt=0)
    weight: Optional[float] = Field(default=None, gt=0)
    married: Optional[bool] = None


def load_data() -> dict:
    """Load patient records from the JSON file."""
    if not DATA_FILE.exists():
        DATA_FILE.write_text("{}", encoding="utf-8")
        return {}

    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail="patients.json contains invalid JSON.") from exc

    if not isinstance(data, dict):
        raise HTTPException(status_code=500, detail="patients.json must contain a JSON object.")
    return data


def save_data(data: dict) -> None:
    """Persist patient records to the JSON file."""
    DATA_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")


@app.get("/")
def home():
    return {"message": "Patient CRUD API is running"}


@app.get("/view")
def view_all_patients():
    return load_data()


@app.get("/patient/{patient_id}")
def view_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient Not Found")
    return data[patient_id]


@app.post("/create/{patient_id}", status_code=201)
def create_patient(patient_id: str, patient: Patient):
    data = load_data()
    if patient_id in data:
        raise HTTPException(status_code=409, detail="Patient ID already exists")

    data[patient_id] = patient.model_dump()
    save_data(data)
    return {"message": "Patient created successfully", "patient_id": patient_id}


@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient Not Found")

    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    if not updated_patient_info:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    existing_patient_info = data[patient_id]
    existing_patient_info.update(updated_patient_info)

    # Validate the complete record before saving it.
    data[patient_id] = Patient(**existing_patient_info).model_dump()
    save_data(data)
    return {"message": "Patient updated successfully", "patient": data[patient_id]}


@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient Not Found")

    deleted_patient = data.pop(patient_id)
    save_data(data)
    return {"message": "Patient deleted successfully", "patient": deleted_patient}
