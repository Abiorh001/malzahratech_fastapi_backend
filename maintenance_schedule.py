from fastapi import APIRouter, HTTPException, Depends, status, Query
from schema import MaintenanceScheduleModel,UpdateMaintenanceScheduleModel,EmailRequestModel
from fastapi_jwt_auth import AuthJWT
from models import Session, engine, User, Machine, MaintenanceSchedule
from fastapi.encoders import jsonable_encoder
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from auth_routes import token_manager






maintenance_schedule_router = APIRouter(prefix="/api/v1.0", tags=["Maintenance-Schedules"])

session = Session(bind=engine)


 


#route to get all maintenance schedule using assest or machine serial number
@maintenance_schedule_router.get("/all_maintenance_schedules/{machine_serial_number}")
def all_maintenance_schedules(machine_serial_number:str, current_user: str = Depends(token_manager)):
    """
    Get All Maintenance Schedules
    """

    
    user = session.query(User).filter_by(email_address=current_user).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    machine = session.query(Machine).filter_by(user_id=user.id, machine_serial_number=machine_serial_number).first()
    if not machine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")
    
    all_maintenance_schedules = session.query(MaintenanceSchedule).filter_by(user_id=user.id, machine_id=machine.id).all()
    if not all_maintenance_schedules:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Maintenance Schedules not found")

    return jsonable_encoder(all_maintenance_schedules)


#route to add a new maintenance schedule
@maintenance_schedule_router.post("/add_maintenance_schedule/{machine_serial_number}", status_code=status.HTTP_201_CREATED)
def add_maintenance_schedule(machine_serial_number: str, maintenance_schedule: MaintenanceScheduleModel,
                              current_user: str = Depends(token_manager)):
    """
    Add a new Maintenance Schedule
    """


    user = session.query(User).filter_by(email_address=current_user).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    machine = session.query(Machine).filter_by(user_id=user.id, machine_serial_number=machine_serial_number).first()
    if not machine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")

    add_maintenance_schedule = MaintenanceSchedule(
    schedule_date=maintenance_schedule.schedule_date,
    notes=maintenance_schedule.notes,
    user_id=user.id,
    machine_id=machine.id,
    schedule_tasks=maintenance_schedule.schedule_tasks,
    status=maintenance_schedule.status,
    technician_name=maintenance_schedule.technician_name
)


    session.add(add_maintenance_schedule)
    session.commit()

    return {"message": "Maintenance Schedule Created successfully"}


#route to get a maintenance schedule using schedule date
@maintenance_schedule_router.get("/all_maintenance_schedule_by_schedule_date/{machine_serial_number}")
def all_maintenance_reports_by_notification_date(
    
    machine_serial_number: str,
    notification_datetime: datetime = Query(...),
    current_user: str = Depends(token_manager)
):
    """
    Get all maintenance schedule by schedule date
    """


    user = session.query(User).filter_by(email_address=current_user).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    machine = session.query(Machine).filter_by(user_id=user.id, machine_serial_number=machine_serial_number).first()
    if not machine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")

    all_maintenance_schedules_by_schedule_date = session.query(MaintenanceSchedule).filter_by(
        user_id=user.id,
        machine_id=machine.id,
        notification_datetime=notification_datetime
    ).all()

    return jsonable_encoder(all_maintenance_schedules_by_schedule_date)


#route to update a maintenance schedule
@maintenance_schedule_router.put("/update_maintenance_schedule/{machine_serial_number}/{id}", status_code=status.HTTP_200_OK)
async def update_maintenance_schedule(machine_serial_number: str, id: str, maintenance_schedule: UpdateMaintenanceScheduleModel,
                                  current_user: str = Depends(token_manager)):
    """
    Update A Maintenance Schedule
    """

    user = session.query(User).filter_by(email_address=current_user).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    
    machine = session.query(Machine).filter_by(user_id=user.id, machine_serial_number=machine_serial_number).first()

    if not machine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine  not found")

    maintenance_schedule_to_update = session.query(MaintenanceSchedule).filter_by(user_id=user.id,
                                                                                    machine_id=machine.id,
                                                                                     id=id).first()

    if not maintenance_schedule_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Maintenance Schedule not found")

    maintenance_schedule_to_update.notes = maintenance_schedule.notes
    maintenance_schedule_to_update.schedule_tasks = maintenance_schedule.schedule_tasks
    maintenance_schedule_to_update.status = maintenance_schedule.status
    maintenance_schedule_to_update.date_updated = datetime.utcnow()

    session.commit()

    return {"message":"maintenance schedule updated successfully"}



#route to delete a maintenance schedule
@maintenance_schedule_router.delete("/delete_maintenance_schedule/{machine_serial_number}/{id}",
                                     status_code=status.HTTP_204_NO_CONTENT)
async def delete_maintenance_schedule(machine_serial_number:str, id:str, current_user: str = Depends(token_manager)):
        """
         Delete A Maintenance Schedule
        """


        user = session.query(User).filter_by(email_address=current_user).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
       
        
        machine = session.query(Machine).filter_by(user_id=user.id, machine_serial_number=machine_serial_number).first()

        if not machine:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine  not found")

        maintenance_schedule_to_delete = session.query(MaintenanceSchedule).filter_by(user_id=user.id,
                                                                                    machine_id=machine.id,
                                                                                     id=id).first()

        if not maintenance_schedule_to_delete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Maintenance Schedule not found")
        

        session.delete(maintenance_schedule_to_delete)
        session.commit()


#route to send a maintenance schedule email to technician or staff
@maintenance_schedule_router.post("/send_maintenance_schedule_email/{machine_serial_number}/{id}")
async def send_maintenance_schedule_email(email_request: EmailRequestModel, machine_serial_number:str,
                                           id:str, current_user: str = Depends(token_manager)):

    """
        Sending An Email For Maintenance Schedule
    """

    user = session.query(User).filter_by(email_address=current_user).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
       
        
    machine = session.query(Machine).filter_by(user_id=user.id, machine_serial_number=machine_serial_number).first()

    if not machine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine  not found")

    maintenance_schedule = session.query(MaintenanceSchedule).filter_by(user_id=user.id,
                                                                                    machine_id=machine.id,
                                                                                     id=id).first()

    if not maintenance_schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Maintenance Schedule not found")

    # SMTP server details
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587  
    smtp_username = 'abiolaadedayo1993@gmail.com'
    smtp_password = 'etkazqurxvtqouak'  

    # Create a multipart message
    msg = MIMEMultipart()
    msg["From"] = email_request.sender_email
    msg["To"] = email_request.receiver_email
    msg["Subject"] = email_request.subject
    # Add the schedule data to the email body

    body = f"Schedule Data:\t\t{maintenance_schedule.schedule_date}\n\n{maintenance_schedule.notes}\n\n{maintenance_schedule.status}\
        \n\n{maintenance_schedule.technician_name}\n\n{maintenance_schedule.schedule_tasks}"
    msg.attach(MIMEText(body, "plain"))


    try:
        # Create a secure connection with the SMTP server
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        # Login to the SMTP server
        server.login(smtp_username, smtp_password)
        # Send the email
        server.send_message(msg)
        # Close the SMTP server connection
        server.quit()

        return {"message": "Email sent successfully"}

    except Exception as e:
        return {"message": "Failed to send email", "error": str(e)}
    
