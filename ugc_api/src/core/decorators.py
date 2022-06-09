from functools import wraps

from fastapi import HTTPException, status

from core.utils.translation import gettext_lazy as _


def login_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs.get('request')
        if not request.user.is_authenticated:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=_('You need to login'),
            )
        return await func(*args, **kwargs)

    return wrapper
