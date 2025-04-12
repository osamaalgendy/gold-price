from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import requests_cache
import os
from dotenv import load_dotenv
from requests.structures import CaseInsensitiveDict

# 1. Load environment variables
load_dotenv()

# 2. Enable caching (12 hours)
requests_cache.install_cache("gold_cache", expire_after=43200)

# 3. Create FastAPI app
app = FastAPI()

# 4. Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. Get API key
API_KEY = os.getenv("METALS_DEV_API_KEY")


# 6. Endpoint to get gold price
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
            "price": round(price, 2),
            "currency": currency.upper(),
            "unit": unit.lower(),
        }

    except Exception as e:
        return {"error": str(e)}
