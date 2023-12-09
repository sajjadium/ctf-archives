const mariadb = require("mariadb");

const pool = mariadb.createPool({
  host: process.env.DATABASE_HOST,
  database: process.env.DATABASE_NAME,
  user: process.env.DATABASE_USER,
  password: process.env.DATABASE_PASSWORD,
  connectionLimit: process.env.DATABASE_POOL_LIMIT, // TODO: Check the best value
});

const withDBConnection = async (callback, fallback = undefined) => {
  let conn;
  try {
    conn = await pool.getConnection();
    return await callback(conn);
  } catch (err) {
    console.error(err);
  } finally {
    if (conn) conn.end();
  }
  return fallback;
};

const withDBTransaction = async (callback, fallback = undefined) => {
  let conn;
  try {
    conn = await pool.getConnection();
    await conn.beginTransaction();
    const result = await callback(conn);
    await conn.commit();
    return result;
  } catch (err) {
    console.error(err);
    await conn.rollback();
  } finally {
    if (conn) conn.end();
  }
  return fallback;
};

module.exports = {
  fetchUser: async (username) => {
    return await withDBConnection(async (conn) => {
      const rows = await conn.query(
        "SELECT * FROM users WHERE username = ?",
        username
      );
      if (rows.length > 0) return rows[0];
      return undefined;
    });
  },
  fetchUserById: async (id) => {
    return await withDBConnection(async (conn) => {
      const rows = await conn.query("SELECT * FROM users WHERE id = ?", id);
      if (rows.length > 0) return rows[0];
      return undefined;
    });
  },
  addUser: async (username, password_enc, private_key, session_key, coupon) => {
    return await withDBConnection(async (conn) => {
      const res = await conn.query(
        "INSERT INTO users(username, password, curve_private_key, session_key, balance, coupon, shield) VALUES (?, ?, ?, ?, 0, ?, NULL)",
        [username, password_enc, private_key, session_key, coupon]
      );
      return res.affectedRows > 0;
    }, false);
  },
  updateUser: async (old_username, password_enc, username, enabled) => {
    return await withDBConnection(async (conn) => {
      const query = `UPDATE users SET ${
        password_enc ? "password = ?," : ""
      }${
        username ? "username = ?," : ""
      }  enabled = ? WHERE username = ?`;

      const args = [];
      if(password_enc)
        args.push(password_enc);
      if(username)
        args.push(username);
      args.push(enabled);
      args.push(old_username);

      const res = await conn.query(query, args);
      return res.affectedRows > 0;
    }, false);
  },
  changeMotto: async (user_id, motto) => {
    return await withDBConnection(async (conn) => {
      const res = await conn.query("UPDATE users SET motto = ? WHERE id = ?", [
        motto,
        user_id,
      ]);
      return res.affectedRows > 0;
    }, false);
  },
  applyCoupon: async (user_id) => {
    return await withDBConnection(async (conn) => {
      const res = await conn.query(
        "UPDATE users SET balance = balance + ?, coupon = NULL WHERE id = ?",
        [process.env.COUPON_VALUE, user_id]
      );
      return res.affectedRows > 0;
    }, false);
  },
  resetUser: async (user_id, coupon) => {
    return await withDBTransaction(async (conn) => {
      await conn.query(
        "UPDATE users SET balance = 0, motto = NULL, coupon = ?, shield = NULL WHERE id = ?",
        [coupon, user_id]
      );
      await conn.query(
        "UPDATE actions SET owner = NULL WHERE owner = ?",
        user_id
      );
      await conn.query("DELETE FROM reports WHERE user_id = ?", user_id);
      return true;
    }, false);
  },
  applyShield: async (user_id) => {
    return await withDBTransaction(async (conn) => {
      const [{ balance }] = await conn.query(
        "SELECT balance FROM users WHERE id = ?",
        user_id
      );
      if (balance < parseFloat(process.env.SHIELD_PRICE)) {
        throw Error("Insufficient balance"); // conn.rollback();
      }
      const res = await conn.query(
        "UPDATE users SET balance = balance - ?, shield = CURRENT_TIMESTAMP WHERE id = ?",
        [process.env.SHIELD_PRICE, user_id]
      );
      conn.commit();
      return res.affectedRows > 0;
    }, false);
  },
  hasShieldActivated: async (user_id) => {
    return await withDBConnection(async (conn) => {
      const res = await conn.query(
        "SELECT * FROM users WHERE id = ? AND shield IS NOT NULL AND TIMESTAMPADD(SECOND, ?, shield) > CURRENT_TIMESTAMP",
        [user_id, process.env.SHIELD_DURATION]
      );
      return res.length > 0;
    }, false);
  },
  fetchItems: async () => {
    return await withDBConnection(async (conn) => {
      const rows = await conn.query("SELECT * FROM actions");
      return rows;
    }, []);
  },
  fetchItemsAndOwners: async () => {
    return await withDBConnection(async (conn) => {
      const rows = await conn.query(
        "SELECT a.id, a.name, a.text, u.username FROM actions a LEFT OUTER JOIN users u ON a.owner = u.id"
      );
      return rows;
    }, []);
  },
  fetchItemAndOwner: async (action) => {
    return await withDBConnection(async (conn) => {
      const rows = await conn.query(
        "SELECT a.id, a.name, a.text, u.username FROM actions a LEFT OUTER JOIN users u ON a.owner = u.id WHERE a.name = ?",
        [action]
      );
      if (rows.length > 0) return rows[0];
      return [];
    }, []);
  },
  resetItemOwner: async (item_id) => {
    return await withDBTransaction(async (conn) => {
      const locks = await conn.query(
        "SELECT u.shield FROM actions a INNER JOIN users u WHERE a.id = ? AND a.owner = u.id AND u.shield IS NOT NULL AND TIMESTAMPADD(SECOND, ?, u.shield) > CURRENT_TIMESTAMP",
        [item_id, process.env.SHIELD_DURATION]
      );
      if (locks.length > 0) {
        throw Error("Item is shielded"); // conn.rollback();
      }
      const res = await conn.query(
        "UPDATE actions SET owner = NULL WHERE id = ?",
        item_id
      );
      conn.commit();
      return res.affectedRows > 0;
    }, false);
  },
  buyItem: async (user_id, item_name) => {
    return await withDBTransaction(async (conn) => {
      const [{ balance }] = await conn.query(
        "SELECT balance FROM users WHERE id = ?",
        user_id
      );
      const item = await conn.query(
        "SELECT price, owner FROM actions WHERE name = ?",
        item_name
      );
      if(item.length == 0){
        throw Error("Item not found");
      }
      const [{ price, owner }] = item;
      if (owner !== null || balance < price) {
        throw Error("Item already sold or insufficient balance"); // conn.rollback();
      }
      conn.query("UPDATE users SET balance = balance - ? WHERE id = ?", [
        price,
        user_id,
      ]);
      const res = await conn.query(
        "UPDATE actions SET owner = ? WHERE name = ? AND owner is NULL",
        [user_id, item_name]
      );
      conn.commit();
      return res.affectedRows > 0;
    }, false);
  },
  addReport: async (user_id, url) => {
    return await withDBConnection(async (conn) => {
      const res = await conn.query(
        "INSERT INTO reports (user_id, url) VALUES (?, ?)",
        [user_id, url]
      );
      return res.affectedRows > 0;
    }, false);
  },
  fetchAndRemoveReport: async () => {
    return await withDBConnection(async (conn) => {
      const rows = await conn.query("SELECT * FROM reports LIMIT 1");
      if (!rows) return false;

      if (rows.length > 0) {
        const res = rows[0];
        await conn.query("DELETE FROM reports WHERE id = ?", res.id);
        return res;
      }
      return [];
    }, []);
  },
};
