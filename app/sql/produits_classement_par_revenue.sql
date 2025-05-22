SELECT produits.nom, ROUND((SUM(ventes.quantite) * produits.prix), 2) AS revenue_total
FROM ventes
INNER JOIN produits
ON ventes.id_reference_produit=produits.id_reference_produit
GROUP BY produits.nom
ORDER BY revenue_total DESC;