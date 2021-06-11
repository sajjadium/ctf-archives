package main

import (
    "fmt"
    "log"
    "net/http"
    "io/ioutil"
    "strconv"
    "database/sql"
    "encoding/json"
    "github.com/buger/jsonparser"
    "github.com/gorilla/mux"
    _ "github.com/mattn/go-sqlite3"
)

var db *sql.DB
var token string = "REDACTED"


type Waffle struct {
    Name    string  `json:"name"`
    Radius  int     `json:"radius"`
    Height  int     `json:"height"`
    Url     string  `json:"img_url"`
}


func JSONerror(w http.ResponseWriter, code int, msg string){
    w.WriteHeader(code)
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]string{"err": msg})
}


func JSONmessage(w http.ResponseWriter, code int, msg string){
    w.WriteHeader(code)
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]string{"msg": msg})
}


func searchWaffle(w http.ResponseWriter, r *http.Request) {

    cookie,err := r.Cookie("token")

    if (err != nil || cookie.Value!=token) {
        JSONerror(w,403,"You need a valid token")
        return
    }
    
   
    reqBody, _ := ioutil.ReadAll(r.Body)

    query := "SELECT name, radius, height, img_url FROM waffle "
    var nFilt = 0

    name, err := jsonparser.GetString(reqBody,"name")
    if (err==nil){
        nFilt++
        query += "WHERE name = '" + name + "' "
    }

    minRad, err := jsonparser.GetInt(reqBody,"min_radius")
    if err == nil {
        if(nFilt != 0){
            query += "AND "
        } else {
            query += "WHERE "
        }
        nFilt ++
        query += "radius >= " + strconv.Itoa(int(minRad)) + " "
    }
    maxRad, err := jsonparser.GetInt(reqBody,"max_radius")
    if err == nil {
        if(nFilt != 0){
            query += "AND "
        } else {
            query += "WHERE "
        }
        nFilt ++
        query += "radius <= " + strconv.Itoa(int(maxRad)) + " "
    }

    query += ";"

    rows, err := db.Query(query)
    if err != nil {
        fmt.Println(err)
        JSONerror(w,500,"DB error, something was wrong with the query")
        return
    }

    waffleList := make([]Waffle, 0)
    
    defer rows.Close()
    for rows.Next() {
        var waffle Waffle
        err = rows.Scan(&waffle.Name, &waffle.Radius, &waffle.Height, &waffle.Url)
        if err != nil {
            fmt.Println(err)
            JSONerror(w,500,"DB error, something was wrong with the query")
            return
        }
        waffleList = append(waffleList,waffle)
    }

    w.Header().Set("Content-Type", "application/json")
    err = json.NewEncoder(w).Encode(waffleList);
}

func gettoken(w http.ResponseWriter, r *http.Request) {
    query := r.URL.Query()

    creditcards, ok1 := query["creditcard"]
    if !ok1 || len(creditcards[0]) < 1 {
        JSONerror(w,400,"Paramerer 'creditcard' is missing")
        return
    }
  
    promo := ""
    promos, ok := query["promocode"]
    
    if ok && len(promos[0]) > 0 {
        promo = promos[0]
    }

    _ = creditcards[0]
    
    if promo == "FREEWAF"{
        cookie    :=    http.Cookie{Name:"token",Value:token}
        http.SetCookie(w, &cookie)
        JSONmessage(w,200,"Take your free token!")
        return
    }
    
    //TODO implement payments
    JSONerror(w,403,"Sorry, we were unable to process your payment")

}


func handleRequests() {

    myRouter := mux.NewRouter().StrictSlash(true)

    myRouter.HandleFunc("/search", searchWaffle).Methods("POST")
    myRouter.HandleFunc("/gettoken", gettoken).Methods("GET")
    myRouter.PathPrefix("/").Handler(http.FileServer(http.Dir("./static/")))


    fmt.Println("Listening on port 10000")
    log.Fatal(http.ListenAndServe("0.0.0.0:10000", myRouter))
}

func main() {
    var err error
    db, err = sql.Open("sqlite3", "./db.sqlite")

    if err!= nil{
        fmt.Println("Unable to open the db")
        return
    }

    handleRequests()
}
