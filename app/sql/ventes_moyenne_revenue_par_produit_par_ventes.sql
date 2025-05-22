SELECT produits.nom, (SUM(ventes.quantite) * produits.prix) / (SELECT COUNT(v.date) FROM ventes AS v WHERE ventes.id_reference_produit = v.id_reference_produit) AS moyenne_revenue_par_achat
FROM produits
INNER JOIN ventes
ON ventes.id_reference_produit = produits.id_reference_produit
GROUP BY produits.nom
ORDER BY moyenne_revenue_par_achat DESC;