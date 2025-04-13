from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import requests_cache
import os
from dotenv import load_dotenv
from requests.structures import CaseInsensitiveDict

# Load environment variables
load_dotenv()

# Enable caching (12 hours)
requests_cache.install_cache("gold_cache", expire_after=43200)

# Create FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get API key
API_KEY = os.getenv("METALS_API_KEY")


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on the cloud!",
    "developer": "osama algendy",
    "contact me at":"osamaalgendy@gmail.com"}


# Endpoint to get gold price
@app.get("/gold-price")
def get_gold_price(currency: str = "SAR", unit: str = "g"):
    if not API_KEY:
        return {"error": "API key not found in environment variables."}

    url = (
        f"https://api.metals.dev/v1/latest"
        f"?api_key={API_KEY}&currency={currency.upper()}&unit={unit.lower()}"
    )

    # Use proper headers as per official docs
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if response.status_code != 200:
            return {"error": data.get("error", "Failed to fetch price.")}

        price = data["metals"].get("gold")

        if price is None:
            return {"error": "Gold price not available."}

        return {
            "price 24 karat": round(price, 2), # price in 24 karat
            "price 21 karat": round(price * 21/24, 2), # price in 21 karat
            "price 18 karat": round(price * 18/24, 2), # price in 18 karat
            "currency": currency.upper(),
            "unit": unit.lower(),
        }

    except Exception as e:
        return {"error": str(e)}
