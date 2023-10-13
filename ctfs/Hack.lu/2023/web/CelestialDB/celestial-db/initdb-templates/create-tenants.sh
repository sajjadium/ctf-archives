#!/usr/bin/env bash

# if TENANTS is empty, abort
if [ -z "$TENANTS" ]; then
    echo "No tenants specified"
    exit 1
fi

# builds an initdb file from templates
create_tenant() {
    creds="$1"

    # split creds into name and password
    IFS=':' read -r -a tenant_creds <<< "$creds"
    tenant="${tenant_creds[0]}"
    tenant_pw="${tenant_creds[1]}"
    outfile="/docker-entrypoint-initdb.d/99-tenant-$tenant.sql"

    if [ -f "$outfile" ]; then
        echo "Tenant $tenant already exists, skipping..."
        return
    fi
    
    cat /templates/create-tenant.sql \
        | sed "s/TENANTDB/tenant_$tenant/g" \
        | sed "s/TENANTUSER/$tenant/g" \
        | sed "s/TENANTPW/$tenant_pw/g" \
        > "$outfile"
    cat /templates/define-management-functions.sql >> "$outfile"
}

# iterate over each tenant from the TENANTS env var, split by commas
for tenant in $(echo "$TENANTS" | sed "s/,/ /g")
do
    echo "Creating tenant $tenant..."
    create_tenant "$tenant"
done
