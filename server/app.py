#app.py (root of server folder)
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from src.core.config import settings
from src.logger.logger import setup_logger
from src.core import CredentialsException, PermissionDeniedException, NotFoundException, BadRequestException, ConflictException
from src.api import auth, users

logger = setup_logger()


app = FastAPI(
    title="MuscleAI Backend",
    description='Backend for MuscleAI, a fitness app that generates personalized workout plans using AI.',
    version="1.0.0",
    docs_url="/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(CredentialsException)
async def credentials_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(PermissionDeniedException)
async def permission_denied_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(BadRequestException)
async def bad_request_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(ConflictException)
async def conflict_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])

# Root endpoints
@app.get("/")
def read_root():
    return {
        "message": "MuscleAI Backend",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    """Health check endpoint to verify that the server is running."""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": "1.0.0",
        "message": f"{settings.app_name} is healthy!"
    }

# Start up hook
@app.on_event("startup")
async def startup_event():
    print(f"Starting {settings.app_name}")
    print(f"Debug mode: {settings.debug}")

    # Validate critical settings
    if not settings.jwt_secret_key or settings.jwt_secret_key == "your-secret-key-change-this":
        print("WARNING: JWT secret key is not properly configured!")

    if not settings.google_api_key:
        print("WARNING: Google API key is not properly configured!")

    # Initialize any resources here (e.g., database connections, AI models)
    logger.info(f"{settings.app_name} started successfully.")

@app.on_event("shutdown")
async def shutdown_event():
    print(f"Shutting down {settings.app_name}")

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )