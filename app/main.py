from simple_term_menu import TerminalMenu

from utils.typography import color, text, title
from views.authorization import authorization
from views.coffee_search import coffee_search
from views.coffee_tasting import coffee_tasting
from views.top_coffees import top_coffees
from views.top_users import top_users


def show_menu():
 

    terminal_menu = TerminalMenu(
        [
            "Søk etter kaffe",
            "Legg til kaffesmaking",
            "Se topp 10 beste kaffer for prisen",
            "Se topp 10 brukere",
            "Avslutt",
        ]
    )

    choice = terminal_menu.show()

    return choice


def main():

    menu = f"""
========================================

    {color.BOLD}{color.YELLOW}Velkommen til KaffeDB{color.END}

    Velg en av handlingene nedenfor

========================================
"""

    print(menu)

    user_data = authorization()
    user_id = user_data[1]


    # Main program loop
    while True:
        if user_data[0] == False:
            break

        choice = show_menu()

        # Initialize selected view
        if choice == 0:
            coffee_search()
        if choice == 1:
            coffee_tasting(user_id=user_id)
        if choice == 2:
            top_coffees()
        if choice == 3:
            top_users()
        if choice == 4:
            print(text("Ses neste gang!"))
            break

        # Handle continuation / exit
        print(title("Vil du fortsette?"))

        terminal_menu = TerminalMenu(["Gå til hovedmeny", "Avslutt program"])

        continue_menu = terminal_menu.show()
        if continue_menu == 1:
            print(text("Ses neste gang!"))
            break


if __name__ == "__main__":
    main()
