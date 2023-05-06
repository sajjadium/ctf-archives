(ns story-mode.core
  (:gen-class)
  (:require
   [aleph.http :as http]
   [clojure.java.io :as io]
   [compojure.core :as compojure]
   [compojure.route :as route]
   [ring.middleware.params :as params]
   [ring.util.request :as request]
   [ring.util.response :as response]))

(defn check-flag [req]
  (if (= (request/body-string req) (slurp "flag.txt"))
    {:status 200 :body "yes"}
    {:status 400 :body "no"}))

(defn get-story-part [req]
  (let [part ((req :query-params) "part")]
    (if (nil? part)
      {:status 400 :body "No part specified"}
      (response/file-response (str "story/" part)))))

(def handle
  (compojure/routes
    (compojure/GET "/" []
                   {
                    :status 200
                    :headers {"content-type" "text/html"}
                    :body (io/input-stream (io/resource "public/index.html"))
                   })
    (compojure/POST "/check" [] check-flag)
    (compojure/GET "/story" [] (params/wrap-params get-story-part))
    (route/resources "/")
    (route/not-found "hm")))

(defn -main []
  (http/start-server handle {:port 3000}))