from utils.fetch import run_query


def all_countries():
    return run_query(
        """
        SELECT Navn as land_navn FROM Land
        """
    )


def all_coffees():
    return run_query(
        """
        SELECT FerdigbrentKaffeID as ferdigbrentkaffe_id, FerdigbrentKaffe.Navn as ferdigbrentkaffe_navn, Brenneri.Navn as brenneri_navn FROM FerdigbrentKaffe
        JOIN Brenneri on BrenneriID = Brenneri_BrenneriID
        """
    )


def all_breweries():
    return run_query(
        """
        SELECT BrenneriID as brenneri_id, Navn as brenneri_navn FROM Brenneri
        """
    )


def log_in(email, password):

    user_data = run_query(
        f"""
        SELECT BrukerID as bruker_id, Passord as bruker_passord from Bruker where Epost = "{email}"
        """
    )[0]
    if not user_data:
        return False, "Kan ikke finne bruker"
    else:
        if password == user_data.get("bruker_passord"):
            return True, user_data.get("bruker_id")
        else:
            return False, "Feil passord"


def register(email, password, first_name, last_name):

    try:
        run_query(
            f"""
        INSERT INTO Bruker (Epost, Passord, Fornavn, Etternavn)
        VALUES ("{email}", "{password}", "{first_name}", "{last_name}")
        """
        )
        return True, "Opprettet bruker"
    except:
        return False, "Epost er allerede i bruk"
