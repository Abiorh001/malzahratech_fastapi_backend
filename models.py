from sqlalchemy import Column, String, Text, DateTime, Date, Integer, DECIMAL, ForeignKey, create_engine, Float
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
import uuid
from datetime import datetime
from sqlalchemy_utils import ChoiceType
from sqlalchemy import MetaData





#creating engine for sqlalchemy database uri
engine = create_engine("mysql+pymysql://root:Lucifer_001@localhost:3306/fastapi_malzahratech", echo=True)


metadata = MetaData()
Base = declarative_base(metadata=metadata)
#creating a session
Session = sessionmaker()


# creating table model
class User(Base):
    __tablename__ = "user"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150))
    role = Column(String(150), default="user")
    phone_number = Column(String(150))
    email_address = Column(String(150), nullable=False, unique=True)
    password = Column(String(225), nullable=False)
    street_address = Column(String(150), nullable=False)
    city = Column(String(150), nullable=False)
    state = Column(String(150), nullable=False)
    zip_code = Column(String(50), nullable=False)
    country = Column(String(150), nullable=False)
    reset_token = Column(String(128), default=None)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow)

    machines = relationship('Machine', backref='user', lazy='dynamic', cascade="delete")
    machine_maintenance_reports = relationship('MachineMaintenanceReport', backref='user', lazy='dynamic', cascade='delete')
    maintenance_report_notifications = relationship('MaintenanceNotification', backref='user', lazy='dynamic', cascade='delete')
    maintenance_schedules = relationship('MaintenanceSchedule', backref='user', lazy='dynamic', cascade='delete')


class Machine(Base):
    __tablename__ = 'machine'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    machine_name = Column(String(150), nullable=False)
    machine_model = Column(String(150), nullable=False)
    machine_serial_number = Column(String(150), nullable=False)
    machine_manufacturer = Column(String(150), nullable=False)
    machine_location = Column(String(150), nullable=False)
    machine_warranty_expiration_date = Column(Date)
    machine_purchase_date = Column(Date)
    machine_operational_hours = Column(Integer)
    machine_error_logs = Column(Text)
    machine_description = Column(Text)
    machine_images = Column(Text)
    user_id = Column(String(36), ForeignKey('user.id'))
    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow)

    machine_maintenance_reports = relationship('MachineMaintenanceReport', backref='machine', lazy='dynamic', cascade='delete')
    maintenance_report_notifications = relationship('MaintenanceNotification', backref='machine', lazy='dynamic', cascade='delete')
    maintenance_schedule = relationship('MaintenanceSchedule', backref='machine', lazy='dynamic', cascade='delete')


class MachineMaintenanceReport(Base):
    __tablename__ = "machine_maintenance_report"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    maintenance_task_problem = Column(Text, nullable=False)
    technician_name = Column(String(150), nullable=False)
    maintenance_type = Column(String(150), nullable=False)
    report_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    maintenance_task_solution = Column(Text)
    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime)
    labor_hours = Column(DECIMAL(10, 2))
    parts_cost = Column(DECIMAL(10, 2))
    additional_notes = Column(Text)
    user_id = Column(String(36), ForeignKey('user.id'))
    machine_id = Column(String(36), ForeignKey('machine.id'))
    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow)


class MaintenanceNotification(Base):
    __tablename__ = 'maintenance_notification'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    description = Column(Text)
    status = Column(String(150), nullable=False)
    notification_datetime = Column(DateTime)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String(36), ForeignKey('user.id'))
    machine_id = Column(String(36), ForeignKey('machine.id'))


class MaintenanceSchedule(Base):

    Status = (
        ("PENDING", "pending"),
        ("COMPLETED", "completed")
    )
    __tablename__ = 'maintenance_schedule'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    schedule_date = Column(DateTime, nullable=False)
    notes = Column(Text)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String(36), ForeignKey('user.id'))
    machine_id = Column(String(36), ForeignKey('machine.id'))
    schedule_tasks = Column(Text)
    status = Column(ChoiceType(choices=Status), default="PENDING")
    technician_name = Column(String(150))


class Workorder(Base):
    __tablename__ = "workorder"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    work_order_id = Column(String(50), nullable=False, unique=True)
    machine_id = Column(String(36), ForeignKey('machine.id'))
    work_type = Column(String(50), nullable=False)
    description = Column(Text)
    priority = Column(String(20))
    status = Column(String(20))
    assigned_technician = Column(String(150), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    estimated_hours = Column(Float)
    actual_hours = Column(Float)
    cost = Column(Float)
    additional_notes = Column(Text)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow)


class RevokedToken(Base):
    __tablename__ = 'revoked_tokens'

    id = Column(String(225), primary_key=True)




# class Sparepart(Base):
#     __tablename__ = "sparepart"

#     id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
#     part_name = Column(String(100), nullable=False)
#     description = Column(String(255), nullable=True)
#     quantity = Column(Integer, nullable=False)
#     unit_price = Column(Float, nullable=False)
#     minimum_quantity = Column(Integer, nullable=False)
#     location = Column(String(100), nullable=True)
#     suppliers = relationship("Supplier", back_populates="sparepart")
#     purchase_orders = relationship("PurchaseOrder", back_populates="sparepart")
#     date_created = Column(DateTime, default=datetime.utcnow)
#     date_updated = Column(DateTime, default=datetime.utcnow)

# class Supplier(Base):
#     __tablename__ = "suppliers"

#     id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
#     supplier_name = Column(String(100), nullable=False)
#     contact_person = Column(String(100), nullable=True)
#     phone_number = Column(String(20), nullable=True)
#     email = Column(String(100), nullable=True)
#     sparepart_id = Column(Integer, ForeignKey("sparepart.id"), nullable=False)
#     spareparts = relationship("Sparepart", back_populates="suppliers")
#     date_created = Column(DateTime, default=datetime.utcnow)
#     date_updated = Column(DateTime, default=datetime.utcnow)

# class PurchaseOrder(Base):
#     __tablename__ = "purchase_orders"

#     id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
#     sparepart_id = Column(Integer, ForeignKey("sparepart.id"), nullable=False)
#     supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
#     quantity = Column(Integer, nullable=False)
#     total_price = Column(Float, nullable=False)
#     date_ordered = Column(DateTime, default=datetime.utcnow)
#     spareparts = relationship("Part", back_populates="purchase_orders")
#     supplier = relationship("Supplier")
#     date_created = Column(DateTime, default=datetime.utcnow)
#     date_updated = Column(DateTime, default=datetime.utcnow)

# class PurchaseRequest(Base):
#     __tablename__ = "purchase_requests"

#     id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
#     sparepart_id = Column(Integer, ForeignKey("sparepart.id"), nullable=False)
#     quantity = Column(Integer, nullable=False)
#     date_created = Column(DateTime, default=datetime.utcnow)
#     date_updated = Column(DateTime, default=datetime.utcnow)
#     spareparts = relationship("sparepart")

# class RequestForQuote(Base):
#     __tablename__ = "requestforquote"

#     id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
#     sparepart_id = Column(Integer, ForeignKey("sparepart.id"), nullable=False)
#     description = Column(String(255), nullable=True)
#     spareparts = relationship("Sparepart")
#     date_created = Column(DateTime, default=datetime.utcnow)
#     date_updated = Column(DateTime, default=datetime.utcnow)

# class RequestForProposal(Base):
#     __tablename__ = "requestforproposal"

#     id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
#     sparepart_id = Column(Integer, ForeignKey("sparepart.id"), nullable=False)
#     description = Column(String(255), nullable=True)
#     sparepart = relationship("Sparepart")
#     date_created = Column(DateTime, default=datetime.utcnow)
#     date_updated = Column(DateTime, default=datetime.utcnow)
