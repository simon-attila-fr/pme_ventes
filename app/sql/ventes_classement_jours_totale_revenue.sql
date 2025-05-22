SELECT date, ROUND((quantite * p.prix), 2) AS vente_totale
FROM ventes
INNER JOIN produits AS p
ON ventes.id_reference_produit = p.id_reference_produit
ORDER BY vente_totale DESC;