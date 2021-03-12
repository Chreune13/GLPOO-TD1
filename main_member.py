
from model.database import DatabaseEngine
from controller.member_controller import MemberController
from vue.admin_vue import AdminVue
from exceptions import Error


def main():
    print("Welcome to the Shop")

    # Init db
    database_engine = DatabaseEngine(url='sqlite:///shop.db')
    database_engine.create_database()
    member_controller = MemberController(database_engine)
    admin_vue = AdminVue(member_controller)

    try:
        member = admin_vue.add_member("customer")
        admin_vue.show_member(member)
    except Error as e:
        admin_vue.error_message(str(e))


if __name__ == "__main__":
    main()
