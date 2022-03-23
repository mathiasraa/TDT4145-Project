from simple_term_menu import TerminalMenu
from queries import log_in, register

from utils.typography import title

def authorization_login():

    print(title("Logg inn"))

    email = input("Epost: ")
    password = input("Password: ")
    result = log_in(email, password)

    if result[0] == True:
        print(title("Du er logget inn"))

        return result
    else:
        print(title(result[1] + ", vil du prøve på nytt?"))

        terminal_menu = TerminalMenu(["Ja", "Nei"])

        choice = terminal_menu.show()

        if choice == 0:
            authorization_login()
        if choice == 1:
            return result


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
            return result
    else:

        print(title(result[1]+ ", vil du prøve på nytt?"))

        terminal_menu = TerminalMenu(["Ja", "Nei"])
        choice = terminal_menu.show()

        if choice == 0:
            return authorization_register()
        if choice == 1:
            return result


def authorization():

    terminal_menu = TerminalMenu(["Logg inn", "Registrer"])
    choice = terminal_menu.show()

    if choice == 0:
        return authorization_login()
    if choice == 1:
        return authorization_register()