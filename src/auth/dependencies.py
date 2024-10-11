from fastapi import Request, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from .utils import decode_token
from src.db.redis import token_in_blocklist
from src.db.main import get_session
from .service import UserService


user_service = UserService()


class TokenBearer(HTTPBearer):
    
    def __init__(self, auto_error = True):
        super().__init__(auto_error = auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token = creds.credentials

        token_data = decode_token(token)

        if not self.token_valid(token):
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = {
                    "error": "This token is invalid or has expired.",
                    "resolution": "Please get a new token"
                }
            )
        
        if await token_in_blocklist(token_data["jti"]):
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = {
                    "error": "This token is invalid or has been revoked.",
                    "resolution": "Please get a new token"
                }
            )
        
        self.verify_token_data(token_data)

        return token_data
    
    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)

        return token_data is not None
    
    def verify_token_data(self, token_data):
        raise NotImplementedError("Please override this method in child classes")
    

class AccessTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = "Please provide an access token"
            )
    

class RefreshTokenBearer(TokenBearer):
    
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = "Please provide a refresh token"
            )
        

async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session)
):
    user_email = token_details["user"]["email"]

    user = await user_service.get_user_by_email(user_email, session)

    return user
