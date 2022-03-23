from queries import log_in, register
from simple_term_menu import TerminalMenu
from utils.typography import text, title


def authorization_login():

    print()
    print(title("Logg inn"))

    

    email = input(text("Epost: "))
    password = input(text("Password: "))

    #Running function to check if email and password corresponds to data from database
    #Returns tuple (True, BrukerID) if logged in, and (False, Error Message) if not
    result = log_in(email, password)

    if result[0] == True:
        print(title("Du er logget inn"))

        #Return (True, BrukerID)
        return result
    else:
        print(title(result[1] + ", vil du prøve på nytt?"))

        terminal_menu = TerminalMenu(["Ja", "Nei"])

        choice = terminal_menu.show()

        #Ja = 0, Nei = 1

        if choice == 0:
            #Try login again
            authorization_login()
        if choice == 1:
            #Return (False, Error Message)
            return result


def authorization_register():

    print(title("Registrer"))

    email = input(text("Epost: "))
    password = input(text("Password: "))
    first_name = input(text("Fornavn: "))
    last_name = input(text("Etternavn: "))

    #Running function to register user
    #Returns tuple (True, Created Message)
    result = register(email, password, first_name, last_name)

    if result[0] ==True:

        print(title(result[1]))
        print(title("Vil du logge inn?"))

        terminal_menu = TerminalMenu(["Ja", "Nei"])
        choice = terminal_menu.show()

        #Ja = 0, Nei = 1

        if choice == 0:
            #Run login function
            return authorization_login()
        if choice == 1:
            #User does not want to log in so return False instead of True
            return False, result[1]
    else:
        #Print error message
        print(title(result[1] + ", vil du prøve på nytt?"))

        terminal_menu = TerminalMenu(["Ja", "Nei"])
        choice = terminal_menu.show()

        #Ja = 0, Nei = 1

        if choice == 0:
            return authorization_register()
        if choice == 1:
            return result


def authorization():
    print()

    terminal_menu = TerminalMenu(["Logg inn", "Registrer"])
    choice = terminal_menu.show()

    #Logg inn = 0, Registrer = 1

    if choice == 0:
        return authorization_login()
    if choice == 1:
        return authorization_register()
