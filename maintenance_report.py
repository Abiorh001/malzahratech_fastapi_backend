from fastapi import APIRouter, HTTPException, Depends, status, Query
from schema import  MaintenanceReportModel
from models import Session, engine, User, Machine, MachineMaintenanceReport
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from auth_routes import token_manager


session = Session(bind=engine)

maintenance_report_router = APIRouter(prefix="/api/v1.0", tags=["Maintenance Reports"])




#route to get all maintenance report using assest or machine serial number
@maintenance_report_router.get("/all_maintenance_reports/{machine_serial_number}")
def all_maintenance_reports(machine_serial_number, current_user: str = Depends(token_manager)):
    """
    Get all maintenance report 
    """
    

    user = session.query(User).filter_by(email_address=current_user).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    machine = session.query(Machine).filter_by(user_id=user.id, machine_serial_number=machine_serial_number).first()
    if not machine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")
    
    all_maintenance_reports = session.query(MachineMaintenanceReport).filter_by(user_id=user.id, machine_id=machine.id).all()
    return jsonable_encoder(all_maintenance_reports)


#route to add a new maintenance report
@maintenance_report_router.post("/add_maintenance_report/{machine_serial_number}", status_code=status.HTTP_201_CREATED)
def add_maintenance_report(machine_serial_number: str, maintenance_report: MaintenanceReportModel,
                            current_user: str = Depends(token_manager)):
    """
    Add a new maintenance report
    """

    
    user = session.query(User).filter_by(email_address=current_user).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    machine = session.query(Machine).filter_by(user_id=user.id, machine_serial_number=machine_serial_number).first()
    if not machine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")

    add_maintenance_report = MachineMaintenanceReport(
        maintenance_task_problem=maintenance_report.maintenance_task_problem,
        technician_name=maintenance_report.technician_name,
        maintenance_type=maintenance_report.maintenance_type,
        report_date=maintenance_report.report_date,
        maintenance_task_solution=maintenance_report.maintenance_task_solution,
        start_datetime=maintenance_report.start_datetime,
        end_datetime=maintenance_report.end_datetime,
        labor_hours=maintenance_report.labor_hours,
        parts_cost=maintenance_report.parts_cost,
        additional_notes=maintenance_report.additional_notes,
        user_id=user.id,
        machine_id=machine.id
    )

    session.add(add_maintenance_report)
    session.commit()

    return {"message": "Maintenance report created successfully"}


#route to get a maintenance report using report date
@maintenance_report_router.get("/all_maintenance_reports_by_report_date/{machine_serial_number}")
def all_maintenance_reports_by_report_date(
    
    machine_serial_number: str,
    report_date: datetime = Query(...),
    current_user: str = Depends(token_manager)
):
    """
    Get all maintenance report by report date
    """

   
    user = session.query(User).filter_by(email_address=current_user).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    machine = session.query(Machine).filter_by(user_id=user.id, machine_serial_number=machine_serial_number).first()
    if not machine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")

    all_maintenance_reports_by_report_date = session.query(MachineMaintenanceReport).filter_by(
        user_id=user.id,
        machine_id=machine.id,
        report_date=report_date
    ).all()

    return jsonable_encoder(all_maintenance_reports_by_report_date)


#route to update a maintenance report
@maintenance_report_router.put("/update_maintenance_report/{machine_serial_number}/{id}", status_code=status.HTTP_200_OK)
async def update_maintenance_report(machine_serial_number: str, id: str, maintenance_report: MaintenanceReportModel,
                                    current_user: str = Depends(token_manager)):
    """
    Update a maintenance report
    """

    user = session.query(User).filter_by(email_address=current_user).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    
    machine = session.query(Machine).filter_by(user_id=user.id, machine_serial_number=machine_serial_number).first()

    if not machine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine  not found")

    maintenance_report_to_update = session.query(MachineMaintenanceReport).filter_by(user_id=user.id,
                                                                                    machine_id=machine.id,
                                                                                     id=id).first()

    if not maintenance_report_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Maintenance Report not found")

    maintenance_report_to_update.maintenance_task_problem = maintenance_report.maintenance_task_problem
    maintenance_report_to_update.technician_name = maintenance_report.technician_name
    maintenance_report_to_update.maintenance_type = maintenance_report.maintenance_type
    maintenance_report_to_update.maintenance_task_solution = maintenance_report.maintenance_task_solution
    maintenance_report_to_update.start_datetime = maintenance_report.start_datetime
    maintenance_report_to_update.end_datetime = maintenance_report.end_datetime
    maintenance_report_to_update.labor_hours = maintenance_report.labor_hours
    maintenance_report_to_update.parts_cost = maintenance_report.parts_cost
    maintenance_report_to_update.additional_notes = maintenance_report.additional_notes
    maintenance_report_to_update.date_updated = datetime.utcnow()

    session.commit()

    return {"message":"maintenance report update successfulyy"}



#route to delete a maintenance report
@maintenance_report_router.delete("/delete_maintenance_report/{machine_serial_number}/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_machine(machine_serial_number:str, id:str, current_user: str = Depends(token_manager)):
        """
         Delete a maintenance report 
        """

        user = session.query(User).filter_by(email_address=current_user).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
       
        
        machine = session.query(Machine).filter_by(user_id=user.id, machine_serial_number=machine_serial_number).first()

        if not machine:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine  not found")

        maintenance_report_to_delete = session.query(MachineMaintenanceReport).filter_by(user_id=user.id,
                                                                                    machine_id=machine.id,
                                                                                     id=id).first()

        if not maintenance_report_to_delete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Maintenance Report not found")
        

        session.delete(maintenance_report_to_delete)
        session.commit()
    
