from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime



class SignUpModel(BaseModel):

    id: Optional[str]
    first_name: str
    last_name: Optional[str]
    role:Optional[str]
    phone_number: Optional[str]
    email_address: str
    password: str
    street_address: str
    city: str
    state: str
    zip_code: str
    country: str
    reset_token: Optional[str]
    date_created: Optional[datetime]
    date_updated: Optional[datetime]

    class Config:

        orm_mode = True
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email_address": "johndoe@example.com",
                "password": "mypassword",
                "street_address": "123 Main St",
                "city": "New York",
                "state": "NY",
                "zip_code": "10001",
                "country": "USA"
            }
        }

class Settings(BaseModel):

    authjwt_secret_key : str='fefe3367fd45db15554f0e1e36c9af1a'

class SignInModel(BaseModel):
     
    email_address: str
    password: str

class ForgetPasswordModel(BaseModel):
     
    email_address: str

class ResetPasswordModel(BaseModel):
    password:str

class MachineModel(BaseModel):
    id: Optional[str]
    machine_name: str
    machine_model: str
    machine_serial_number: str
    machine_manufacturer: str
    machine_location: str
    machine_warranty_expiration_date: Optional[datetime]
    machine_purchase_date: Optional[datetime]
    machine_operational_hours: Optional[int]
    machine_error_logs: Optional[str]
    machine_description: Optional[str]
    machine_images: Optional[str]
    user_id: Optional[str]
    date_created: Optional[datetime]
    date_updated: Optional[datetime]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "machine_name": "Machine 1",
                "machine_model": "Model XYZ",
                "machine_serial_number": "12345",
                "machine_manufacturer": "Manufacturer ABC",
                "machine_location": "Location XYZ",
                "machine_warranty_expiration_date": "2023-12-31",
                "machine_purchase_date": "2023-01-01",
                "machine_operational_hours": 500,
                "machine_error_logs": "No errors",
                "machine_description": "Description of the machine",
                "machine_images": "https://example.com/image.jpg",
                "user_id": "user_id_123",
                "date_created": "2023-05-27T10:00:00Z",
                "date_updated": "2023-05-27T15:30:00Z"
            }
        }

class UpdateMachineModel(BaseModel):

    machine_operational_hours: Optional[int]
    machine_error_logs: Optional[str]
    machine_description: Optional[str]
    date_updated: Optional[datetime]


    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
               
                "machine_operational_hours": 500,
                "machine_error_logs": "No errors",
                "machine_description": "Description of the machine",
                 "date_updated": "2023-05-27T15:30:00Z"
              
            }
        }

class MaintenanceReportModel(BaseModel):
    maintenance_task_problem: str
    technician_name: str
    maintenance_type: str
    report_date: datetime
    maintenance_task_solution: Optional[str]
    start_datetime: Optional[datetime]
    end_datetime: Optional[datetime]
    labor_hours: Optional[float]
    parts_cost: Optional[float]
    additional_notes: Optional[str]
    user_id: Optional[str]
    machine_id: Optional[str]
    date_created: Optional[datetime]
    date_updated: Optional[datetime]

class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "maintenance_task_problem": "Example problem",
                "technician_name": "John Doe",
                "maintenance_type": "Routine maintenance",
                "report_date": "2023-05-24T10:00:00Z",
                "maintenance_task_solution": "Example solution",
                "start_datetime": "2023-05-24T10:30:00Z",
                "end_datetime": "2023-05-24T11:30:00Z",
                "labor_hours": 1.5,
                "parts_cost": 50.0,
                "additional_notes": "Additional notes",
                "user_id": "user123",
                "machine_id": "machine123",
                "date_created": "2023-05-24T12:00:00Z",
                "date_updated": "2023-05-24T12:00:00Z"
            }
        }
class MaintenanceNotificationModel(BaseModel):
    description: Optional[str]
    status: str
    notification_datetime: datetime
    date_created: Optional[datetime]
    date_updated: Optional[datetime]
    user_id: Optional[str]
    machine_id: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "description": "Maintenance notification description",
                "status": "Pending",
                "notification_datetime": "2023-05-25T10:30:00Z",
                "date_created": "2023-05-24T15:45:00Z",
                "date_updated": "2023-05-24T15:45:00Z",
                "user_id": "user-id",
                "machine_id": "machine-id"
            }
        }

class UpdateMaintenanceNotificationModel(BaseModel):

    description: Optional[str]
    status: str
    date_updated: Optional[datetime]


    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
               
                "description": "Maintenance notification description",
                    "status": "Pending",
                 "date_updated": "2023-05-27T15:30:00Z"
              
            }
        }

class MaintenanceScheduleModel(BaseModel):
    id: Optional[str]
    schedule_date: datetime
    notes: Optional[str]
    user_id: Optional[str]
    machine_id: Optional[str]
    schedule_tasks: Optional[str]
    status: str
    technician_name: Optional[str]
    date_created: Optional[datetime]
    date_updated: Optional[datetime]
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "schedule_date": "2023-05-31T09:00:00",
                "notes": "Perform maintenance tasks",
                "user_id": "user123",
                "machine_id": "machine456",
                "schedule_tasks": "Task 1, Task 2, Task 3",
                "status": "PENDING",
                "technician_name": "John Doe"
            }
        }

class UpdateMaintenanceScheduleModel(BaseModel):

    notes: Optional[str]
    schedule_tasks: Optional[str]
    status: str
    date_updated: Optional[datetime]


    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
               
                "notes": "Perform maintenance tasks",
                "schedule_tasks": "Task 1, Task 2, Task 3",
                "status": "PENDING",
                "date_updated": "2023-05-27T15:30:00Z"
              
            }
        }

class EmailRequestModel(BaseModel):
    sender_email: str
    receiver_email: str
    subject: str


class WorkOrderModel(BaseModel):
    work_order_id: str
    work_type: str
    description: str
    priority: str
    status: str
    assigned_technician: str
    start_date: datetime
    end_date: datetime
    estimated_hours: Optional[float]
    actual_hours: Optional[float]
    cost: Optional[float]
    additional_notes: Optional[str]
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "work_order_id": "WO12345",
                "machine_id": "M123",
                "work_type": "Maintenance",
                "description": "Perform maintenance tasks",
                "priority": "High",
                "status": "PENDING",
                "assigned_technician": "John Doe",
                "start_date": "2023-05-27",
                "end_date": "2023-05-28",
                "estimated_hours": 4.5,
                "actual_hours": 3.5,
                "cost": 100.0,
                "additional_notes": "Additional notes",
            }
        }

class UpdateWorkorderModel(BaseModel):
    status: str
    assigned_technician: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    estimated_hours: Optional[float]
    actual_hours: Optional[float]
    cost: Optional[float]
    additional_notes: Optional[str]
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
               
                "status": "COMPLETED",
                "assigned_technician": "John Doe",
                "start_date": "2023-05-27",
                "end_date": "2023-05-28",
                "estimated_hours": 4.5,
                "actual_hours": 3.5,
                "cost": 100.0,
                "additional_notes": "Additional notes",
            }
        }


class SparePartModel(BaseModel):
    part_name: str
    description: str
    quantity: int
    unit_price: float
    minimum_quantity: int
    location: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "part_name": "Part A",
                "description": "Sample description",
                "quantity": 10,
                "unit_price": 19.99,
                "minimum_quantity": 5,
                "location": "Warehouse 1"
            }
        }


class SparePartUpdateModel(BaseModel):
    part_name: str
    description: str
    quantity: int
    unit_price: float
    minimum_quantity: int
    location: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "part_name": "Part A",
                "description": "Sample description",
                "quantity": 10,
                "unit_price": 19.99,
                "minimum_quantity": 5,
                "location": "Warehouse 1"
            }
        }

class SupplierModel(BaseModel):
    supplier_name: str
    contact_person: str
    phone_number: str
    email: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "supplier_name": "Supplier A",
                "contact_person": "John Doe",
                "phone_number": "1234567890",
                "email": "supplier@example.com",
                
            }
        }

class PurchaseOrderModel(BaseModel):
   
    quantity: int
    total_price: float
    date_ordered: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "quantity": 5,
                "total_price": 99.95,
                "date_ordered": "2023-05-27T10:30:00"
            }
        }

class PurchaseRequestModel(BaseModel):
    quantity: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "quantity": 10,
            }
        }

class RequestForQuoteModel(BaseModel):

    description: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "description": "Request for quote for Part A"
            }
        }

class RequestForProposalModel(BaseModel):
    description: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "description": "Request for proposal for Part A"
            }
        }
