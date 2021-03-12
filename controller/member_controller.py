import re

from model.dao.member_dao import MemberDAO
from exceptions import Error, InvalidData


class MemberController:
    """
    Member actions
    """

    def __init__(self, database_engine):
        self._database_engine = database_engine
        self._frames = []

    def list_members(self):
        with self._database_engine.new_session() as session:
            members = MemberDAO(session).get_all()
            members_data = [member.to_dict() for member in members]
        return members_data

    def get_member(self, member_id):
        with self._database_engine.new_session() as session:
            member = MemberDAO(session).get(member_id)
            member_data = member.to_dict()
        return member_data

    def create_member(self, data):

        self._check_profile_data(data)
        try:
            with self._database_engine.new_session() as session:
                # Save member in database
                member = MemberDAO(session).create(data)
                member_data = member.to_dict()
                return member_data
        except Error as e:
            # log error
            raise e

    def update_member(self, member_id, member_data):

        self._check_profile_data(member_data, update=True)
        with self._database_engine.new_session() as session:
            member_dao = MemberDAO(session)
            member = member_dao.get(member_id)
            member = member_dao.update(member, member_data)
            return member.to_dict()

    def delete_member(self, member_id):

        with self._database_engine.new_session() as session:
            member_dao = MemberDAO(session)
            member = member_dao.get(member_id)
            member_dao.delete(member)

    def search_member(self, firstname, lastname):

        # Query database
        with self._database_engine.new_session() as session:
            member_dao = MemberDAO(session)
            member = member_dao.get_by_name(firstname, lastname)
            return member.to_dict()

    def _check_profile_data(self, data, update=False):
        name_pattern = re.compile("^[\S-]{2,50}$")
        type_pattern = re.compile("^(customer|seller)$")
        email_pattern = re.compile("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$")
        mandatories = {
            'firstname': {"type": str, "regex": name_pattern},
            'lastname': {"type": str, "regex": name_pattern},
            'email': {"type": str, "regex": email_pattern},
            'type': {"type": str, "regex": type_pattern}
        }
        for mandatory, specs in mandatories.items():
            if not update:
                if mandatory not in data or data[mandatory] is None:
                    raise InvalidData("Missing value %s" % mandatory)
            else:
                if mandatory not in data:
                    continue
            value = data[mandatory]
            if "type" in specs and not isinstance(value, specs["type"]):
                raise InvalidData("Invalid type %s" % mandatory)
            if "regex" in specs and isinstance(value, str) and not re.match(specs["regex"], value):
                raise InvalidData("Invalid value %s" % mandatory)
