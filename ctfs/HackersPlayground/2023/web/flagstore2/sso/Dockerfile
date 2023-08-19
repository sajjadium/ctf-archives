FROM quay.io/keycloak/keycloak:21.1

COPY sctf_realm.json /opt/keycloak/sctf_realm.json
RUN /opt/keycloak/bin/kc.sh import --file /opt/keycloak/sctf_realm.json

ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]