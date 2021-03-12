
from controller.member_controller import MemberController
from model.database import DatabaseEngine
from vue.admin_vue import AdminVue


def main():
    print("Welcome to the Shop")

    # Init db
    database_engine = DatabaseEngine(url='sqlite:///shop.db')
    database_engine.create_database()
    admin_controller = MemberController(database_engine)
    AdminVue(admin_controller).admin_shell()


if __name__ == "__main__":
    main()
