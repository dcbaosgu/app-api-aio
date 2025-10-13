from fastapi import APIRouter, Query
from typing import Optional
from . import schema
from .controller import InvoiceController
from .exception import ErrorCode

router = APIRouter(prefix="/v1/invoice", tags=["Invoice"])
controller = InvoiceController()


@router.post("/checkout/{user_id}", status_code=201, responses={
    201: {"model": schema.InvoiceResponse, "description": "Create items success"},
})
async def checkout_invoice(user_id: str):
    result = await controller.checkout_cart(user_id)
    if not result:
        raise ErrorCode.InvoiceNotFound()
    return result


@router.get("/get/{invoice_id}", status_code=200, responses={
    200: {"model": schema.InvoiceResponse, "description": "Get items success"},
})
async def get_invoice(invoice_id: str):
    result = await controller.get(invoice_id)
    if not result:
        raise ErrorCode.InvalidInvoiceId()
    return result


@router.put("/edit/{invoice_id}", status_code=200, responses={
    200: {"model": schema.InvoiceResponse, "description": "Edit items success"},
})
async def update_invoice(invoice_id: str, data: schema.InvoiceUpdate):
    result = await controller.update(invoice_id, data.model_dump(exclude_unset=True))
    return schema.InvoiceResponse(**result)


@router.delete("/delete/{invoice_id}", status_code=200, responses={
    200: {"description": "Xóa invoice thành công"},
})
async def delete_invoice(invoice_id: str):
    result = await controller.delete(invoice_id)
    return result


@router.get("/search", status_code=200, responses={
    200: {"model": schema.PaginatedInvoiceResponse, "description": "Get items success"},
})
async def list_invoices(
    page: int = Query(1, gt=0, description="Page number"),
    limit: int = Query(10, le=100, description="Quantity items per page"),
    user_id: Optional[str] = Query(None, description="Filter User ID"),
    status: Optional[str] = Query(None, description="Status: pending /confirmed / delivery / finished/ cancelled"),
    start_time: Optional[str] = Query(None, description="Start time (Format: DD-MM-YYYY HH:MM:SS)-GMT+7"),
    end_time: Optional[str] = Query(None, description="End time (Format: DD-MM-YYYY HH:MM:SS)-GMT+7)")
):
    query = {}
    if user_id: query["user_id"] = user_id
    if status: query["status"] = status

    result = await controller.search(query, page, limit, start_time, end_time)
    return result
