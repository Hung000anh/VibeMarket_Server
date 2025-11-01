from fastapi import FastAPI
from app.modules.health.router import router as health_router
from app.modules.asset_types.router import router as asset_types_router
from app.modules.exchanges.router import router as exchanges_router
from app.modules.symbols.router import router as symbols_router
from app.modules.symbol_timeframes.router import router as symbol_timeframes_router
from app.modules.timeframes.router import router as timeframes_router
from app.modules.prices.router import router as prices_router
from app.scheduler import scheduler
app = FastAPI(
    title="VibeMarket",
    docs_url="/docs",       # URL Swagger UI
    openapi_url="/openapi.json",
    swagger_ui_parameters={
        "deepLinking": True,
        "displayRequestDuration": True,
        "docExpansion": "none",
        "tryItOutEnabled": True,
        "persistAuthorization": True,
        "defaultModelsExpandDepth": -1,
        "tagsSorter": "none"
        }
)

from datetime import datetime

now = datetime.now()
print("Local time:", now.strftime("%Y-%m-%d %H:%M:%S"))

app.include_router(health_router)
app.include_router(asset_types_router)
app.include_router(exchanges_router)
app.include_router(symbols_router)
app.include_router(timeframes_router)
app.include_router(symbol_timeframes_router)
app.include_router(prices_router)