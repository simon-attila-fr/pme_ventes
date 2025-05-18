CREATE TABLE IF NOT EXISTS magasins (
    id_magasin INTEGER PRIMARY KEY,
    ville VARCHAR(100),
    nb_de_salaries INTEGER,
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS produits (
    id_reference_produit VARCHAR(100) PRIMARY KEY,
    nom VARCHAR(100),
    prix INTEGER,
    stock INTEGER,
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ventes (
    id_reference_produit VARCHAR(100),
    id_magasin INTEGER,
    id_vente INTEGER PRIMARY KEY,
    quantite INTEGER,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (id_reference_produit)
        REFERENCES produits (id_reference_produit)
        ON DELETE CASCADE
        ON UPDATE NO ACTION
    FOREIGN KEY (id_magasin)
        REFERENCES magasins (id_magasin)
        ON DELETE CASCADE
        ON UPDATE NO ACTION
);