from fastapi import APIRouter

from Controllers import MapController

router = APIRouter()


@router.get('/map')
async def get_map():
    return MapController.getMap()