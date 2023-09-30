// Waits for MongoDB to be accessible

var conn;
try
{
    conn = new Mongo("localhost:27017");
}
catch(Error)
{
    //print(Error);
}
while(conn===undefined)
{
    try
    {
        conn = new Mongo("localhost:27017");
    }
    catch(Error)
    {
        //print(Error);
    }
    sleep(1000);
    print("Wating for Mongo to come up...")
}
DB = conn.getDB("test");
Result = DB.runCommand('buildInfo');
print(Result.version);