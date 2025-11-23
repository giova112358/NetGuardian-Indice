from fastapi import FastAPI
from backend.routers import repertori_router, interactions_router
from fastapi.middleware.cors import CORSMiddleware

# Initialize the API
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers we defined
app.include_router(repertori_router.router)
app.include_router(interactions_router.router)


@app.get("/")
def root():
    return {"message": "Welcome to the Repertori API. Visit /docs for documentation."}
