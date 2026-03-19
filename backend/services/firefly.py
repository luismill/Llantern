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

    async def get_summary(self, target_date: date = None, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """
        Fetches the summary from Firefly III for a specific period.
        """
        if not start_date or not end_date:
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
            
            # Formatting as 'Mes YYYY' in Spanish
            meses_es = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
            label = f"{meses_es[target.month - 1]} {target.year}"
            
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

    async def get_transactions(self, 
                               start_date: str = None, 
                               end_date: str = None, 
                               uncategorized_only: bool = False,
                               category: str = None,
                               tag: str = None,
                               source: str = None,
                               destination: str = None,
                               account: str = None) -> list[Dict[str, Any]]:
        """
        Fetches transactions based on criteria, looping through all pages.
        Uses /api/v1/search ?query= 
        """
        import urllib.parse
        
        if not end_date:
            today = date.today()
            _, last_day = calendar.monthrange(today.year, today.month)
            end_date = today.replace(day=last_day).strftime("%Y-%m-%d")

        if not start_date:
            # Default to the first day of the PREVIOUS month
            today = date.today()
            m = today.month - 1
            y = today.year
            if m == 0:
                m = 12
                y -= 1
            start_date = date(y, m, 1).strftime("%Y-%m-%d")

        query_parts = [f"date_after:{start_date}", f"date_before:{end_date}"]
        
        if category:
            query_parts.append(f'category:"{category}"')
        if tag:
            query_parts.append(f'tag:"{tag}"')
        if source:
            query_parts.append(f'source_account:"{source}"')
        if destination:
            query_parts.append(f'destination_account:"{destination}"')
        if account:
            query_parts.append(f'account:"{account}"')
            
        search_query = " ".join(query_parts)
        encoded_query = urllib.parse.quote(search_query)
        
        base_search_url = f"{self.base_url}/api/v1/search/transactions?query={encoded_query}"
        
        transactions = []
        current_page = 1
        total_pages = 1 # Will be updated after first request
        
        async with httpx.AsyncClient() as client:
            try:
                while current_page <= total_pages:
                    url = f"{base_search_url}&page={current_page}"
                    response = await client.get(url, headers=self.headers, timeout=15.0)
                    response.raise_for_status()
                    json_resp = response.json()
                    
                    # Update total pages from the meta object
                    meta = json_resp.get('meta', {})
                    pagination = meta.get('pagination', {})
                    total_pages = pagination.get('total_pages', 1)
                    
                    data = json_resp.get('data', [])
                    
                    for item in data:
                        attrs = item.get('attributes', {})
                        if not attrs: continue
                        
                        sub_txs = attrs.get('transactions', [])
                        for tx in sub_txs:
                            tx_category = tx.get('category_name', '')
                            # Python-side fallback for uncategorized
                            if uncategorized_only and tx_category:
                                continue
                                
                            tx_source = tx.get('source_name', '')
                            tx_dest = tx.get('destination_name', '')
                            
                            # Python-side strict filtering to prevent Firefly III broad matching issues
                            if account:
                                if account.lower() not in tx_source.lower() and account.lower() not in tx_dest.lower():
                                    continue
                            if source:
                                if source.lower() not in tx_source.lower():
                                    continue
                            if destination:
                                if destination.lower() not in tx_dest.lower():
                                    continue
                            if category:
                                if category.lower() not in tx_category.lower():
                                    continue

                            transactions.append({
                                "id": item.get('id'),
                                "type": tx.get('type', 'unknown'),
                                "date": tx.get('date', '').split('T')[0],
                                "amount": float(tx.get('amount', 0)),
                                "description": tx.get('description', ''),
                                "category": tx_category,
                                "source": tx_source,
                                "destination": tx_dest,
                                "tags": tx.get('tags', []),
                                "notes": tx.get('notes', '')
                            })
                    current_page += 1
                    
                # Sort newest first
                transactions.sort(key=lambda x: x['date'], reverse=True)
                return transactions
            except Exception as e:
                return [{"error": str(e)}]

    async def get_category_summary(self, start_date: str = None, end_date: str = None) -> list[Dict[str, Any]]:
        """
        Fetches transactions and aggregates total expense per category.
        """
        transactions = await self.get_transactions(start_date=start_date, end_date=end_date)
        if transactions and "error" in transactions[0]:
            return transactions

        categories_summary = {}
        for tx in transactions:
            # We only care about expenses for the breakdown
            if tx.get("type") == "withdrawal":
                cat = tx.get("category") or "Sin categoría"
                # Accumulate the amount (storing as positive numbers for charting)
                categories_summary[cat] = categories_summary.get(cat, 0.0) + abs(tx.get("amount", 0))

        # Convert to list and sort by amount descending
        result = [{"name": k, "amount": v} for k, v in categories_summary.items() if v > 0]
        result.sort(key=lambda x: x["amount"], reverse=True)
        return result

    async def get_accounts(self) -> list[Dict[str, Any]]:
        """
        Fetches all asset accounts and their current balances.
        """
        url = f"{self.base_url}/api/v1/accounts?type=asset"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers, timeout=10.0)
                response.raise_for_status()
                data = response.json().get('data', [])
                
                accounts = []
                for item in data:
                    attrs = item.get('attributes', {})
                    if not attrs: continue
                    if not attrs.get('active', True): continue # Skip inactive
                    
                    balance_str = attrs.get('current_balance', '0')
                    try:
                        balance = float(balance_str)
                    except (ValueError, TypeError):
                        balance = 0.0
                        
                    accounts.append({
                        "id": item.get('id'),
                        "name": attrs.get('name', 'Unknown'),
                        "balance": balance,
                        "currency_code": attrs.get('currency_code', 'EUR'),
                        "role": attrs.get('account_role', 'default')
                    })
                return accounts
            except Exception as e:
                return [{"error": str(e)}]

    async def get_all_categories(self) -> list[str]:
        """Fetches all category names."""
        url = f"{self.base_url}/api/v1/categories"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers, timeout=10.0)
                response.raise_for_status()
                data = response.json().get('data', [])
                return [item.get('attributes', {}).get('name') for item in data if item.get('attributes', {}).get('name')]
            except Exception as e:
                return []

    async def get_all_tags(self) -> list[str]:
        """Fetches all tag names."""
        url = f"{self.base_url}/api/v1/tags"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers, timeout=10.0)
                response.raise_for_status()
                data = response.json().get('data', [])
                return [item.get('attributes', {}).get('tag') for item in data if item.get('attributes', {}).get('tag')]
            except Exception as e:
                return []

    async def get_all_accounts_all_types(self) -> list[Dict[str, str]]:
        """Fetches all accounts (asset, revenue, expense) for selection."""
        # Simple implementation: fetch all accounts. Firefly allows getting accounts without type filter to get all or multiple.
        # Actually Firefly pagination might be needed but let's try 1 page for now or just standard endpoint
        url = f"{self.base_url}/api/v1/accounts"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers, timeout=10.0)
                response.raise_for_status()
                data = response.json().get('data', [])
                
                accounts = []
                for item in data:
                    attrs = item.get('attributes', {})
                    if not attrs: continue
                    accounts.append({
                        "id": item.get('id'),
                        "name": attrs.get('name', 'Unknown'),
                        "type": attrs.get('type', 'asset')
                    })
                return accounts
            except Exception:
                return []

    async def get_maintenance_updates(self) -> list[Dict[str, str]]:
        """
        Looks for tags associated with imports (e.g., 'csv_') and finds the date of their latest transaction.
        """
        all_tags = await self.get_all_tags()
        import_tags = [t for t in all_tags if "csv" in t.lower() or "import" in t.lower() or "n8n" in t.lower()]
        
        updates = []
        async with httpx.AsyncClient() as client:
            for tag in import_tags:
                try:
                    import urllib.parse
                    encoded_query = urllib.parse.quote(f'tag:"{tag}"')
                    url = f"{self.base_url}/api/v1/search/transactions?query={encoded_query}&limit=1"
                    response = await client.get(url, headers=self.headers, timeout=10.0)
                    if response.status_code == 200:
                        data = response.json().get('data', [])
                        if data:
                            txs = data[0].get('attributes', {}).get('transactions', [])
                            if txs:
                                latest_date = txs[0].get('date', '').split('T')[0]
                                updates.append({
                                    "tag": tag,
                                    "last_update": latest_date
                                })
                except Exception:
                    pass
        return sorted(updates, key=lambda x: x.get('last_update', ''), reverse=True)

    async def update_transaction(self, tx_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates specific fields of a transaction.
        """
        url = f"{self.base_url}/api/v1/transactions/{tx_id}"
        async with httpx.AsyncClient() as client:
            try:
                # 1. Fetch existing transaction
                get_response = await client.get(url, headers=self.headers, timeout=10.0)
                get_response.raise_for_status()
                current_tx = get_response.json()
                
                attrs = current_tx.get('data', {}).get('attributes', {})
                sub_txs = attrs.get('transactions', [])
                
                if not sub_txs:
                    return {"error": "No split transactions found."}
                
                # 2. Modify the first split (assuming single split for simplicity)
                sub_tx = sub_txs[0]
                
                if "category" in payload:
                    sub_tx["category_name"] = payload["category"]
                if "source" in payload:
                    sub_tx["source_name"] = payload["source"]
                if "destination" in payload:
                    sub_tx["destination_name"] = payload["destination"]
                if "tags" in payload:
                    sub_tx["tags"] = payload["tags"]
                
                # 3. Put back
                put_payload = {
                    "transactions": [sub_tx]
                }
                
                put_response = await client.put(url, headers=self.headers, json=put_payload, timeout=10.0)
                put_response.raise_for_status()
                
                return {"success": True, "id": tx_id}
            except Exception as e:
                return {"error": str(e)}
