from queries import find_coffee
from utils.typography import text


def search_by_name_brewery():

    coffee = None

    while True:
        coffee_name = input(text("Kaffenavn:"))
        if coffee_name.lower() == "avbryt":
            break
        brewery_name = input(text("Brennerinavn:"))
        if brewery_name.lower() == "avbryt":
            break

        coffee = find_coffee(coffee_name, brewery_name)
        if coffee:
            coffee = coffee[0]
            break
        else:
            print()
            print(text("Kaffen eksisterer ikke i databasen."))
            print(text("Prøv igjen eller skriv 'avbryt':"))

    return coffee


def search_by_description():
    description = input(text("Beskrivelse:"))

    coffee = find_coffee(description=description)

    return coffee
