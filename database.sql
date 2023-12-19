DROP TABLE IF EXISTS Utenti;
DROP TABLE IF EXISTS Viaggi;
DROP TABLE IF EXISTS RichiestePassaggio;
DROP TABLE IF EXISTS Tracking;

PRAGMA foreign_keys = ON;

-- Tabella per gli utenti
CREATE TABLE IF NOT EXISTS Utenti (
    idUtente INTEGER PRIMARY KEY AUTOINCREMENT,
    nomeUtente TEXT NOT NULL,
    cognomeUtente TEXT NOT NULL,
    emailUtente TEXT UNIQUE NOT NULL,
    passwordUtente TEXT NOT NULL,
    telefonoUtente TEXT UNIQUE NOT NULL
);

-- Tabella per i viaggi
CREATE TABLE IF NOT EXISTS Viaggi (
    idViaggio INTEGER PRIMARY KEY AUTOINCREMENT,
    _idUtente INTEGER,
    indirizzoPartenza TEXT NOT NULL,
    lat_Partenza REAL NOT NULL,
    lon_Partenza REAL NOT NULL,
    time_stamp DATETIME NOT NULL,
    postiDisponibili INTEGER NOT NULL,
    Stato TEXT DEFAULT 'In Corso...', -- può essere Concluso
    
    FOREIGN KEY (_idUtente) REFERENCES Utenti(idUtente)
);

-- Tabella per le richieste di passaggio
CREATE TABLE IF NOT EXISTS RichiestePassaggio (
    idRichiestaPassaggio INTEGER PRIMARY KEY AUTOINCREMENT,
    _idViaggio INTEGER,
    _idUtente INTEGER,
    indirizzoPartenzaRider TEXT NOT NULL,
    indirizzoArrivo TEXT NOT NULL,
    lat_Arrivo REAL NOT NULL,
    lon_Arrivo REAL NOT NULL,
    Stato TEXT DEFAULT 'In Attesa', -- può essere Accettato / Rifiutato
    FOREIGN KEY (_idUtente) REFERENCES Utenti(idUtente),
    FOREIGN KEY (_idViaggio) REFERENCES Viaggi(idViaggio) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Tracking (
    idTrackingUtente INTEGER PRIMARY KEY AUTOINCREMENT, 
    lat REAL NOT NULL, 
    lon REAL NOT NULL,
    time_stamp DATETIME NOT NULL,
    _idUtente INTEGER, 
    FOREIGN KEY (_idUtente) REFERENCES Utenti(idUtente)
)