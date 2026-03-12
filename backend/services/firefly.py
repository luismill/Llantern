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

    def _parse_summary_data(self, data: Any) -> tuple[float, float, float]:
        """Parses Firefly III summary JSON and returns (income, expenses, balance)"""
        income = 0.0
        expenses = 0.0

        items = []
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, dict) and ('earned' in v or 'spent' in v or 'net-worth' in v):
                    items.append(v)
                else:
                    items.append({"key": k, "value": v})
        elif isinstance(data, list):
            items = data

        for item in items:
            if not isinstance(item, dict):
                continue

            # Format 1: Direct keys
            for key, val in item.items():
                key_lower = key.lower()
                amount = 0.0
                if isinstance(val, dict):
                    amount_raw = val.get('monetary_value', val.get('amount', val.get('value', 0)))
                    try:
                        amount = float(amount_raw)
                    except (ValueError, TypeError):
                        amount = 0.0
                elif isinstance(val, (int, float, str)):
                    try:
                        amount = float(val)
                    except (ValueError, TypeError):
                        amount = 0.0

                if 'earned' in key_lower or 'income' in key_lower:
                    income += amount
                elif 'spent' in key_lower or 'expense' in key_lower or 'paid' in key_lower:
                    expenses += abs(amount)

            # Format 2: {"key": "earned", "value": ...}
            key_attr = item.get('key', '').lower()
            if key_attr:
                val_attr = item.get('monetary_value', item.get('amount', item.get('value', 0)))
                amount = 0.0
                if isinstance(val_attr, dict):
                    amount_raw = val_attr.get('monetary_value', val_attr.get('amount', val_attr.get('value', 0)))
                    try:
                        amount = float(amount_raw)
                    except (ValueError, TypeError):
                        amount = 0.0
                else:
                    try:
                        amount = float(val_attr)
                    except (ValueError, TypeError):
                        amount = 0.0
                
                if 'earned' in key_attr or 'income' in key_attr:
                    income += amount
                elif 'spent' in key_attr or 'expense' in key_attr or 'paid' in key_attr:
                    expenses += abs(amount)

        balance = income - expenses
        return round(income, 2), round(expenses, 2), round(balance, 2)

    async def get_summary(self, target_date: date = None) -> Dict[str, Any]:
        """
        Fetches the summary from Firefly III for a specific month (defaults to current)
        """
        if target_date is None:
            target_date = date.today()
            
        _, last_day = calendar.monthrange(target_date.year, target_date.month)
        start_date = target_date.replace(day=1).strftime("%Y-%m-%d")
        end_date = target_date.replace(day=last_day).strftime("%Y-%m-%d")

        url = f"{self.base_url}/api/v1/summary/basic?start={start_date}&end={end_date}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                income, expenses, balance = self._parse_summary_data(data)
                
                return {
                    "income": income,
                    "expenses": expenses,
                    "balance": balance,
                    "period": {
                        "start": start_date,
                        "end": end_date
                    }
                }
            except Exception as e:
                return {
                    "error": f"Failed to connect to Firefly III: {str(e)}",
                    "income": 0, "expenses": 0, "balance": 0,
                    "period": {"start": start_date, "end": end_date}
                }

    async def get_history(self, months: int = 6) -> list[Dict[str, Any]]:
        """
        Fetches historical data by gathering summaries for the past N months.
        """
        history = []
        today = date.today()
        
        # Calculate trailing N months
        for i in range(months - 1, -1, -1):
            y = today.year
            m = today.month - i
            while m <= 0:
                m += 12
                y -= 1
            
            target = date(y, m, 1)
            summary = await self.get_summary(target)
            
            # Formatting as 'YYYY-MM' for the frontend graph labels
            label = target.strftime("%Y-%m")
            
            history.append({
                "label": label,
                "income": summary.get("income", 0),
                "expenses": summary.get("expenses", 0),
                "balance": summary.get("balance", 0)
            })
            
        return history

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
