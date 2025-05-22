SELECT avg(quantite * p.prix)
FROM ventes
INNER JOIN produits AS p
ON ventes.id_reference_produit = p.id_reference_produit;