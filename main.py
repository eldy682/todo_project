from db.init_db import init_db
import menus as men


init_db()

def main():
    men.main_menu()

if __name__ == "__main__":
    main()