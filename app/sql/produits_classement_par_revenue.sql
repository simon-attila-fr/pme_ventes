SELECT produits.nom, (SUM(ventes.quantite) * produits.prix) AS revenue_total
FROM ventes
INNER JOIN produits
ON ventes.id_reference_produit=produits.id_reference_produit
GROUP BY produits.nom
ORDER BY revenue_total DESC;