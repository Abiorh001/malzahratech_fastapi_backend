from fastapi import APIRouter, HTTPException, Depends, status, Query
from schema import MaintenanceNotificationModel, UpdateMaintenanceNotificationModel, EmailRequestModel
from fastapi_jwt_auth import AuthJWT
from models import Session, engine, User, Machine, MaintenanceNotification
from fastapi.encoders import jsonable_encoder
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from auth_routes import token_manager


session = Session(bind=engine)

maintenance_notification_router = APIRouter(prefix="/api/v1.0", tags=["Maintenance Notifications"])






#route to get all maintenance notification using assest or machine serial number
@maintenance_notification_router.get("/all_maintenance_notifications/{machine_serial_number}")
def all_maintenance_notifications(machine_serial_number, current_user: str = Depends(token_manager)):
    """
    Get All Maintenance Notifications
    """
    
    user = session.query(User).filter_by(email_address=current_user).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    machine = session.query(Machine).filter_by(user_id=user.id, machine_serial_number=machine_serial_number).first()
    if not machine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")
    
    all_maintenance_notifications = session.query(MaintenanceNotification).filter_by(user_id=user.id, machine_id=machine.id).all()
    if not all_maintenance_notifications:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Maintenance Notification not found")

    return jsonable_encoder(all_maintenance_notifications)


#route to add a new maintenance notification
@maintenance_notification_router.post("/add_maintenance_notification/{machine_serial_number}", status_code=status.HTTP_201_CREATED)
def add_maintenance_notification(machine_serial_number: str, maintenance_notification: MaintenanceNotificationModel, 
                                 current_user: str = Depends(token_manager)):
    """
    Add a new Maintenance Notification
    """

    user = session.query(User).filter_by(email_address=current_user).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    machine = session.query(Machine).filter_by(user_id=user.id, machine_serial_number=machine_serial_number).first()
    if not machine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")

    add_maintenance_notification = MaintenanceNotification(
    description = maintenance_notification.description,
    status = maintenance_notification.status,
    notification_datetime=maintenance_notification.notification_datetime,
    date_created=maintenance_notification.date_created,
    date_updated=maintenance_notification.date_updated,
    user_id=user.id,
    machine_id=machine.id
)


    session.add(add_maintenance_notification)
    session.commit()

    return {"message": "Maintenance Notification Created successfully"}


#route to get a maintenance notification using notification date
@maintenance_notification_router.get("/all_maintenance_notification_by_notification_date/{machine_serial_number}")
def all_maintenance_reports_by_notification_date(
    
    machine_serial_number: str,
    notification_datetime: datetime = Query(...),
   current_user: str = Depends(token_manager)
):
    """
    Get all maintenance notification by notification date
    """

    user = session.query(User).filter_by(email_address=current_user).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    machine = session.query(Machine).filter_by(user_id=user.id, machine_serial_number=machine_serial_number).first()
    if not machine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")

    all_maintenance_reports_by_notification_date = session.query(MaintenanceNotification).filter_by(
        user_id=user.id,
        machine_id=machine.id,
        notification_datetime=notification_datetime
    ).all()

    return jsonable_encoder(all_maintenance_reports_by_notification_date)


#route to update a maintenance notification
@maintenance_notification_router.put("/update_maintenance_notification/{machine_serial_number}/{id}", status_code=status.HTTP_200_OK)
async def update_maintenance_notification(machine_serial_number: str, id: str, maintenance_notification: UpdateMaintenanceNotificationModel,
                                   current_user: str = Depends(token_manager)):
    """
    Update A Maintenance Notification
    """

    user = session.query(User).filter_by(email_address=current_user).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    
    machine = session.query(Machine).filter_by(user_id=user.id, machine_serial_number=machine_serial_number).first()

    if not machine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine  not found")

    maintenance_notification_to_update = session.query(MaintenanceNotification).filter_by(user_id=user.id,
                                                                                    machine_id=machine.id,
                                                                                     id=id).first()

    if not maintenance_notification_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Maintenance Notification not found")
    
    maintenance_notification_to_update.description = maintenance_notification.description
    maintenance_notification_to_update.status = maintenance_notification.status
    maintenance_notification_to_update.date_updated = datetime.utcnow()


    session.commit()

    return {"message":"maintenance notification updated successfully"}



#route to delete a maintenance notification
@maintenance_notification_router.delete("/delete_maintenance_notification/{machine_serial_number}/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_maintenance_notification(machine_serial_number:str, id:str, current_user: str = Depends(token_manager)):
        """
         Delete A Maintenance Notification
        """


        user = session.query(User).filter_by(email_address=current_user).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
       
        
        machine = session.query(Machine).filter_by(user_id=user.id, machine_serial_number=machine_serial_number).first()

        if not machine:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine  not found")

        maintenance_notification_to_delete = session.query(MaintenanceNotification).filter_by(user_id=user.id,
                                                                                    machine_id=machine.id,
                                                                                     id=id).first()

        if not maintenance_notification_to_delete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Maintenance Notification not found")
        

        session.delete(maintenance_notification_to_delete)
        session.commit()


#route to send a maintenance notification email to technician or staff
@maintenance_notification_router.post("/send_maintenance_notification_email/{machine_serial_number}/{id}", status_code=status.HTTP_200_OK)
async def send_maintenance_notification_email(email_request: EmailRequestModel, machine_serial_number:str,
                                           id:str, current_user: str = Depends(token_manager)):


    
    """
        Sending An Email For Maintenance Notification
    """

    user = session.query(User).filter_by(email_address=current_user).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
       
        
    machine = session.query(Machine).filter_by(user_id=user.id, machine_serial_number=machine_serial_number).first()

    if not machine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine  not found")

    maintenance_notification = session.query(MaintenanceNotification).filter_by(user_id=user.id,
                                                                                    machine_id=machine.id,
                                                                                     id=id).first()

    if not maintenance_notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Maintenance Notification not found")
   
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

    body = f"Maintenance Notification:\t\t{maintenance_notification.status}\n\n{maintenance_notification.description}\n\n{maintenance_notification.notification_datetime}"
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
    

    
