import traceback
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from schemas.product_schema import Product, ProductEdit
from controllers.product_controller import ProductController


router = APIRouter(prefix="/product", tags=["product"])

@router.post("/")
def create_product(new_product: Product):
    try:
        product_controller = ProductController()
        result = product_controller.create(new_product)
        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            content={"error":True, "details":str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/event/{event_id}")
def get_products_by_event(event_id: int):
    try:
        product_controller = ProductController()
        result = product_controller.get_products_by_event(event_id)
        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            content={"error":True, "details":str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/user/{user_id}")
def get_products_by_user(user_id: int):
    try:
        product_controller = ProductController()
        result = product_controller.get_products_by_user(user_id)
        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            content={"error":True, "details":str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.put("/")
def update_product(product_edit: ProductEdit):
    try:
        product_controller = ProductController()
        result = product_controller.update_product(product_edit)
        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            content={"error":True, "details":str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )