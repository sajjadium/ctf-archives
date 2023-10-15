up:
	docker-compose up -d
build:
	docker-compose build --no-cache --force-rm
codeigniter4-install:
	docker-compose exec web composer create-project --prefer-dist codeigniter4/appstarter .
create-project:
	@make build
	@make up
	@make codeigniter4-install
install-recommend-packages:
	docker-compose exec web composer require --dev roave/security-advisories:dev-master
init:
	docker-compose up -d --build
	docker-compose exec web composer install
	docker-compose exec web cp env .env
remake:
	@make destroy
	@make init
stop:
	docker-compose stop
down:
	docker-compose down --remove-orphans
restart:
	@make down
	@make up
destroy:
	docker-compose down --rmi all --volumes --remove-orphans
destroy-volumes:
	docker-compose down --volumes --remove-orphans
ps:
	docker-compose ps
logs:
	docker-compose logs
logs-watch:
	docker-compose logs --follow
log-web:
	docker-compose logs web
log-web-watch:
	docker-compose logs --follow web
log-app:
	docker-compose logs app
log-app-watch:
	docker-compose logs --follow app
log-db:
	docker-compose logs db
log-db-watch:
	docker-compose logs --follow db
web:
	docker-compose exec web bash
migrate:
	docker-compose exec web php spark migrate
test:
	docker-compose exec web composer test
cache-clear:
	docker-compose exec web php spark cache:clear
npm:
	@make npm-install
npm-install:
	docker-compose exec web npm install
npm-dev:
	docker-compose exec web npm run dev
npm-watch:
	docker-compose exec web npm run watch
npm-watch-poll:
	docker-compose exec web npm run watch-poll
npm-hot:
	docker-compose exec web npm run hot
yarn:
	docker-compose exec web yarn
yarn-install:
	@make yarn
yarn-dev:
	docker-compose exec web yarn dev
yarn-watch:
	docker-compose exec web yarn watch
yarn-watch-poll:
	docker-compose exec web yarn watch-poll
yarn-hot:
	docker-compose exec web yarn hot
db:
	docker-compose exec db bash
sql:
	docker-compose exec db bash -c 'mysql -u $$MYSQL_USER -p$$MYSQL_PASSWORD $$MYSQL_DATABASE'
redis:
	docker-compose exec redis redis-cli
