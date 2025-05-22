SELECT magasins.ville, (SUM(ventes.quantite) * produits.prix) AS revenue_total
FROM ventes
INNER JOIN produits
ON ventes.id_reference_produit=produits.id_reference_produit
INNER JOIN magasins
ON ventes.id_magasin = magasins.id_magasin
GROUP BY produits.nom
ORDER BY revenue_total DESC;