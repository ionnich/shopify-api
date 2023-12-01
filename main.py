
from fastapi import FastAPI
from routers import donation, user, partners
from security import security

app = FastAPI()

app.include_router(donation.router, prefix="/donations", tags=["Donations"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(partners.router, prefix="/partners", tags=["Partners"])


@app.get("/")
async def root():
    return {"message": "Hello from PCX Donations!"}
