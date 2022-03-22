import sqlite3


def run_query(query):
    connection = sqlite3.connect("kaffedb.db")

    cursor = connection.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()
    connection.commit()
    connection.close()

    return rows


def find_coffee(coffee_name=None, brewery_name=None, description=None, coffee_id=None):
    coffee = None

    if description:
        coffee = run_query(
            f"""
            SELECT FerdigbrentKaffe.FerdigbrentKaffeID, FerdigbrentKaffe.Navn, Brenneri.Navn
            FROM Kaffesmaking
            JOIN FerdigbrentKaffe ON FerdigbrentKaffeID = FerdigbrentKaffe_FerdigbrentKaffeID
            JOIN Brenneri ON BrenneriID = Brenneri_BrenneriID where Kaffesmaking.Smaksnotater
            LIKE("%{description}%") or FerdigbrentKaffe.Beskrivelse LIKE("%{description}%")
            """
        )
    else:
        try:
            brewery_id = run_query(
                f"""
                SELECT BrenneriID FROM Brenneri WHERE Navn = "{brewery_name}"
                """
            )[0][0]
        except:
            return False

        try:
            coffee = run_query(
                f"""
                SELECT FerdigbrentKaffeID, FerdigbrentKaffe.Navn
                FROM FerdigbrentKaffe WHERE FerdigbrentKaffe.Navn = "{coffee_name}" AND Brenneri_BrenneriID = {brewery_id}
                """
            )
        except:
            pass

    return coffee


def create_coffee_tasting(coffee_id, user_id=0, tasting_data=None):
    tasting_note = tasting_data["tasting_note"]
    points = tasting_data["points"]

    run_query(
        f"""
        INSERT INTO Kaffesmaking (Smaksnotater, Poeng, FerdigbrentKaffe_FerdigbrentKaffeID, Bruker_BrukerID)
        VALUES ("{tasting_note}", {points}, {coffee_id}, {user_id})
        """
    )


def find_coffee_toplist():
    return run_query(
        """
        SELECT Brenneri.Navn, FerdigbrentKaffe.Navn, FerdigbrentKaffe.Kilopris, AVG(Poeng) 
        from Kaffesmaking 
        join FerdigbrentKaffe on FerdigbrentKaffe_FerdigbrentKaffeID = FerdigbrentKaffeID 
        join Brenneri on BrenneriID = Brenneri_BrenneriID 
        GROUP BY FerdigbrentKaffeID 
        ORDER BY kilopris/AVG(Poeng)
        """
    )


def all_countries():
    return run_query(
        """
        SELECT Navn FROM Land
        """
    )


def all_coffees():
    return run_query(
        """
        SELECT FerdigbrentKaffeID, Navn FROM FerdigbrentKaffe
        """
    )


def all_breweries():
    return run_query(
        """
        SELECT BrenneriID, Navn FROM Brenneri
        """
    )


def log_in(email, password):

    user_data = run_query(
        f"""
        SELECT BrukerID, Passord from Bruker where Epost = "{email}"
        """
    )
    if not user_data:
        return False, "No matchin credentials"
    else:
        if password == user_data[0][1]:
            return True, user_data[0][0]
        else:
            return False, "Wrong password"


def register(email, password, first_name, last_name):

    run_query(
        f"""
        INSERT INTO Bruker (Epost, Passord, Fornavn, Etternavn)
        VALUES ("{email}", "{password}", "{first_name}", "{last_name}")
        """
    )
