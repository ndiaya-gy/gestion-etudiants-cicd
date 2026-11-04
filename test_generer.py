"""Tests du projet « Gestion des étudiants ». Lancement : pytest -v"""
from generer import lire_etudiants, verifier, statistiques, FICHIER_CSV


def exemple(matricule="ISEP26-9999", moyenne=12.0, email="a.b@etudiant.exemple.sn"):
    return {"matricule": matricule, "prenom": "Awa", "nom": "Diop", "email": email,
            "moyenne": moyenne, "filiere": "DevOps et cloud", "annee": 2}


# ---- Tests des fonctions ----

def test_statistiques_simples():
    stats = statistiques([exemple("A", 8), exemple("B", 12), exemple("C", 16)])
    assert stats["effectif"] == 3
    assert stats["moyenne_generale"] == 12
    assert stats["taux_reussite"] == 67


def test_statistiques_liste_vide():
    assert statistiques([])["effectif"] == 0


def test_verifier_detecte_une_moyenne_invalide():
    assert len(verifier([exemple(moyenne=25)])) == 1


def test_verifier_detecte_un_matricule_en_double():
    assert len(verifier([exemple("A"), exemple("A")])) == 1


# ---- Tests des données du fichier CSV ----

def test_le_fichier_contient_des_etudiants():
    assert len(lire_etudiants(FICHIER_CSV)) >= 60


def test_les_donnees_sont_valides():
    erreurs = verifier(lire_etudiants(FICHIER_CSV))
    assert erreurs == [], "\n".join(erreurs)
