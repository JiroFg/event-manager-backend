import traceback
from fastapi import APIRouter, status, Depends
from middlewares.token_middleware import validate_token_middleware
from schemas.company_schema import Company
from controllers.company_controller import CompanyController
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/company", tags=["company"])

@router.post("/", dependencies=[Depends(validate_token_middleware)])
def create_company(new_company: Company):
    try:
        company_controller = CompanyController()
        result = company_controller.create(new_company)
        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        traceback_str = traceback.format_exc()
        print(traceback_str)
        return JSONResponse(
            content={"error": True, "details": str(e)},
            status_code=status.status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/{company_id}", dependencies=[Depends(validate_token_middleware)])
def get_company(company_id: int):
    try:
        company_controller = CompanyController()
        result = company_controller.get_company(company_id)
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
            status_code=status.status.HTTP_500_INTERNAL_SERVER_ERROR
        )