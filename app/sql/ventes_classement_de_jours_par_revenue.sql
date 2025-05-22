SELECT
  case cast (strftime('%w', date) as integer)
  when 0 then 'Dimanche'
  when 1 then 'Lundi'
  when 2 then 'Mardi'
  when 3 then 'Mercredi'
  when 4 then 'Jeudi'
  when 5 then 'Vendredi'
  else 'Samedi' end as weekday,
  SUM(produits.prix) AS revenue_totale
FROM ventes
INNER JOIN produits
ON produits.id_reference_produit = ventes.id_reference_produit
GROUP BY weekday
ORDER BY revenue_totale DESC;