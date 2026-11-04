// Charge etudiants.json (fabriqué par generer.py) et remplit la page.
let etudiants = [];

function afficher(liste) {
  const corps = document.getElementById("liste");
  corps.innerHTML = "";
  for (const e of liste) {
    const ligne = document.createElement("tr");
    for (const valeur of [e.matricule, e.prenom, e.nom, e.ville, e.filiere, e.annee]) {
      const cellule = document.createElement("td");
      cellule.textContent = valeur;
      ligne.appendChild(cellule);
    }
    const moyenne = document.createElement("td");
    moyenne.textContent = e.moyenne.toFixed(2);
    if (e.moyenne < 10) moyenne.className = "ajourne";
    ligne.appendChild(moyenne);
    corps.appendChild(ligne);
  }
}

document.getElementById("recherche").addEventListener("input", (evt) => {
  const texte = evt.target.value.toLowerCase();
  afficher(etudiants.filter((e) =>
    [e.matricule, e.prenom, e.nom, e.ville, e.filiere].join(" ").toLowerCase().includes(texte)));
});

fetch("etudiants.json")
  .then((reponse) => {
    if (!reponse.ok) throw new Error(reponse.status);
    return reponse.json();
  })
  .then((donnees) => {
    etudiants = donnees.etudiants;
    const s = donnees.statistiques;
    document.getElementById("effectif").textContent = s.effectif;
    document.getElementById("moyenne").textContent = s.moyenne_generale.toFixed(2);
    document.getElementById("reussite").textContent = s.taux_reussite + " %";
    document.getElementById("filieres").textContent = s.filieres;
    document.getElementById("construction").textContent =
      "commit " + donnees.commit + ", fabriqué le " + donnees.fabrique_le;
    afficher(etudiants);
  })
  .catch(() => {
    document.getElementById("erreur").hidden = false;
  });
