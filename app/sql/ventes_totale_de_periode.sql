SELECT ROUND(SUM(quantite * p.prix), 2) AS ventes_totale_en_eur
FROM ventes
INNER JOIN produits AS p
ON ventes.id_reference_produit = p.id_reference_produit;