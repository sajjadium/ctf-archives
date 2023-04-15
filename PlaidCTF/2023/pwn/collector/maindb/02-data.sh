#!/bin/sh

set -euo pipefail

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    INSERT INTO items (id, kind, name) VALUES (0, 'gold', 'Gold Pieces');
    INSERT INTO items (kind, name) VALUES
        ('compass2', 'Compass of Cartography'),
        ('tribarrel', 'Tribarrel'),
        ('treasuremap', 'Treasure Map'),
        ('rum', 'Rum'),
        ('anchor', 'Anchor'),
        ('wheel', 'Wheel'),
        ('dagger', 'Dagger'),
        ('dubloon', 'Dangerous Dubloon'),
        ('cap', 'Cap'),
        ('gold-dagger', 'Gold Dagger'),
        ('crossbow', 'Crossbow'),
        ('compass', 'Basic Compass'),
        ('cannon2', 'Cannon of Carnage'),
        ('chest-of-gold', 'Chest'),
        ('key', 'Key'),
        ('cannonballs', 'Cannonball'),
        ('spyglass', 'Spyglass'),
        ('hook', 'Hook'),
        ('peg-leg', 'Peg Leg'),
        ('map', 'Map'),
        ('blunderbuss', 'Blunderbuss'),
        ('cannon', 'Cannon of Creativity'),
        ('saber', 'Saber'),
        ('cutlass', 'Cutlass'),
        ('sea-chest', 'Sea my Chest'),
        ('feather-cap', 'Hood of Robin'),
        ('chest-of-jewels', 'Chest of Jewels'),
        ('pistol', 'Pistol'),
        ('sextant', 'Sextant'),
        ('rapier', 'Rapier'),
        ('chalice', 'Golden Chalice of Cornwall'),
        ('bomb', 'Bomb');


    INSERT INTO initial_inventory (item_id, count)
    VALUES (0, 10000);
    INSERT INTO market (item_id, bid_price, bid_size, ask_price, ask_size) 
    VALUES (1, 30, 100, 200, 100); 

    INSERT INTO flag (flag) VALUES ('$FLAG')
EOSQL
