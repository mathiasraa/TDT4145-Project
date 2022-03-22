from queries import find_coffee
from utils.typography import text


def coffee_filter(filters):

    coffee = NONe

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


# '''
#     WITH selectedland AS (
#         SELECT LandID as id FROM Land WHERE
#         Navn = 'Rwanda' OR Navn = 'Colombia'),
#     unwashed AS (
#         SELECT ForedlingsmetodeID as id FROM Foredlingsmetode
#         WHERE Foredlingsmetode.Navn != 'Vasket')

#     SELECT Brenneri.Navn, FerdigbrentKaffe.Navn
#     FROM selectedland JOIN Region ON selectedland.id = Land_LandID
#     JOIN Gård ON RegionID = Region_RegionID
#     JOIN Kaffeparti ON Gård.GårdID = Kaffeparti.Gård_GårdID
#     JOIN unwashed ON unwashed.id = Foredlingsmetode_ForedlingsmetodeID
#     JOIN FerdigbrentKaffe ON KaffepartiID = Kaffeparti_KaffepartiID
#     JOIN Brenneri ON BrenneriID = Brenneri_BrenneriID
# '''

# '''
# SELECT Brenneri.Navn, FerdigbrentKaffe.Navn from Kaffesmaking
# JOIN FerdigbrentKaffe ON FerdigbrentKaffeID = FerdigbrentKaffe_FerdigbrentKaffeID
# JOIN Brenneri ON BrenneriID = Brenneri_BrenneriID
# WHERE Kaffesmaking.Smaksnotater LIKE('%%Wow%') OR FerdigbrentKaffe.Beskrivelse
# LIKE('%%Wow%')
# '''
