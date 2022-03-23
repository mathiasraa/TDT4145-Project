from simple_term_menu import TerminalMenu

from queries import all_countries
from utils.fetch import run_query, run_query_params
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
    countries = ()
    descripton = " "
    refinement = " "

    # Database selection views for filtration
    selectors = []

    params = {}

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

        # Creating selecting arguments like (Land.Navn = country_0 OR Land.Navn = country_1 OR ...)
        args = f"""{" OR ".join(map(
                        lambda country: f"Land.Navn = :country_{countries.index(country)}",
                        countries)
                        )}"""

        # Create selector
        selectors.append(
            f"""SelectedFarms AS (
            SELECT GårdID as ID FROM Gård
            JOIN Region ON RegionID = Region_RegionID
            JOIN Land ON LandID = Land_LandID
            WHERE {args}
            )"""
        )
        # Creating entries in params like (county_0: Country Name)
        for index, country in enumerate(countries):
            params[f"country_{index}"] = f"{country}"

    if filter_description:
        descripton = input(text("Beskrivelsefilter:"))

        descripton = "%" + descripton + "%"

        # Create selector
        selectors.append(
            """SelectedDescriptions AS (
            SELECT FerdigbrentKaffe.FerdigbrentKaffeID as ID from Kaffesmaking
            JOIN FerdigbrentKaffe ON FerdigbrentKaffeID = FerdigbrentKaffe_FerdigbrentKaffeID
            WHERE Kaffesmaking.Smaksnotater LIKE(:description) OR FerdigbrentKaffe.Beskrivelse
            LIKE(:description)
            ) """
        )

        # adding description to params
        params["description"] = descripton

    if filter_refinement:
        print(text("Foredlingsfilter"))
        refinement = input(text("(skriv '!' foran søk for å eksludere):"))

        # adding NOT to query if user types !
        exclude = " NOT" if refinement[0] == "!" else ""

        # removing !
        refinement = "%" + refinement.replace("!", "") + "%"

        # Create selector
        selectors.append(
            f"""SelectedRefinements AS (
            SELECT ForedlingsmetodeID as ID FROM Foredlingsmetode
            WHERE Foredlingsmetode.Navn {exclude} LIKE(:refinement)
            )"""
        )

        # adding refinement to params
        params["refinement"] = refinement

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

    coffees = run_query_params(query, params)

    return coffees
