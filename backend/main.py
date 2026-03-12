from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.firefly import FireflyService

app = FastAPI(
    title="Llantern API",
    description="Backend API for the Llantern financial dashboard",
    version="1.0.0"
)

# Setup CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

firefly_service = FireflyService()

@app.get("/api/summary", summary="Get financial summary")
async def get_summary(start: str = None, end: str = None):
    """
    Returns the total income, expenses, and balance for a given period.
    Data is fetched directly from the configured Firefly III instance.
    """
    return await firefly_service.get_summary(start_date=start, end_date=end)

@app.get("/api/history", summary="Get historical financial data")
async def get_history(months: int = 6):
    """
    Returns aggregated income/expenses data over the last N months.
    """
    return await firefly_service.get_history(months=months)

@app.get("/api/transactions", summary="Get transactions")
async def get_transactions(
    start: str = None, 
    end: str = None, 
    uncategorized_only: bool = False,
    category: str = None,
    tag: str = None,
    source: str = None,
    destination: str = None
):
    """
    Returns transactions, optionally filtered by date range and category/entity.
    """
    return await firefly_service.get_transactions(
        start_date=start, 
        end_date=end, 
        uncategorized_only=uncategorized_only,
        category=category,
        tag=tag,
        source=source,
        destination=destination
    )

@app.get("/api/accounts", summary="Get asset accounts")
async def get_accounts():
    """
    Returns a list of asset accounts with their balances.
    """
    return await firefly_service.get_accounts()

@app.get("/api/categories", summary="Get category aggregated summary")
async def get_categories(start: str = None, end: str = None):
    """
    Returns a list of categories and their total expenses for a given period.
    """
    return await firefly_service.get_category_summary(start_date=start, end_date=end)

@app.get("/api/debug", summary="Get raw data for debugging")
async def get_debug_summary():
    """
    Returns the exact JSON that Firefly III provides, to help fix parsing bugs.
    """
    return await firefly_service.get_raw_summary()

@app.get("/health", summary="Health check endpoint")
async def health_check():
    return {"status": "ok"}
