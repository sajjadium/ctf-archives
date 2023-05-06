import Vapor
import SQLite
import Foundation

let flag = try! String(contentsOfFile: "flag.txt")

let db: Connection = {
    let db = try! Connection(":memory:")
    try! db.run("CREATE TABLE flags (flag TEXT)")
    try! db.run("INSERT INTO flags VALUES ('\(flag)')")
    return db
}()

func routes(_ app: Application) throws {
    app.get { req -> EventLoopFuture<Vapor.View> in
        var result: String?
        let content = req.cookies.all["flag"]?.string ?? ""
        
        do {
            for _ in try db.prepare("SELECT * FROM flags WHERE flag='\(content)'") {
                result = "yes"
            }
        } catch {
            result = "bad"
        }
        
        return req.view.render("index", ["result": result ?? "no"])
    }

    // Okay while this doesn't do anything it's just easier
    // to keep it in here
    app.get("hello") { req -> String in
        return "Hello, world!"
    }
}
