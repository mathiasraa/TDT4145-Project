-- -----------------------------------------------------
-- Table Land
-- -----------------------------------------------------
CREATE TABLE Land (
  LandID INTEGER NOT NULL,
  Navn TEXT NOT NULL,
  PRIMARY KEY (LandID),
  UNIQUE(Navn)
) -- -----------------------------------------------------
-- Table Region
-- -----------------------------------------------------
CREATE TABLE Region (
  RegionID INTEGER NOT NULL,
  Land_LandID INTEGER NOT NULL,
  Navn TEXT NOT NULL,
  PRIMARY KEY (RegionID, Land_LandID),
  CONSTRAINT fk_Region_Land FOREIGN KEY (Land_LandID) REFERENCES Land (LandID) ON DELETE CASCADE ON UPDATE CASCADE,
  UNIQUE(Land_LandID, Navn)
) -- -----------------------------------------------------
-- Table Gård
-- -----------------------------------------------------
CREATE TABLE Gård (
  GårdID INTEGER NOT NULL,
  Navn TEXT NOT NULL,
  Høyde INTEGER NOT NULL,
  Region_RegionID INTEGER NOT NULL,
  Region_Land_LandID INTEGER NOT NULL,
  PRIMARY KEY (GårdID),
  CONSTRAINT fk_Gård_Region FOREIGN KEY (Region_RegionID, Region_Land_LandID) REFERENCES Region (RegionID, Land_LandID) ON DELETE CASCADE ON UPDATE CASCADE,
  UNIQUE(Navn, Region_RegionID, Region_Land_LandID)
) -- -----------------------------------------------------
-- Table KaffebønneArt
-- -----------------------------------------------------
CREATE TABLE KaffebønneArt (
  KaffebønneArtID INTEGER NOT NULL,
  Art TEXT NOT NULL,
  PRIMARY KEY (KaffebønneArtID),
  UNIQUE(Art)
) -- -----------------------------------------------------
-- Table Kaffebønne
-- -----------------------------------------------------
CREATE TABLE Kaffebønne (
  KaffebønneID INTEGER NOT NULL,
  Navn TEXT NOT NULL,
  KaffebønneArt_KaffebønneArtID INTEGER NOT NULL,
  PRIMARY KEY (KaffebønneID),
  CONSTRAINT fk_Kaffebønne_KaffebønneArt FOREIGN KEY (KaffebønneArt_KaffebønneArtID) REFERENCES KaffebønneArt (KaffebønneArtID) ON DELETE CASCADE ON UPDATE CASCADE,
  UNIQUE(Navn)
) -- -----------------------------------------------------
-- Table GårdHarKaffebønne
-- -----------------------------------------------------
CREATE TABLE GårdHarKaffebønne (
  Gård_GårdID INTEGER NOT NULL,
  Kaffebønne_KaffebønneID INTEGER NOT NULL,
  PRIMARY KEY (Gård_GårdID, Kaffebønne_KaffebønneID),
  CONSTRAINT fk_GårdHarKaffebønne_Gård FOREIGN KEY (Gård_GårdID) REFERENCES Gård (GårdID) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_GårdHarKaffebønne_Kaffebønne FOREIGN KEY (Kaffebønne_KaffebønneID) REFERENCES Kaffebønne (KaffebønneID) ON DELETE CASCADE ON UPDATE CASCADE
) -- -----------------------------------------------------
-- Table Foredlingsmetode
-- -----------------------------------------------------
CREATE TABLE Foredlingsmetode (
  ForedlingsmetodeID INTEGER NOT NULL,
  Navn TEXT NOT NULL,
  Beskrivelse TEXT NOT NULL,
  PRIMARY KEY (ForedlingsmetodeID),
  UNIQUE(Navn)
) -- -----------------------------------------------------
-- Table Kaffeparti
-- -----------------------------------------------------
CREATE TABLE Kaffeparti (
  KaffepartiID INTEGER NOT NULL,
  Innhøstingsår TEXT NOT NULL,
  Kilopris REAL NOT NULL CHECK(Kilopris >= 0),
  Gård_GårdID INTEGER NOT NULL,
  Foredlingsmetode_ForedlingsmetodeID INTEGER NOT NULL,
  PRIMARY KEY (KaffepartiID),
  CONSTRAINT fk_Kaffeparti_Gård FOREIGN KEY (Gård_GårdID) REFERENCES Gård (GårdID) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_Kaffeparti_Foredlingsmetode FOREIGN KEY (Foredlingsmetode_ForedlingsmetodeID) REFERENCES Foredlingsmetode (ForedlingsmetodeID) ON DELETE CASCADE ON UPDATE CASCADE
) -- -----------------------------------------------------
-- Table Brenneri
-- -----------------------------------------------------
CREATE TABLE Brenneri (
  BrenneriID INTEGER NOT NULL,
  Navn TEXT NOT NULL,
  PRIMARY KEY (BrenneriID),
  UNIQUE(Navn)
) -- -----------------------------------------------------
-- Table FerdigbrentKaffe
-- -----------------------------------------------------
CREATE TABLE FerdigbrentKaffe (
  FerdigbrentKaffeID INTEGER NOT NULL,
  Brenningsgrad TEXT NOT NULL,
  Kaffeparti_KaffepartiID INTEGER NOT NULL,
  Brenneri_BrenneriID INTEGER NOT NULL,
  Dato DATE NOT NULL,
  Navn TEXT NOT NULL,
  Beskrivelse TEXT NOT NULL,
  Kilopris REAL NOT NULL CHECK(Kilopris >= 0),
  PRIMARY KEY (FerdigbrentKaffeID),
  CONSTRAINT fk_FerdigbrentKaffe_Kaffeparti FOREIGN KEY (Kaffeparti_KaffepartiID) REFERENCES Kaffeparti (KaffepartiID) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_FerdigbrentKaffe_Brenneri FOREIGN KEY (Brenneri_BrenneriID) REFERENCES Brenneri (BrenneriID) ON DELETE CASCADE ON UPDATE CASCADE,
  UNIQUE(Navn, Brenneri_BrenneriID)
) -- -----------------------------------------------------
-- Table KaffepartiHarKaffebønne
-- -----------------------------------------------------
CREATE TABLE KaffepartiHarKaffebønne (
  Kaffeparti_KaffepartiID INTEGER NOT NULL,
  Kaffebønne_KaffebønneID INTEGER NOT NULL,
  PRIMARY KEY (Kaffeparti_KaffepartiID, Kaffebønne_KaffebønneID),
  CONSTRAINT fk_KaffepartiHarKaffebønne_Kaffeparti FOREIGN KEY (Kaffeparti_KaffepartiID) REFERENCES Kaffeparti (KaffepartiID) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_KaffepartiHarKaffebønne_Kaffebønne FOREIGN KEY (Kaffebønne_KaffebønneID) REFERENCES Kaffebønne (KaffebønneID) ON DELETE CASCADE ON UPDATE CASCADE
) -- -----------------------------------------------------
-- Table Bruker
-- -----------------------------------------------------
CREATE TABLE Bruker (
  BrukerID INTEGER NOT NULL,
  Fornavn TEXT NOT NULL,
  Etternavn TEXT NOT NULL,
  Epost TEXT NOT NULL,
  Passord TEXT NOT NULL,
  PRIMARY KEY (BrukerID),
  UNIQUE(Epost)
) -- -----------------------------------------------------
-- Table Kaffesmaking
-- -----------------------------------------------------
CREATE TABLE Kaffesmaking (
  KaffesmakingID INTEGER NOT NULL,
  Smaksnotater TEXT NOT NULL,
  Poeng INTEGER NOT NULL CHECK(
    Poeng >= 0
    AND Poeng <= 10
  ),
  Dato DATE,
  FerdigbrentKaffe_FerdigbrentKaffeID INTEGER NOT NULL,
  Bruker_BrukerID INTEGER NOT NULL,
  PRIMARY KEY (KaffesmakingID),
  CONSTRAINT fk_Kaffesmaking_FerdigbrentKaffe1 FOREIGN KEY (FerdigbrentKaffe_FerdigbrentKaffeID) REFERENCES FerdigbrentKaffe (FerdigbrentKaffeID) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_Kaffesmaking_Bruker FOREIGN KEY (Bruker_BrukerID) REFERENCES Bruker (BrukerID) ON DELETE CASCADE ON UPDATE CASCADE
)