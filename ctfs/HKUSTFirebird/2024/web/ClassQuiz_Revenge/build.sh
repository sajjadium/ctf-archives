#!/usr/bin/env bash
set -e
FLAG="${FLAG:-firebird\{fakeflag\}}"

#
# master branch latest as of 20 January, 2024 10:00 HKT
# https://github.com/mawoka-myblock/ClassQuiz/commit/e8e330e385df906f4cb4bba0dabbfb005de2e472
#

rm -rf ClassQuiz/
git clone --depth=1 -- https://github.com/mawoka-myblock/ClassQuiz.git ClassQuiz
pushd ClassQuiz

git reset --hard e8e330e385df906f4cb4bba0dabbfb005de2e472

#
# initial config
# modifying docker-compose config base on the documentation: https://classquiz.de/docs/self-host
#
sed -i "s/TOP_SECRET/$(openssl rand -hex 32)/g" docker-compose.yml

yq -i ".services.frontend.environment.VITE_GOOGLE_AUTH_ENABLED=false" docker-compose.yml
yq -i ".services.frontend.environment.VITE_GITHUB_AUTH_ENABLED=false" docker-compose.yml
yq -i ".services.frontend.environment.VITE_CAPTCHA_ENABLED=false" docker-compose.yml

yq -i ".services.api.volumes=[\"appdata:/app/data\"]" docker-compose.yml
yq -i ".volumes.appdata=null" docker-compose.yml


# add security headers
git apply -v ../patches/caddy-headers.patch

# add CSP headers
git apply -v ../patches/csp.patch

# disable telemetry
git apply -v ../patches/disable_telemetry.patch


#
# start ClassQuiz
#
docker compose up -d --build

#
# Flag is in the password hash of the admin user (xssbot user). Good luck!
#
docker compose exec -T db psql --user postgres --dbname classquiz \
    --command "INSERT INTO public.users (id,email,username,password,verified,created_at,avatar,require_password,backup_code,storage_used) 
                VALUES (
                    REPLACE(gen_random_uuid()::text, '-', ''),
                    'admin@firebird.sh',
                    'admin',
                    '$FLAG',
                    True,
                    now(),
                    DECODE('DEADBEEF', 'hex'),
                    True,
                    REPLACE(CONCAT(gen_random_uuid()::text, gen_random_uuid()::text), '-', ''),
                    0)"