"""Fabrique le site « Gestion des étudiants » dans le dossier _site/.

1. lit donnees/etudiants.csv
2. vérifie les données (s'arrête en cas d'erreur)
3. copie les fichiers du dossier site/ dans _site/
4. écrit _site/etudiants.json, lu par la page web
"""
import csv
import json
import os
import shutil
import sys
from datetime import datetime, timezone

FICHIER_CSV = "donnees/etudiants.csv"
DOSSIER_SITE = "site"
DOSSIER_SORTIE = "_site"


def lire_etudiants(chemin):
    """Lit le fichier CSV et renvoie la liste des étudiants."""
    etudiants = []
    with open(chemin, encoding="utf-8") as fichier:
        for ligne in csv.DictReader(fichier):
            ligne = {cle: valeur.strip() for cle, valeur in ligne.items()}
            ligne["annee"] = int(ligne["annee"])
            ligne["moyenne"] = float(ligne["moyenne"])
            etudiants.append(ligne)
    return etudiants


def verifier(etudiants):
    """Renvoie la liste des erreurs trouvées dans les données (vide si tout va bien)."""
    erreurs = []
    vus = set()
    for e in etudiants:
        m = e["matricule"]
        if m in vus:
            erreurs.append(f"{m} : matricule en double")
        vus.add(m)
        if not 0 <= e["moyenne"] <= 20:
            erreurs.append(f"{m} : moyenne invalide ({e['moyenne']})")
        if "@" not in e["email"]:
            erreurs.append(f"{m} : adresse e-mail invalide ({e['email']})")
        if e["prenom"] == "" or e["nom"] == "":
            erreurs.append(f"{m} : prénom ou nom vide")
    return erreurs


def statistiques(etudiants):
    """Calcule les chiffres clés affichés en haut du site."""
    if len(etudiants) == 0:
        return {"effectif": 0, "moyenne_generale": 0, "taux_reussite": 0, "filieres": 0}
    moyennes = [e["moyenne"] for e in etudiants]
    admis = [m for m in moyennes if m >= 10]
    return {
        "effectif": len(etudiants),
        "moyenne_generale": round(sum(moyennes) / len(moyennes), 2),
        "taux_reussite": round(100 * len(admis) / len(moyennes)),
        "filieres": len({e["filiere"] for e in etudiants}),
    }


def fabriquer_site(etudiants):
    """Copie le site dans _site/ et y ajoute les données en JSON."""
    if os.path.exists(DOSSIER_SORTIE):
        shutil.rmtree(DOSSIER_SORTIE)
    shutil.copytree(DOSSIER_SITE, DOSSIER_SORTIE)
    donnees = {
        "commit": os.environ.get("GITHUB_SHA", "local")[:7],
        "fabrique_le": datetime.now(timezone.utc).strftime("%d/%m/%Y à %H:%M UTC"),
        "statistiques": statistiques(etudiants),
        "etudiants": etudiants,
    }
    with open(os.path.join(DOSSIER_SORTIE, "etudiants.json"), "w", encoding="utf-8") as sortie:
        json.dump(donnees, sortie, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    etudiants = lire_etudiants(FICHIER_CSV)
    erreurs = verifier(etudiants)
    if erreurs:
        print("Données invalides :")
        for erreur in erreurs:
            print(" -", erreur)
        sys.exit(1)
    fabriquer_site(etudiants)
    stats = statistiques(etudiants)
    print(f"Site fabriqué dans {DOSSIER_SORTIE}/ : {stats['effectif']} étudiants, "
          f"moyenne générale {stats['moyenne_generale']}")
