from models import engine, Base




      
# creating database table/schema
Base.metadata.create_all(bind=engine)



