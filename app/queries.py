import sqlite3

from utils.fetch import run_query


def run_query_old(query):
    connection = sqlite3.connect("kaffedb.db")

    cursor = connection.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()
    connection.commit()
    connection.close()

    return rows


def find_coffee(coffee_name=None, brewery_name=None):
    coffee = None

    try:
        brewery_id = run_query(
            f"""
            SELECT BrenneriID as brenneri_id FROM Brenneri WHERE Navn = "{brewery_name}"
            """
        ).get("brenneri_id")
    except:
        return False

    try:
        coffee = run_query(
            f"""
            SELECT FerdigbrentKaffeID as ferdigbrentkaffe_id, FerdigbrentKaffe.Navn as ferdigbrentkaffe_navn
            FROM FerdigbrentKaffe WHERE FerdigbrentKaffe.Navn = "{coffee_name}" AND Brenneri_BrenneriID = {brewery_id}
            """
        )
    except:
        return False

    return coffee


def create_coffee_tasting(coffee_id, user_id, tasting_data=None):
    tasting_note = tasting_data["tasting_note"]
    points = tasting_data["points"]
    date = tasting_data["date"]

    run_query_old(
        f"""
        INSERT INTO Kaffesmaking (Smaksnotater, Poeng, Dato, FerdigbrentKaffe_FerdigbrentKaffeID, Bruker_BrukerID)
        VALUES ("{tasting_note}", {points}, "{date}", {coffee_id}, {user_id})
        """
    )


def find_coffee_toplist():
    return run_query_old(
        """
        SELECT Brenneri.Navn, FerdigbrentKaffe.Navn, FerdigbrentKaffe.Kilopris, AVG(Poeng) 
        from Kaffesmaking 
        join FerdigbrentKaffe on FerdigbrentKaffe_FerdigbrentKaffeID = FerdigbrentKaffeID 
        join Brenneri on BrenneriID = Brenneri_BrenneriID 
        GROUP BY FerdigbrentKaffeID 
        ORDER BY kilopris/AVG(Poeng)
        LIMIT 10
        """
    )


def all_countries():
    return run_query_old(
        """
        SELECT Navn FROM Land
        """
    )


def find_user_toplist():
    return run_query_old(
        """
        SELECT Bruker.Fornavn, Bruker.Etternavn, COUNT(DISTINCT FerdigbrentKaffeID) as Score
        FROM Bruker LEFT JOIN Kaffesmaking ON BrukerID = Bruker_BrukerID 
        LEFT JOIN FerdigbrentKaffe ON FerdigbrentKaffeID = FerdigbrentKaffe_FerdigbrentKaffeID 
        GROUP BY BrukerID
        ORDER BY Score DESC
        LIMIT 10
        """
    )


def all_coffees():
    return run_query_old(
        """
        SELECT FerdigbrentKaffeID, FerdigbrentKaffe.Navn, Brenneri.Navn FROM FerdigbrentKaffe
        JOIN Brenneri on BrenneriID = Brenneri_BrenneriID
        """
    )


def all_breweries():
    return run_query_old(
        """
        SELECT BrenneriID, Navn FROM Brenneri
        """
    )


def log_in(email, password):

    user_data = run_query_old(
        f"""
        SELECT BrukerID, Passord from Bruker where Epost = "{email}"
        """
    )
    if not user_data:
        return False, "Kan ikke finne bruker"
    else:
        if password == user_data[0][1]:
            return True, user_data[0][0]
        else:
            return False, "Feil passord"


def register(email, password, first_name, last_name):

    try:
        run_query_old(
            f"""
        INSERT INTO Bruker (Epost, Passord, Fornavn, Etternavn)
        VALUES ("{email}", "{password}", "{first_name}", "{last_name}")
        """
        )
        return True, "Opprettet bruker"
    except:
        return False, "Epost er allerede i bruk"
