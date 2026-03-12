import os
import httpx
from typing import Dict, Any
from datetime import date
import calendar
from dotenv import load_dotenv

load_dotenv()

class FireflyService:
    def __init__(self):
        # Allow connecting via HTTP to the internal docker network, strip trailing slash
        self.base_url = os.getenv("FIREFLY_URL", "http://firefly_iii:8080").rstrip("/")
        self.pat = os.getenv("FIREFLY_PAT", "")
        self.headers = {
            "Authorization": f"Bearer {self.pat}",
            "Accept": "application/json"
        }

    async def get_summary(self) -> Dict[str, Any]:
        """
        Fetches the summary from Firefly III for the current month
        and calculates Income, Expenses, and Balance.
        """
        today = date.today()
        _, last_day = calendar.monthrange(today.year, today.month)
        start_date = today.replace(day=1).strftime("%Y-%m-%d")
        end_date = today.replace(day=last_day).strftime("%Y-%m-%d")

        url = f"{self.base_url}/api/v1/summary/basic?start={start_date}&end={end_date}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    url,
                    headers=self.headers,
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                
                income = 0.0
                expenses = 0.0
                
                # Parse the response data from Firefly III summary
                for key_group in data.keys():
                    # Format varies depending on the specific user settings, 
                    # but usually there are array groups or specific keys.
                    # We will loop through the top level array if it's a list.
                    pass

                # If the response is a list or dictionary with 'data'
                items = data if isinstance(data, list) else data.get('data', [])
                if isinstance(data, dict) and not items:
                    # Some versions return the dictionary directly keyed by properties
                    items = [ { "key": k, "value": v } for k, v in data.items() ]

                # Actually, Firefly III /api/v1/summary/basic usually returns a dictionary 
                # where the keys might be user-defined or standard. Let's handle common structures:
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    key_lower = item.get('key', '').lower()
                    
                    # Some properties might be nested in 'value' or 'amount'
                    val = item.get('value', 0)
                    amount = float(val) if not isinstance(val, dict) else float(val.get('amount', val.get('value', 0)))
                    
                    if 'earned' in key_lower or 'income' in key_lower:
                        income += amount
                    elif 'spent' in key_lower or 'expense' in key_lower or 'paid' in key_lower:
                        expenses += abs(amount)  # ensure expense is positive for the formula

                balance = income - expenses
                
                return {
                    "income": round(income, 2),
                    "expenses": round(expenses, 2),
                    "balance": round(balance, 2),
                    "period": {
                        "start": start_date,
                        "end": end_date
                    }
                }
            except Exception as e:
                # In case of an error we return a consistent object but with the error string
                return {
                    "error": f"Failed to connect to Firefly III: {str(e)}",
                    "income": 0,
                    "expenses": 0,
                    "balance": 0,
                    "period": {
                        "start": start_date,
                        "end": end_date
                    }
                }

    async def get_raw_summary(self) -> Dict[str, Any]:
        today = date.today()
        _, last_day = calendar.monthrange(today.year, today.month)
        start_date = today.replace(day=1).strftime("%Y-%m-%d")
        end_date = today.replace(day=last_day).strftime("%Y-%m-%d")

        url = f"{self.base_url}/api/v1/summary/basic?start={start_date}&end={end_date}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers, timeout=10.0)
                response.raise_for_status()
                return {"url": url, "data": response.json()}
            except Exception as e:
                return {"error": str(e)}
