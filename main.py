from fastapi import FastAPI, APIRouter
from auth_routes import auth_router
from machine_routes import machine_router
from maintenance_report import maintenance_report_router
from maintenance_notification import maintenance_notification_router
from maintenance_schedule import maintenance_schedule_router
from fastapi_jwt_auth import AuthJWT
from schema import Settings
from workorder_routes import workorder_router
# from inventory_routes import inventory_router






app = FastAPI(title="Malzahratech Computerized Assets(Machine) Maintenance Management System",
              version="1.0.0",
              description="Malzahratech is a platform for assest management(machines, vehicles, equipments), maintenace report\
                , maintenance schedule, inventory management, predictive maintenance, preventive maintenance, \
                    live data analysis and reports and work order management.")

#load jwt secret key
@AuthJWT.load_config
def get_config():
    return Settings()









app.include_router(auth_router)
app.include_router(machine_router)
app.include_router(maintenance_report_router)
app.include_router(maintenance_notification_router)
app.include_router(maintenance_schedule_router)
app.include_router(workorder_router)
# app.include_router(inventory_router)
