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

@app.get("/health", summary="Health check endpoint")
async def health_check():
    return {"status": "ok"}
