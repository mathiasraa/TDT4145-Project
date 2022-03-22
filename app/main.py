from secrets import choice
from simple_term_menu import TerminalMenu
from queries import log_in, register

from coffee_search import search_by_description, search_by_name_brewery
from queries import (
    all_breweries,
    all_coffees,
    create_coffee_tasting,
    find_coffee,
    find_coffee_toplist,
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
            "Se topp 10 rimlige kaffer",
            "Se topp 10 brukere",
        ]
    )

    choice = terminal_menu.show()

    return choice


def coffee_tasting():
    print(title("Finn kaffen du har smakt"))

    coffees = list(set(map(lambda coffee: coffee[1], all_coffees())))
    breweries = list(map(lambda coffee: coffee[1], all_breweries()))

    print(title("Kaffenavn:"))
    coffee = TerminalMenu(coffees, show_search_hint=True).show()
    print(title("Brennerinavn:"))
    brewery = TerminalMenu(breweries, show_search_hint=True).show()

    coffee = find_coffee(coffees[coffee], breweries[brewery])

    print(title(f"Du har valgt kaffen {coffee}"))

    # tasting_note = input(text("Smaksnotat:"))
    # points = input("Poeng:")

    # create_coffee_tasting(
    #     coffee_id=coffee[0],
    #     tasting_data={"tasting_note": tasting_note, "points": points},
    # )

    # print(title("Smaksnotat opprettet"))


def coffee_search():
    print(title("Velg type søk"))

    terminal_menu = TerminalMenu(
        ["Søk etter navn og brenneri", "Søk etter beskrivelse"],
        multi_select=True,
        show_multi_select_hint=True,
    )

    search_menu = terminal_menu.show()
    if search_menu == 0:
        print(search_by_name_brewery())
    elif search_menu == 1:
        print(search_by_description())


def coffee_toplist():
    print(title("Her er topp 10 beste kaffer for prisen"))

    for count, coffee in enumerate(find_coffee_toplist()):
        print(
            text(f"{count+1}: {coffee[1]} {coffee[2]} pris {coffee[3]} poeng"))


def authorization_login():

    print(title("Logg inn"))

    email = input("Epost: ")
    password = input("Password: ")
    result = log_in(email, password)

    if result[0]:
        print(title("Du er logget inn"))
        return(result[1])
    else:
        print(title(result[1] + " Vil du prøve på nytt?"))

        terminal_menu = TerminalMenu(
            [
                "Ja",
                "Nei"
            ]
        )
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

        terminal_menu = TerminalMenu(
            [
                "Ja",
                "Nei"
            ]
        )
        choice = terminal_menu.show()

        if choice == 0:
            authorization_login()
        if choice == 1:
            return False
    else:

        print(title("Noe gikk galt, vil du prøve på nytt?"))

        terminal_menu = TerminalMenu(
            [
                "Ja",
                "Nei"
            ]
        )
        choice = terminal_menu.show()

        if choice == 0:
            authorization_register()
        if choice == 1:
            return False



def authorization():

    terminal_menu = TerminalMenu(
        [
            "Logg inn",
            "Registrer"
        ]
    )
    choice = terminal_menu.show()

    if choice == 0:
        authorization_login()
    if choice == 1:
        authorization_register()


def program():
    while True:

        user_id = authorization()

        if user_id == False: break



        choice = show_menu()

        if choice == 0:
            coffee_search()
        if choice == 1:
            coffee_tasting()
        if choice == 2:
            coffee_toplist()

        print(title("Vil du fortsette?"))

        terminal_menu = TerminalMenu(["Gå til hovedmeny", "Avslutt program"])

        continue_menu = terminal_menu.show()
        if continue_menu == 1:
            print(text("Ses neste gang!"))
            break


program()
