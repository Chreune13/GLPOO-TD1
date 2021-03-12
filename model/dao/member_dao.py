from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from model.mapping.member import Member
from model.dao.dao import DAO

from exceptions import Error, ResourceNotFound


class MemberDAO(DAO):
    """
    Member Mapping DAO
    """

    def __init__(self, database_session):
        super().__init__(database_session)

    def get(self, id):
        try:
            return self._database_session.query(Member).filter_by(id=id).order_by(Member.firstname).one()
        except NoResultFound:
            raise ResourceNotFound()

    def get_all(self):
        try:
            return self._database_session.query(Member).order_by(Member.firstname).all()
        except NoResultFound:
            raise ResourceNotFound()

    def get_by_name(self, firstname: str, lastname: str):
        try:
            return self._database_session.query(Member).filter_by(firstname=firstname, lastname=lastname)\
                .order_by(Member.firstname).one()
        except NoResultFound:
            raise ResourceNotFound()

    def create(self, data: dict):
        try:
            member = Member(firstname=data.get('firstname'), lastname=data.get('lastname'), email=data.get('email'), type=data.get('type'))
            self._database_session.add(member)
            self._database_session.flush()
        except IntegrityError:
            raise Error("Member already exists")
        return member

    def update(self, member: Member, data: dict):
        if 'firstname' in data:
            member.firstname = data['firstname']
        if 'lastname' in data:
            member.lastname = data['lastname']
        if 'email' in data:
            member.email = data['email']
        if 'type' in data:
            member.type = data['type']
        try:
            self._database_session.merge(member)
            self._database_session.flush()
        except IntegrityError:
            raise Error("Error data may be malformed")
        return member

    def delete(self, entity):
        try:
            self._database_session.delete(entity)
        except SQLAlchemyError as e:
            raise Error(str(e))
