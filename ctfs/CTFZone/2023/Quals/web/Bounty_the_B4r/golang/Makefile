SWAGGER_FILE=swagger.yaml
SHARED_DIR=./api

generate:
	oapi-codegen -generate types -package api -o ${SHARED_DIR}/models.gen.go ${SWAGGER_FILE}
	oapi-codegen -generate chi-server -package api -o ${SHARED_DIR}/server.gen.go ${SWAGGER_FILE}