### detection.py
* **Pydantic**: A library that helps define and validate data (like forms or JSON). It automatically checks if the input is correct (e.g., URL is a string).
* **BaseModel**: The base class from Pydantic used to create your own data models. It makes input/output clean and validated.
* **URLRequest** (class): Defines what data the user must send when calling the API (here, just a url field). It acts as the input format.
* **PredictionResponse** (class): Defines what data the API will return (url, is_phishing, confidence, message). It acts as the output format and shows clear structure in Swagger UI.
* **@router.post("/predict")**: This creates a new API endpoint.
* POST means it receives data from the user (not just reading).
* /predict is the URL path.
The function below runs when someone calls this endpoint.