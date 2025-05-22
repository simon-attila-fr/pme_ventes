SELECT ROUND(avg(quantite * p.prix), 2) AS ventes_moyenne_journaliere_de_periode
FROM ventes
INNER JOIN produits AS p
ON ventes.id_reference_produit = p.id_reference_produit;