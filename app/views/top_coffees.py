from utils.fetch import run_query
from utils.typography import text, title

# ================================
#
#   Dekker brukerhistorie NR. 3
#
# ================================


# Top Coffees View
def top_coffees():
    print(title("Her er topp 10 beste kaffer for prisen"))

    for count, coffee in enumerate(find_coffee_toplist()):
        print(
            text(
                f"""{count+1}: {coffee.get('ferdigbrentkaffe_navn')} av {coffee.get('brenneri_navn')} 
       Pris: {coffee.get('ferdigbrentkaffe_kilopris')}  Poeng: {round(coffee.get('ferdigbrentkaffe_poeng'), 1)}"""
            )
        )


# Query
def find_coffee_toplist():
    return run_query(
        """
        SELECT Brenneri.Navn as brenneri_navn, 
               FerdigbrentKaffe.Navn as ferdigbrentkaffe_navn,
               FerdigbrentKaffe.Kilopris as ferdigbrentkaffe_kilopris, 
               AVG(Poeng) as ferdigbrentkaffe_poeng
        FROM Kaffesmaking 
        JOIN FerdigbrentKaffe ON FerdigbrentKaffe_FerdigbrentKaffeID = FerdigbrentKaffeID 
        JOIN Brenneri ON BrenneriID = Brenneri_BrenneriID 
        GROUP BY FerdigbrentKaffeID 
        ORDER BY AVG(Poeng)/kilopris DESC
        LIMIT 10
        """
    )
