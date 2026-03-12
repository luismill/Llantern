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

@app.get("/api/summary", summary="Get monthly financial summary")
async def get_summary():
    """
    Returns the total income, expenses, and balance for the current month.
    Data is fetched directly from the configured Firefly III instance.
    """
    return await firefly_service.get_summary()

@app.get("/api/history", summary="Get historical financial data")
async def get_history(months: int = 6):
    """
    Returns aggregated income/expenses data over the last N months.
    """
    return await firefly_service.get_history(months=months)

@app.get("/api/debug", summary="Get raw data for debugging")
async def get_debug_summary():
    """
    Returns the exact JSON that Firefly III provides, to help fix parsing bugs.
    """
    return await firefly_service.get_raw_summary()

@app.get("/health", summary="Health check endpoint")
async def health_check():
    return {"status": "ok"}
