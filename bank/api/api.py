from fastapi import APIRouter
from starlette.responses import RedirectResponse

from bank.api.endpoints import wallets, transfer

api_router = APIRouter()
api_router.include_router(wallets.router, prefix="/wallets", tags=["wallet"])
api_router.include_router(transfer.router, prefix="/transfer", tags=["transfer"])


@api_router.get("/")
def index():
    return RedirectResponse(url="/docs")
