from core.initialize import router


@router.get("/")
async def root():
    return {"message": "Alive"}
