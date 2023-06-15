from fastapi import APIRouter, HTTPException, Depends, status, Request
from schema import MachineModel, UpdateMachineModel
from models import Session, engine, User, Machine
from fastapi.encoders import jsonable_encoder
import datetime
from auth_routes import token_manager




machine_router = APIRouter(prefix="/api/v1.0", tags=["Machines"])

#creating new session for the database
session = Session(bind=engine)



# route to add new machine
@machine_router.post("/new_machine", status_code=status.HTTP_201_CREATED)
async def new_machine(machine:MachineModel, current_user: str = Depends(token_manager)):
    """
    Add a new machine
    """
    
    user = session.query(User).filter_by(email_address=current_user).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    new_machine = Machine(
        machine_name=machine.machine_name,
        machine_model=machine.machine_model,
        machine_serial_number=machine.machine_serial_number,
        machine_manufacturer=machine.machine_manufacturer,
        machine_location=machine.machine_location,
        machine_warranty_expiration_date=machine.machine_warranty_expiration_date,
        machine_purchase_date=machine.machine_purchase_date,
        machine_operational_hours=machine.machine_operational_hours,
        machine_error_logs=machine.machine_error_logs,
        machine_description=machine.machine_description,
        machine_images=machine.machine_images,
        user_id=user.id
    )

    session.add(new_machine)
    session.commit()

    return {"message": "new machine created succesfully"}


#route to get all machines
@machine_router.get("/all_machines", status_code=status.HTTP_200_OK)
async def all_machines(current_user: str = Depends(token_manager)):
        """
        Get all machines
        """
    
        user = session.query(User).filter_by(email_address=current_user).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        all_machines = session.query(Machine).filter_by(user_id=user.id).all()

        return jsonable_encoder(all_machines)



#route to get a machine
@machine_router.get("/machine/{machine_serial_number}", status_code=status.HTTP_200_OK)
async def one_machine(machine_serial_number:int, request:Request, current_user: str = Depends(token_manager)):
        """
        Get a specific machine by machine serial number
        """

        user = session.query(User).filter_by(email_address=current_user).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        machine_serial_number = request.path_params['machine_serial_number']
        
        machine = session.query(Machine).filter_by(user_id=user.id, machine_serial_number=machine_serial_number).first()
        print(machine_serial_number)

        if not machine:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")

        return jsonable_encoder(machine)

#route to update a machine
@machine_router.put("/update_machine/{machine_serial_number}", status_code=status.HTTP_200_OK)
async def update_machine(machine_serial_number:str, machine:UpdateMachineModel, current_user: str = Depends(token_manager)):
        """
         Update a machine
        """
    
       

        user = session.query(User).filter_by(email_address=current_user).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        
        machine_to_update = session.query(Machine).filter_by(user_id=user.id, machine_serial_number=machine_serial_number).first()

        if not machine:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")
        
        

        machine_to_update.machine_error_logs = machine.machine_error_logs
        machine_to_update.machine_description = machine.machine_description
        machine_to_update.machine_operational_hours = machine.machine_operational_hours
        machine_to_update.date_updated = datetime.datetime.utcnow()


        session.commit()
        return {"message": "machine data updated"}


#route to delete a machine
@machine_router.delete("/delete_machine/{machine_serial_number}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_machine(machine_serial_number:str,  current_user: str = Depends(token_manager)):
        """
         Delete a machine
        """
    
       

        user = session.query(User).filter_by(email_address=current_user).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        machine_to_delete = session.query(Machine).filter_by(user_id=user.id, machine_serial_number=machine_serial_number).first()

        if not machine_to_delete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")
        

        session.delete(machine_to_delete)
        session.commit()
        return {"message":f"{machine_to_delete.machine_name} is deleted successfully!"}
    