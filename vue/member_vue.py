from vue.common import Common


class MemberVue:
    """
    Member Vue
    Members interface features
    """

    def __init__(self, member_controller):
        self._common = Common()
        self._member_controller = member_controller

    def add_member(self, user_type):
        # Show subscription formular
        data = {}
        print("Store user Subscription")
        print(user_type)
        print()
        data['firstname'] = self._common.ask_name(key_name="firstname")
        data['lastname'] = self._common.ask_name(key_name="lastname")
        data['email'] = self._common.ask_email()
        if user_type != 'customer':
            data['type'] = self._common.ask_type()
        else:
            data['type'] = user_type
        return self._member_controller.create_member(data)

    def show_member(self, member: dict):
        print("Member profile: ")
        print(member['firstname'].capitalize(), member['lastname'].capitalize())
        print("email:", member['email'])
        print("type:", member['type'])

    def error_message(self, message: str):
        print("/!\\ %s" % message.upper())

    def succes_message(self, message: str = ""):
        print("Operation succeeded: %s" % message)

    def show_members(self):

        members = self._member_controller.list_members()

        print("Members: ")
        for member in members:
            print("* %s %s (%s) - %s" % (   member['firstname'].capitalize(),
                                            member['lastname'].capitalize(),
                                            member['email'],
                                            member['type']))

    def search_member(self):
        firstname = self._common.ask_name('firstname')
        lastname = self._common.ask_name('lastname')
        member = self._member_controller.search_member(firstname, lastname)
        return member

    def update_member(self):
        member = self.search_member()
        data = {}
        print("Update Member")
        print()
        data['firstname'] = self._common.ask_name(key_name="firstname", default=member['firstname'])
        data['lastname'] = self._common.ask_name(key_name="lastname", default=member['lastname'])
        data['email'] = self._common.ask_email(default=member['email'])
        data['type'] = self._common.ask_type(default=member['type'])
        print()
        return self._member_controller.update_member(member['id'], data)

    def delete_member(self):
        member = self.search_member()
        self._member_controller.delete_member(member['id'])
        self.succes_message()
