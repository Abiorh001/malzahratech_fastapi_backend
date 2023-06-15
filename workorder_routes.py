from fastapi import APIRouter, HTTPException, Depends, status
from schema import EmailRequestModel, WorkOrderModel, UpdateWorkorderModel
from models import Session, engine, User, Machine,Workorder
from fastapi.encoders import jsonable_encoder
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from auth_routes import token_manager





workorder_router = APIRouter(prefix="/api/v1.0", tags=["Work Order Management"])

session = Session(bind=engine)

 
#route to get all work order
@workorder_router.get("/all_workorders/{machine_serial_number}")
def all_work_orders(machine_serial_number:str, current_user: str = Depends(token_manager)):
    """
    Get All Work Orders
    """
    
    user = session.query(User).filter_by(email_address=current_user).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    machine = session.query(Machine).filter_by(user_id=user.id, machine_serial_number=machine_serial_number).first()
    if not machine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")
    
    all_workorders = session.query(Workorder).filter_by(machine_id=machine.id).all()
    if not all_workorders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work order not found")

    return jsonable_encoder(all_workorders)


#route to add a new work order
@workorder_router.post("/add_workorder/{machine_serial_number}/{id}", status_code=status.HTTP_201_CREATED)
def add_work_order(machine_serial_number: str, workorder: WorkOrderModel,
                              current_user: str = Depends(token_manager)):
    """
    Add a new Work order
    """

    user = session.query(User).filter_by(email_address=current_user).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    machine = session.query(Machine).filter_by(user_id=user.id, machine_serial_number=machine_serial_number).first()
    if not machine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")

    new_workorder = Workorder(
        work_order_id=workorder.work_order_id,
        machine_id=machine.id,
        work_type=workorder.work_type,
        description=workorder.description,
        priority=workorder.priority,
        status=workorder.status,
        assigned_technician=workorder.assigned_technician,
        start_date=workorder.start_date,
        end_date=workorder.end_date,
        estimated_hours=workorder.estimated_hours,
        actual_hours=workorder.actual_hours,
        cost=workorder.cost,
        additional_notes=workorder.additional_notes
)


    session.add(new_workorder)
    session.commit()

    return {"message": "New Work Order Created successfully"}


#route to get a work order
@workorder_router.get("/workorder/{machine_serial_number}/{id}")
def view_work_order_by_id(
    machine_serial_number: str,
    id: str,
    current_user: str = Depends(token_manager)
):
    """
    Get a Work Order using its id
    """
   
    user = session.query(User).filter_by(email_address=current_user).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    machine = session.query(Machine).filter_by(user_id=user.id, machine_serial_number=machine_serial_number).first()
    if not machine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")

    workorder = session.query(Workorder).filter_by(machine_id=machine.id, id=id).first()

    return jsonable_encoder(workorder)


#route to update a work order
@workorder_router.put("/update_workorder/{machine_serial_number}/{id}", status_code=status.HTTP_200_OK)
async def update_work_order(machine_serial_number: str, workorder: UpdateWorkorderModel, id: str,
                                  current_user: str = Depends(token_manager)):
    """
    Update A Work Order
    """


    user = session.query(User).filter_by(email_address=current_user).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    
    machine = session.query(Machine).filter_by(user_id=user.id, machine_serial_number=machine_serial_number).first()

    if not machine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine  not found")

    work_order_to_update = session.query(Workorder).filter_by(machine_id=machine.id, id=id).first()

    if not work_order_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work order not found")

    work_order_to_update.status = workorder.status
    work_order_to_update.assigned_technician = workorder.assigned_technician
    work_order_to_update.start_date = workorder.start_date
    work_order_to_update.end_date = workorder.end_date
    work_order_to_update.estimated_hours = workorder.estimated_hours
    work_order_to_update.actual_hours = workorder.actual_hours
    work_order_to_update.cost = workorder.cost
    work_order_to_update.addtional_notes = workorder.additional_notes


    session.commit()

    return {"message":"Work Order updated successfully"}



#route to delete a work order
@workorder_router.delete("/delete_workorder/{machine_serial_number}/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_work_order(machine_serial_number:str, id:str, current_user: str = Depends(token_manager)):
        """
         Delete A Work Order
        """
  
    

        user = session.query(User).filter_by(email_address=current_user).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
       
        
        machine = session.query(Machine).filter_by(user_id=user.id, machine_serial_number=machine_serial_number).first()

        if not machine:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine  not found")

        work_order_to_delete = session.query(Workorder).filter_by(machine_id=machine.id, id=id).first()

        if not work_order_to_delete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=" Work Order not found")
        

        session.delete(work_order_to_delete)
        session.commit()


#route to send a work order email to technician or staff
@workorder_router.post("/send_workorder_email/{machine_serial_number}/{id}")
async def send_work_order_email(email_request: EmailRequestModel, machine_serial_number:str,
                                           id:str, current_user: str = Depends(token_manager)):

    
    """
        Sending An Email For Work Order Request
    """

    user = session.query(User).filter_by(email_address=current_user).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
       
        
    machine = session.query(Machine).filter_by(user_id=user.id, machine_serial_number=machine_serial_number).first()

    if not machine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine  not found")

    workorder = session.query(Workorder).filter_by(machine_id=machine.id, id=id).first()

    if not workorder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work Order not found")
   
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

    body = f"Schedule Data:\t\t {workorder}"
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
    
