from coffee_filter import coffee_filter
from simple_term_menu import TerminalMenu
from utils.typography import text, title

# ================================
#
#   Dekker brukerhistorie NR. 4/5
#
# ================================


# Coffee Search View
def coffee_search():
    print(title("Velg filtreringer"))

    terminal_menu = TerminalMenu(
        ["Beskrivelse", "Land", "Foredlingsmetode"],
        multi_select=True,
        show_multi_select_hint=True,
    )

    search_menu = terminal_menu.show()

    filter_result = coffee_filter(search_menu)
    print(title("Søket ditt ga følgende resultat:"))
    if len(filter_result) == 0:
        print(text("Fant ingen resultater"))

    else:
        for coffee in filter_result:
            print(
                text(
                    f"* Navn: {coffee.get('ferdigbrentkaffe_navn')}  Brenneri: {coffee.get('brenneri_navn')}"
                )
            )
