INSERT INTO
  "main"."Land" ("LandID", "Navn")
VALUES
  ('1', 'El Salvador');

--
INSERT INTO
  "main"."Land" ("LandID", "Navn")
VALUES
  ('2', 'Colombia');

--
INSERT INTO
  "main"."Land" ("LandID", "Navn")
VALUES
  ('3', 'Rwanda');

--
INSERT INTO
  "main"."Region" ("Land_LandID", "Navn")
VALUES
  (3, 'RwandaRegion');

--
INSERT INTO
  "main"."Region" ("Land_LandID", "Navn")
VALUES
  (1, 'Santa Ana');

--
INSERT INTO
  "main"."Gård" (GårdID, "Navn", "Høyde", "Region_RegionID")
VALUES
  (1, 'Gårdsnavn', 200, 1);

--
INSERT INTO
  "main"."Gård" (GårdID, "Navn", "Høyde", "Region_RegionID")
VALUES
  (2, 'Nombre de Dios', 200, 2);

--
INSERT INTO
  "main"."KaffebønneArt" (KaffebønneArtID, Art)
VALUES
  (1, "arabica");

--
INSERT INTO
  Foredlingsmetode (ForedlingsmetodeID, Navn, Beskrivelse)
VALUES
  (1, "Bærtørket", "Beskrivelse") --
INSERT INTO
  Kaffebønne (
    KaffebønneID,
    Navn,
    KaffebønneArt_KaffebønneArtID
  )
VALUES
  (1, "Bourbon", 1) --
INSERT INTO
  Kaffeparti (
    KaffepartiID,
    Innhøstingsår,
    Kilopris,
    Gård_GårdID,
    Foredlingsmetode_ForedlingsmetodeID
  )
VALUES
  (1, 2019, 20, 2, 1) --
INSERT INTO
  KaffepartiHarKaffebønne (Kaffeparti_KaffepartiID, Kaffebønne_KaffebønneID)
VALUES
  (1, 1)