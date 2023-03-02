# TestUnitaireWithFastApi

Outils :

Editeur de code : Visual Studio Code 
Environnement BDD : SSMS (Microsoft SQL Server Management Studio)


Base de donnée :

Dans SSMS, crée une base de donnée 'ApiTestUnitaires' et 'execute new query':
CREATE TABLE USERS
(
	ID BIGINT IDENTITY(1,1) PRIMARY KEY NOT NULL,
	FIRSTNAME VARCHAR(MAX) NOT NULL,
	LASTNAME VARCHAR(MAX) NOT NULL,
	AGE BIGINT NOT NULL
)

GO

INSERT INTO USERS (FIRSTNAME, LASTNAME, AGE)
VALUES('Tom', 'Cousdikian', 23);
GO


Initialisation :

Dans un fichier main.py : 
        import pyodbc as odbccon (cmd : pip install pyodbc)
        from fastapi import FastAPI (cmd : pip install fastapi)
    
    
Api :

Cmd  : pip install "uvicorn[standard]"
Puis aller sur : [http://127.0.0.1:8000](http://127.0.0.1:8000/docs#/default)

Il est maintenant possible d'utiliser les différentes méthodes : CRUD (j'ai 2 delete, l'un pour supprimer 1 row l'un pour tout supprimer)


Test Unitaires :

Créer un fichier test_main.py dans dans le sqous-dossier test/unit
Une fois lest test unitaires créent :
Cmd :  python -m unittest \test\unit\test_main.py
