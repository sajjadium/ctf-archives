vcl 4.1;

backend default {
    .host = "127.0.0.1:8082";
}

sub vcl_recv {
    if (req.url ~ "/admin" && !(req.http.Authorization ~ "^Basic TOKEN$")) {
        return (synth(403, "Access Denied"));
    }
}

sub vcl_synth {
    if (resp.status == 403) {
        set resp.body = resp.reason;
        return (deliver);
    }
}
