SELECT ville, SUM(ventes.quantite) AS q
FROM magasins
INNER JOIN ventes
ON ventes.id_magasin = magasins.id_magasin
GROUP BY ville
ORDER BY q DESC;