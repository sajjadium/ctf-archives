import db from "@/utils/db";
import { getSessionCookie, getUserBySession } from "@/utils/helpers";

export default async function handler(req, res) {
    const session = getSessionCookie(req);
    const user = await getUserBySession(session);

    if (!user) {
        res.status(401).json({ msg: "Unauthorized" });
        return;
    }

    if (req.method === "POST") {
        db.get(
            `SELECT * FROM users WHERE id = ?`,
            user.id,
            async (err, row) => {
                if (err) {
                    res.status(400).json({ error: err.message });
                    return;
                }
                if (!row || Number.isInteger(row.shared_frog)) {
                    res.status(400).json({
                        msg: "You cannot share another frog",
                    });
                    return;
                }
                const { name, url: img, svgProps } = req.body;
                const newFrog = {
                    name,
                    creator: user.id,
                    img,
                    svgProps: svgProps ? JSON.stringify(svgProps) : null,
                };

                const sql =
                    "INSERT INTO frogs (name, creator, img, svgProps, is_approved) VALUES (?,?,?,?,?)";
                db.run(
                    sql,
                    [
                        newFrog.name,
                        newFrog.creator,
                        newFrog.img,
                        newFrog.svgProps,
                        0,
                    ],
                    function (err) {
                        if (err) {
                            res.status(400).json({ error: err.message });
                            return;
                        }
                        const lastId = this.lastID;
                        db.run(
                            `UPDATE users SET shared_frog = ? WHERE id = ?`,
                            [lastId, user.id]
                        );
                        res.status(200).json({
                            msg: "Frog shared successfully",
                            id: lastId,
                        });
                    }
                );
            }
        );
    } else if (req.method === "PATCH") {
        const frogId = req.query.id;

        if (!frogId) {
            res.status(400).json({ msg: "Missing frog ID" });
            return;
        }

        const { name, url: img, svgProps } = req.body;
        const updatedFrog = {
            name,
            img,
            svgProps: svgProps ? JSON.stringify(svgProps) : null,
        };

        db.get(
            `SELECT * FROM frogs WHERE id = ?`,
            frogId,
            async (err, frog) => {
                if (err) {
                    res.status(400).json({ error: err.message });
                    return;
                }
                if (!frog || frog.creator !== user.id) {
                    res.status(400).json({
                        msg: "Frog not found",
                    });
                    return;
                }

                db.run(
                    `UPDATE frogs SET name = ?, img = ?, svgProps = ? WHERE id = ?`,
                    [
                        updatedFrog.name,
                        updatedFrog.img,
                        updatedFrog.svgProps,
                        frogId,
                    ],
                    (err) => {
                        if (err) {
                            res.status(400).json({ error: err.message });
                            return;
                        }
                        res.status(200).json({
                            msg: "Frog updated successfully",
                        });
                    }
                );
            }
        );
    } else {
        res.status(405).json({ msg: "Method not allowed" });
    }
}
