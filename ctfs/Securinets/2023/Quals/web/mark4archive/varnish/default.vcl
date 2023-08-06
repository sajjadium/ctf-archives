#
# This is an example VCL file for Varnish.
#
# It does not do anything by default, delegating control to the
# builtin VCL. The builtin VCL is called when there is no explicit
# return statement.
#
# See the VCL chapters in the Users Guide for a comprehensive documentation
# at https://www.varnish-cache.org/docs/.

# Marker to tell the VCL compiler that this VCL has been written with the
# 4.0 or 4.1 syntax.
vcl 4.1;

# Default backend definition. Set this to point to your content server.
backend default {
    .host = "backend";
    .port = "5000";
}

sub vcl_recv {
    # Check if the request URL matches the internal endpoint
    if (req.url ~ "^/api/pdf") {
        # Respond with a 403 Forbidden status
        return (synth(403, "Forbidden - Internal Endpoint"));
    }
    if (req.http.upgrade ~ "(?i)websocket") {
        return (pipe);
    }
    if (req.method == "POST") {
        set req.http.X-Original-Method = "POST";
    }

    if (req.url ~ "^/makereport") {
        # If the request matches the endpoint, pass it to the backend directly
        return (pass);
    }
    # For all other requests, proceed with the default behavior
    # (e.g., pass the request to the backend or perform other processing)
    return (hash);
}


sub vcl_pipe {
    if (req.http.upgrade) {
	set bereq.http.connection = req.http.connection;
        set bereq.http.upgrade = req.http.upgrade;
    }
    return (pipe);
}

sub vcl_backend_response {
    # Happens after we have read the response headers from the backend.
    #
    # Here you clean the response headers, removing silly Set-Cookie headers
    # and other mistakes your backend does.
}

sub vcl_deliver {
    # Happens when we have all the pieces we need, and are about to send the
    # response to the client.
    #
    # You can do accounting or modifying the final object here.
}

sub vcl_backend_fetch {
    if (bereq.http.X-Original-Method) {
        set bereq.method = bereq.http.X-Original-Method;
        unset bereq.http.X-Original-Method;
    }
    
}
