from fastapi import APIRouter, status, HTTPException, Depends, Request
from models import Session, engine, User, RevokedToken
from schema import SignUpModel, SignInModel, ForgetPasswordModel, ResetPasswordModel
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import secrets









auth_router = APIRouter(prefix="/api/v1.0", tags=["Authentication"])


#creating new session for the database
session = Session(bind=engine)



#function to check if the jwt token has been revoked or not
async def is_token_revoked(jti: str):
   # Query the database for the token ID
    revoked_token = session.query(RevokedToken).filter_by(id=jti).first()
    return revoked_token is not None

#function to create token manager to use jwt token and confirm user login
async def token_manager(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        jti= Authorize.get_raw_jwt()["jti"]
        

        # Check if the token is revoked
        if await is_token_revoked(jti):
            raise HTTPException(status_code=401, detail="Token has been revoked")
        
        #get the current user
        current_user = Authorize.get_jwt_subject()
        return current_user
        
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or missing token")



@auth_router.get("/")
async def home(current_user: str = Depends(token_manager)):
    # You can now use the current_user in your route logic
    return {"message": f"Hello, {current_user}"}
   


# signup route
@auth_router.post("/auth/sign_up", status_code=status.HTTP_201_CREATED)
async def registration(user:SignUpModel):
    existing_user = session.query(User).filter_by(email_address=user.email_address).first()
    if existing_user is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exist")
     
    else:
        new_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            email_address=user.email_address,
            password=generate_password_hash(user.password),
            street_address=user.street_address,
            city=user.city,
            state=user.state,
            zip_code=user.zip_code,
            country=user.country,
            reset_token=user.reset_token,
            date_created=user.date_created,
            date_updated=user.date_updated,
        )
        session.add(new_user)
        session.commit()
        return {"message":"User created succesfully"}


#login route
@auth_router.post("/auth/sign_in", status_code=status.HTTP_200_OK)
async def sign_in(user:SignInModel, Authorize:AuthJWT=Depends()):

    existing_user = session.query(User).filter_by(email_address=user.email_address).first()
    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email doesn't exist.")
    
    if not check_password_hash(existing_user.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is incorrect.")
    
    access_token = Authorize.create_access_token(subject=existing_user.email_address)
    
    response = {"access_token": access_token}

    return jsonable_encoder(response)



#route for password forget
@auth_router.post("/forget_password", status_code=status.HTTP_202_ACCEPTED)
def forget_password(user:ForgetPasswordModel, request:Request):

    existing_user = session.query(User).filter_by(email_address=user.email_address).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
 
    
    existing_user.reset_token = secrets.token_hex(16)
    #update the reset_token
    session.commit()

    # SMTP server details
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587  
    smtp_username = 'abiolaadedayo1993@gmail.com'
    smtp_password = 'etkazqurxvtqouak'  

    # Create a multipart message
    msg = MIMEMultipart()
    msg["From"] = "abiolaadedayo1993@gmail.com"
    msg["To"] = user.email_address
    msg["Subject"] = "Reset Password"
    # Add the schedule data to the email body

    # Construct the reset URL
    reset_url = str(request.base_url) + "reset_password?reset_token=" + existing_user.reset_token

    # Add the reset URL and token to the email body
    body = f"Reset Password confirmation:\n\nPlease click the link below to reset your password:\n\n{reset_url}"
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
    



#route to reset pasword
@auth_router.post("/rest_password", status_code=status.HTTP_202_ACCEPTED)
def reset_password(user:ResetPasswordModel, reset_token:str):
    existing_user = session.query(User).filter_by(reset_token=reset_token).first()
    if existing_user:
        existing_user.password = generate_password_hash(user.password)
        existing_user.reset_token = None
        session.commit()
        return {"message":"password changed successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="reset token is invalid or missing")


   

# #route to log out user
@auth_router.post("/auth/sign_out")
def sign_out(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        jti = Authorize.get_raw_jwt()["jti"]
        
        # Create a new instance of RevokedToken and save it in the database
        revoked_token = RevokedToken(id=jti)
        session.add(revoked_token)
        session.commit()
        
        
        return {"message": "Logged out successfully"}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or missing token")