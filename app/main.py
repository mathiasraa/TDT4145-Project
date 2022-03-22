from simple_term_menu import TerminalMenu

from coffee_filter import coffee_filter
from queries import (
    all_coffees,
    create_coffee_tasting,
    find_coffee,
    find_coffee_toplist,
    find_user_toplist,
    log_in,
    register,
)
from utils.typography import text, title


def show_menu():
    menu = """
========================================

    Velkommen til KaffeDB

    Velg en av handlingene nedenfor

========================================
"""

    print(menu)

    terminal_menu = TerminalMenu(
        [
            "Søk etter kaffe",
            "Legg til kaffesmaking",
            "Se topp 10 beste kaffer for prisen",
            "Se topp 10 brukere",
        ]
    )

    choice = terminal_menu.show()

    return choice


def coffee_tasting(user_id):
    print(title("Finn kaffen du har smakt"))

    coffees = list(set(map(lambda coffee: f"{coffee[1]}, {coffee[2]}", all_coffees())))
    print(text("Velg kaffe:"))
    coffee_index = TerminalMenu(coffees, show_search_hint=True).show()

    coffee = find_coffee(
        coffees[coffee_index].split(", ")[0], coffees[coffee_index].split(", ")[1]
    )

    print(title(f"Du har valgt kaffen {coffee[0][1]}"))

    tasting_note = input(text("Smaksnotat:"))
    points = None
    while not points or int(points) < 0 or int(points) > 10:
        points = input(text("Poeng (0-10):"))

    create_coffee_tasting(
        coffee_id=coffee[0][0],
        user_id=user_id,
        tasting_data={"tasting_note": tasting_note, "points": points},
    )

    print(title("Smaksnotat opprettet"))


def coffee_search():
    print(title("Velg filtreringer"))

    terminal_menu = TerminalMenu(
        ["Beskrivelse", "Land", "Foredlingsmetode"],
        multi_select=True,
        show_multi_select_hint=True,
    )

    search_menu = terminal_menu.show()

    print(coffee_filter(search_menu))


def coffee_toplist():
    print(title("Her er topp 10 beste kaffer for prisen"))

    for count, coffee in enumerate(find_coffee_toplist()):
        print(text(f"{count+1}: {coffee[1]} {coffee[2]} pris {coffee[3]} poeng"))


def user_toplist():
    print(title("Her er topp 10 beste kaffer for prisen"))

    for count, user in enumerate(find_user_toplist()):
        print(text(f"{count+1}: Navn: {user[0]} {user[1]} Antall: {user[2]}"))


def authorization_login():

    print(title("Logg inn"))

    email = input("Epost: ")
    password = input("Password: ")
    result = log_in(email, password)

    if result[0] == True:
        print(title("Du er logget inn"))
        user_id = result[1]

        return user_id
    else:
        print(title(result[1] + " Vil du prøve på nytt?"))

        terminal_menu = TerminalMenu(["Ja", "Nei"])

        choice = terminal_menu.show()

        if choice == 0:
            authorization_login()
        if choice == 1:
            return False


def authorization_register():

    print(title("Registrer"))

    email = input("Epost: ")
    password = input("Password: ")
    first_name = input("Fornavn: ")
    last_name = input("Etternavn: ")

    result = register(email, password, first_name, last_name)

    if result[0]:

        print(title("Vil du logge inn?"))

        terminal_menu = TerminalMenu(["Ja", "Nei"])
        choice = terminal_menu.show()

        if choice == 0:
            return authorization_login()
        if choice == 1:
            return False
    else:

        print(title("Noe gikk galt, vil du prøve på nytt?"))

        terminal_menu = TerminalMenu(["Ja", "Nei"])
        choice = terminal_menu.show()

        if choice == 0:
            return authorization_register()
        if choice == 1:
            return False


def authorization():

    terminal_menu = TerminalMenu(["Logg inn", "Registrer"])
    choice = terminal_menu.show()

    if choice == 0:
        return authorization_login()
    if choice == 1:
        return authorization_register()


def program():

    user_id = authorization()

    while True:
        if str(user_id) == "False":
            break

        choice = show_menu()

        if choice == 0:
            coffee_search()
        if choice == 1:
            coffee_tasting(user_id=user_id)
        if choice == 2:
            coffee_toplist()
        if choice == 3:
            user_toplist()

        print(title("Vil du fortsette?"))

        terminal_menu = TerminalMenu(["Gå til hovedmeny", "Avslutt program"])

        continue_menu = terminal_menu.show()
        if continue_menu == 1:
            print(text("Ses neste gang!"))
            break


program()
