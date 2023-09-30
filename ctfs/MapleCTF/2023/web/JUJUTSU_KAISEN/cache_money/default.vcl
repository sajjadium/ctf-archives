vcl 4.1;
import std;

backend app_backend {
    .host = "jjk_app";
    .port = "9080";   
}

backend db_backend {
    .host = "jjk_db";
    .port = "9090";   
}

acl internal {
    "localhost";
    "192.168.0.0/16";
    "172.0.0.0/8";
}

sub vcl_backend_response {
    set beresp.do_esi = true; 
}

sub vcl_recv {
    if (req.http.host ~ "jjk_db" && std.ip(client.ip, "17.17.17.17") ~ internal) {
        set req.backend_hint = db_backend;
    } else {
        set req.backend_hint = app_backend;
    }
}