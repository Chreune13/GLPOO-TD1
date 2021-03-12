from model.mapping import Base, generate_id

from sqlalchemy import Column, String, UniqueConstraint


class Member(Base):
    __tablename__ = 'members'
    __table_args__ = (UniqueConstraint('firstname', 'lastname'),)

    id = Column(String(36), default=generate_id, primary_key=True)

    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)

    email = Column(String(256), nullable=False)
    type = Column(String(10), nullable=False)

    def __repr__(self):
        return "<Member(%s %s %s)>" % (self.firstname, self.lastname.upper(), self.type)

    def to_dict(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "type": self.type
        }
