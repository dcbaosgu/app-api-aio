from pydantic import BaseModel

class ReportRequest(BaseModel):
    invoice_id: str
    customer_name: str
    total_price: str
    create_time: str
    method_payment: str
    delivery_address: str
    note_transport: str