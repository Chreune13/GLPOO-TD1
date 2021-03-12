import uuid
from sqlalchemy.ext.declarative import declarative_base

""" base class from which all mapped classes should inherit """
Base = declarative_base()


def generate_id():
    return str(uuid.uuid4())
