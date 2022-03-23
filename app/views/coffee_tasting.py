from datetime import datetime

from queries import all_coffees
from simple_term_menu import TerminalMenu
from utils.fetch import run_query
from utils.typography import text, title

# ================================
#
#   Dekker brukerhistorie NR. 1
#
# ================================

# Tasting View
def coffee_tasting(user_id):
    print(title("Finn kaffen du har smakt"))

    # Select coffee by name and brewery from searchable list
    coffees_from_database = all_coffees()

    coffees_menu = list(
        set(
            map(
                lambda coffee: f"{coffee.get('ferdigbrentkaffe_navn')}, {coffee.get('brenneri_navn')}",
                coffees_from_database,
            )
        )
    )
    print(text("Velg kaffe:"))

    # Show terminal menu
    coffee_index = TerminalMenu(coffees_menu, show_search_hint=True).show()

    # Get selected coffee
    coffee = coffees_from_database[coffee_index]

    print(title(f"Du har valgt kaffen {coffee.get('ferdigbrentkaffe_navn')}"))

    tasting_note = input(text("Smaksnotat:"))

    points = None
    while not points or int(points) < 0 or int(points) > 10:
        points = input(text("Poeng (0-10):"))

    # Call database insert mutation
    create_coffee_tasting(
        coffee_id=coffee.get("ferdigbrentkaffe_id"),
        user_id=user_id,
        tasting_data={
            "tasting_note": tasting_note,
            "points": points,
            "date": datetime.now().date(),
        },
    )

    print(title("Smaksnotat opprettet"))


# Find coffee query
def find_coffee(coffee_name=None, brewery_name=None):
    coffee = None

    try:
        brewery_id = run_query(
            f"""
            SELECT BrenneriID as brenneri_id FROM Brenneri WHERE Navn = "{brewery_name}"
            """
        )[0].get("brenneri_id")
    except:
        return False

    try:
        coffee = run_query(
            f"""
            SELECT FerdigbrentKaffeID as ferdigbrentkaffe_id, FerdigbrentKaffe.Navn as ferdigbrentkaffe_navn
            FROM FerdigbrentKaffe WHERE FerdigbrentKaffe.Navn = "{coffee_name}" AND Brenneri_BrenneriID = {brewery_id}
            """
        )[0]
    except:
        return False

    return coffee


# Coffee tasting mutation
def create_coffee_tasting(coffee_id, user_id, tasting_data=None):
    tasting_note = tasting_data["tasting_note"]
    points = tasting_data["points"]
    date = tasting_data["date"]

    run_query(
        f"""
        INSERT INTO Kaffesmaking (Smaksnotater, Poeng, Dato, FerdigbrentKaffe_FerdigbrentKaffeID, Bruker_BrukerID)
        VALUES ("{tasting_note}", {points}, "{date}", {coffee_id}, {user_id})
        """
    )
