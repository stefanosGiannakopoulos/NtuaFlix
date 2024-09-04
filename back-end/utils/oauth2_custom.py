from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi import status

class OAuth2PasswordCustomHeader(OAuth2PasswordBearer):
    """Adapter from 'Authentication: Bearer' header to custom header variable"""

    def __init__(
        self,
        tokenUrl: str,
        header_name: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[dict] = None,
        auto_error: bool = True,
    ):
        super().__init__(
            tokenUrl=tokenUrl,
            scopes=scopes,
            scheme_name=scheme_name,
            auto_error=auto_error,
        )
        self.header_name = header_name

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get(self.header_name)
        if not authorization:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "JWT"},
                )
            else:
                return None
        return authorization

