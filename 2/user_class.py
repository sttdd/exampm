from sqlalchemy import Column, func, Integer, Date, String, ForeignKey, create_engine, nulls_last
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

#Класс подключения к БД
class Connect:
    @staticmethod
    def create_connection():
        engine = create_engine("postgresql://postgres:1234@localhost:5432/zxc10")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        return Session()

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    employees = relationship('Employee', back_populates='company')

class Position(Base):
    __tablename__ = 'positions'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    employees = relationship('Employee', back_populates='position')

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    s_pasport = Column(Integer, nullable=False)
    n_pasport = Column(Integer, nullable=False)
    adres = Column(String, nullable=False)
    data_nach = Column(Date, nullable=False, default=func.current_date)
    position_id = Column(Integer, ForeignKey('positions.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))
    position = relationship('Position', back_populates='employees')
    company = relationship('Company', back_populates='employees')