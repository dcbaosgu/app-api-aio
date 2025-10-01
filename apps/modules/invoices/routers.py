from fastapi import APIRouter, Query
from typing import Optional
from . import schemas
from .exception import ErrorCode
from .controllers import InvoiceController

router = APIRouter(prefix="/v1/invoice", tags=["invoice"])
controller = InvoiceController()


@router.post("/checkout/{user_id}", status_code=201, responses={
    201: {"model": schemas.InvoiceResponse, "description": "Create items success"},
})
async def checkout_invoice(user_id: str):
    result = await controller.checkout_cart(user_id)
    if not result:
        raise ErrorCode.InvoiceNotFound()
    return result


@router.get("/get/{invoice_id}", status_code=200, responses={
    200: {"model": schemas.InvoiceResponse, "description": "Get items success"},
})
async def get_invoice(invoice_id: str):
    result = await controller.get(invoice_id)
    if not result:
        raise ErrorCode.InvalidInvoiceId()
    return result


@router.put("/edit/{invoice_id}", status_code=200, responses={
    200: {"model": schemas.InvoiceResponse, "description": "Edit items success"},
})
async def update_invoice(invoice_id: str, data: schemas.InvoiceUpdate):
    result = await controller.update(invoice_id, data.model_dump(exclude_unset=True))
    return schemas.InvoiceResponse(**result)


@router.delete("/delete/{invoice_id}", status_code=200, responses={
    200: {"description": "Xóa invoice thành công"},
})
async def delete_invoice(invoice_id: str):
    result = await controller.delete(invoice_id)
    return result


@router.get("/search", status_code=200, responses={
    200: {"model": schemas.PaginatedInvoiceResponse, "description": "Get items success"},
})
async def list_invoices(
    page: int = Query(1, gt=0, description="Page number"),
    limit: int = Query(10, le=100, description="Quantity items per page"),
    user_id: Optional[str] = Query(None, description="Filter User ID"),
    status: Optional[str] = Query(None, description="Status: pending /confirmed / delivery / finished/ cancelled"),
    start_time: Optional[str] = Query(None, description="Start day (Format: DD/MM/YYYY) - GMT+7)"),
    end_time: Optional[str] = Query(None, description="End day (Format: DD/MM/YYYY) - GMT+7)")
):
    query = {}
    if user_id: query["user_id"] = user_id
    if status: query["status"] = status

    result = await controller.search(query, page, limit, start_time, end_time)
    return result
