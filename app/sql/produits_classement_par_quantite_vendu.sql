SELECT produits.nom, SUM(ventes.quantite) AS q
FROM ventes
INNER JOIN produits
ON ventes.id_reference_produit=produits.id_reference_produit
GROUP BY produits.nom
ORDER BY q DESC;