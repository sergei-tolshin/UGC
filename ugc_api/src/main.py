import uvicorn

from core.initialize import app
from api.v1 import (
    root,
    views
)


app.include_router(root.router)
app.include_router(views.router, prefix='/api/v1', tags=['views'])
app.include_router(views.router, prefix='/api/v1', tags=['views/centry'])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
