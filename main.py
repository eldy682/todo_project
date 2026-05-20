import repo.task_repo as db
import menus as men


db.init_db()

def main():
    men.main_menu()

if __name__ == "__main__":
    main()