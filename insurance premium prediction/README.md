# Insurance Premium Prediction API

A machine-learning API built with **FastAPI** to predict an insurance premium category from a user's demographic, lifestyle, income, and location-related information.

## Features

- REST API built with FastAPI
- Input validation with Pydantic
- Derived features such as BMI, age group, lifestyle risk, and city tier
- Prediction probabilities and confidence score from the trained model
- Health-check endpoint
- Docker configuration for containerized deployment

## Project Structure

```text
insurance premium prediction/
├── app.py
├── requirements.txt
├── Dockerfile
├── README.md
├── config/
│   └── city_tier.py
├── model/
│   ├── predict.py
│   └── model.pkl
└── Schema/
    ├── user_input.py
    └── prediction_response.py
```

> **Model file required:** Make sure the trained model is available at `model/model.pkl`. The API loads this file when the prediction module is imported.

## Requirements

- Python 3.10 or newer (Python 3.11 recommended)
- pip
- The trained `model/model.pkl` file

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/jaypanchal1706/Projects-With-FastAPI.git
cd Projects-With-FastAPI
cd "insurance premium prediction"
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bat
.venv\Scripts\activate.bat
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the API

```bash
uvicorn app:app --reload
```

The API will be available at:

- Home: http://127.0.0.1:8000/
- Health check: http://127.0.0.1:8000/health
- Interactive Swagger docs: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/` | Welcome message |
| GET | `/health` | API status, model version, and model-loaded status |
| POST | `/predict` | Predict an insurance premium category |

### Example prediction request

Send a JSON request to `POST /predict`:

```json
{
  "age": 30,
  "weight": 70,
  "height": 1.75,
  "income_lpa": 8.5,
  "smoker": false,
  "city": "Ahmedabad",
  "occupation": "private_job"
}
```

The valid occupation values are:

- `retired`
- `freelancer`
- `student`
- `government_job`
- `business_owner`
- `unemployed`
- `private_job`

The API schema derives BMI, age group, lifestyle risk, and city tier from the submitted values.

## Docker

Build the image from this project directory:

```bash
docker build -t insurance-premium-api .
```

Run the container:

```bash
docker run --rm -p 8000:8000 insurance-premium-api
```

Then open http://127.0.0.1:8000/docs.

## Notes

- The model file must be compatible with the scikit-learn version installed in the environment.
- Only load pickle model files from trusted sources.
- Do not commit virtual environments, cache files, credentials, or secrets.
- For deployment, configure dependency versions and environment settings for your target platform.

## Tech Stack

**Python · FastAPI · Pydantic · Pandas · Scikit-learn · Docker**
