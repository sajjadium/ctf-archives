const sqlite3 = require("sqlite3").verbose();

(async () => {
	console.log(process.argv);
	const REAL_FLAG = process.argv[2];
	const db = new sqlite3.Database("/pb_data/data.db");
	db.get("SELECT * from posts", (err, row) => {
		if (err) {
			process.exit(1);
		}
		row.content = row.content.replace("ping{FAKE}", REAL_FLAG);
		db.run(
			"UPDATE posts SET content = ? WHERE id = ?",
			[row.content, row.id],
			(err) => {
				if (err) {
					process.exit(1);
				}
				db.close();
			}
		);
	});
})();
