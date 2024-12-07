import traceback
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from middlewares.token_middleware import validate_token_middleware
from controllers.table_controller import TableController
from schemas.table_schema import ExtraTables


router = APIRouter(prefix="/table", tags=["tables"])

@router.get("/{event_id}", dependencies=[Depends(validate_token_middleware)])
def get_tables_by_event(event_id: int):
    try:
        table_controller = TableController()
        result = table_controller.get_tables_by_event(event_id)
        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            content={"error": True, "details": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.put("/", dependencies=[Depends(validate_token_middleware)], tags=["admin"])
def create_extra_tables(extra_tables: ExtraTables):
    try:
        table_controller = TableController()
        result = table_controller.create_extra_tables(extra_tables)
        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            content={"error": True, "details": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.delete("/{table_id}", dependencies=[Depends(validate_token_middleware)], tags=["admin"])
def delete_table(table_id: int):
    try:
        table_controller = TableController()
        result = table_controller.delete_table(table_id)
        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            content={"error": False, "details": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )