import traceback
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from controllers.catalog_controller import CatalogController

router = APIRouter(
    prefix="/catalog",
    tags=["catalog"]
)

@router.get("/user-type")
def get_user_types():
    try:
        catalog_controller = CatalogController()
        result = catalog_controller.get_user_types()
        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        traceback_str = traceback.format_exc()
        print(traceback_str)
        return JSONResponse(
            content={
                "error": True,
                "details": str(e)
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/country")
def get_countries():
    try:
        catalog_controller = CatalogController()
        result = catalog_controller.get_countries()
        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
            content={
                "error": True,
                "details": str(e)
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/state")
def get_states():
    try:
        catalog_controller = CatalogController()
        result = catalog_controller.get_states()
        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
            content={
                "error": True,
                "details": str(e)
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )