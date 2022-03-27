gtimeout 2 openssl s_client -connect localhost:8000 -CAfile ../secret/cert.pem -verify_return_error -sess_out session.cache < /dev/null
sleep 2
gtimeout 2 openssl s_client -connect localhost:8000 -CAfile ../secret/cert.pem -verify_return_error -sess_in session.cache < /dev/null
