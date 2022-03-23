from simple_term_menu import TerminalMenu

from queries import all_countries
from utils.fetch import run_query
from utils.typography import text


# Flexible coffee filtration method
# Made to easily enable more filters
def coffee_filter(filters):

    # Selected filters as booleans
    # [0: "Beskrivelse", 1: "Land", 2: "Foredlingsmetode"]
    filter_description = 0 in filters
    filter_country = 1 in filters
    filter_refinement = 2 in filters

    # Result container
    coffees = []

    # Init filter inputs
    countries = []
    descripton = " "
    refinement = " "

    # Database selection views for filtration
    selectors = []

    if filter_country:
        print(text("Velg land:"))
        # User select countries
        all_countries_result = all_countries()
        countries = list(
            map(
                lambda index: all_countries_result[index].get("land_navn"),
                TerminalMenu(
                    list(
                        map(
                            lambda country: country.get("land_navn"),
                            all_countries_result,
                        )
                    ),
                    multi_select=True,
                    show_multi_select_hint=True,
                ).show(),
            )
        )
        # Create selector
        selectors.append(
            f"""SelectedFarms AS (
            SELECT GårdID as ID FROM Gård
            JOIN Region ON RegionID = Region_RegionID
            JOIN Land ON LandID = Land_LandID
            WHERE {" OR "
            .join(map(lambda country: f"Land.Navn = '{country}'", countries))}
            )"""
        )

    if filter_description:
        descripton = input(text("Beskrivelsefilter:"))

        # Create selector
        selectors.append(
            f"""SelectedDescriptions AS (
            SELECT FerdigbrentKaffe.FerdigbrentKaffeID as ID from Kaffesmaking
            JOIN FerdigbrentKaffe ON FerdigbrentKaffeID = FerdigbrentKaffe_FerdigbrentKaffeID
            WHERE Kaffesmaking.Smaksnotater LIKE('%{descripton}%') OR FerdigbrentKaffe.Beskrivelse
            LIKE('%{descripton}%')
            ) """
        )

    if filter_refinement:
        print(text("Foredlingsfilter"))
        refinement = input(text("(skriv '!' foran søk for å eksludere):"))

        # Create selector
        selectors.append(
            f""" SelectedRefinements AS (
            SELECT ForedlingsmetodeID as ID FROM Foredlingsmetode
            WHERE Foredlingsmetode.Navn {"NOT" if refinement[0] == "!" else ""} LIKE('%{refinement.replace("!", "")}%')
            )"""
        )

    # Build querystring
    query = "WITH "

    # Add selectors
    query += ", ".join(selectors)

    query += """
        SELECT FerdigbrentKaffe.Navn as ferdigbrentkaffe_navn, Brenneri.Navn as brenneri_navn FROM FerdigbrentKaffe
        JOIN Brenneri ON Brenneri_BrenneriID = BrenneriID
        """
    if filter_country or filter_refinement:
        query += " JOIN Kaffeparti ON KaffepartiID = Kaffeparti_KaffepartiID"
    if filter_country:
        query += " JOIN SelectedFarms ON SelectedFarms.ID = Gård_GårdID"
    if filter_description:
        query += (
            " JOIN SelectedDescriptions ON SelectedDescriptions.ID = FerdigbrentKaffeID"
        )
    if filter_refinement:
        query += " JOIN SelectedRefinements ON SelectedRefinements.ID = Foredlingsmetode_ForedlingsmetodeID"

    # Ensure no duplicates
    query += " GROUP BY FerdigbrentKaffeID"

    coffees = run_query(query)

    return coffees
