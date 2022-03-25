from utils.fetch import run_query
from utils.typography import text, title

# ================================
#
#   Dekker brukerhistorie NR. 2
#
# ================================


# User Toplist View
def top_users():
    print(title("Topp 10 brukere i antall smakingsregistreringer"))

    for count, user in enumerate(find_user_toplist()):
        print(
            text(
                f"{count+1}: Navn: {user.get('bruker_fornavn')} {user.get('bruker_etternavn')}  Antall: {user.get('antall')}"
            )
        )


# Query
def find_user_toplist():
    return run_query(
        """
        SELECT 
            Bruker.Fornavn as bruker_fornavn, 
            Bruker.Etternavn as bruker_etternavn, 
            COUNT(DISTINCT FerdigbrentKaffeID) as antall
        FROM Bruker LEFT JOIN Kaffesmaking ON BrukerID = Bruker_BrukerID 
        LEFT JOIN FerdigbrentKaffe ON FerdigbrentKaffeID = FerdigbrentKaffe_FerdigbrentKaffeID
        WHERE Kaffesmaking.Dato > '2022-01-01' AND Kaffesmaking.Dato < '2023-01-01' OR Kaffesmaking.Dato IS NULL
        GROUP BY BrukerID
        ORDER BY antall DESC
        LIMIT 10
        """
    )


