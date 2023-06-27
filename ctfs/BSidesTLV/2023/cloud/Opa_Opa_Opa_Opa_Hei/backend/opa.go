package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	url "net/url"
	"os"
	"regexp"
	"strings"

	"github.com/google/uuid"
	"github.com/pkg/errors"

	"github.com/open-policy-agent/opa/ast"

	log "github.com/sirupsen/logrus"

	"github.com/gorilla/handlers"
	"github.com/gorilla/mux"
)

const (
	PackageString   = "package temp "
	PolicyModuleKey = "PolicyModule"
	PolicyMaxLength = 200
	APIBaseUrl      = "http://opa:8181/v1/"
	APIPoliciesUrl  = APIBaseUrl + "policies/"
	APIDataUrl      = APIBaseUrl + "data/"
)

type AddPolicyRequest struct {
	Policy string `json:"policy"`
}

type AddPolicyResponse struct {
	UUID string `json:"uuid"`
}

type EvalPolicyRequest struct {
	Input string `json:"input"`
	UUID  string `json:"uuid"`
}

type EvalPolicyResponse struct {
	Res bool `json:"res"`
}

func replaceHyphenByUnderscore(id uuid.UUID) string {
	return strings.ReplaceAll(id.String(), "-", "_")
}

func respondWithError(w http.ResponseWriter, code int, message string) {
	respondWithJSON(w, code, map[string]string{"error": message})
}

func respondWithJSON(w http.ResponseWriter, code int, payload interface{}) {
	response, _ := json.Marshal(payload)

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(code)
	w.Write(response)
}

func parseRegoPolicy(regoPolicy string) (map[string]*ast.Module, error) {
	var err error
	modules := map[string]*ast.Module{}
	compiler := ast.NewCompiler()

	modules[PolicyModuleKey], err = ast.ParseModule(PolicyModuleKey, PackageString+regoPolicy)
	if err != nil {
		log.WithError(err).Error("Invalid rego syntax")
		return nil, errors.New("Invalid rego syntax")
	}

	compiler.Compile(modules)
	if compiler.Failed() {
		log.WithError(compiler.Errors).Error("Compile failed")
		return nil, errors.New("Compile failed")
	}

	return modules, nil
}

func EvaluatePolicy(jsonString string, guid uuid.UUID) (*map[string]interface{}, error) {
	result, err := url.JoinPath(APIDataUrl, "opa", "opa", "g"+replaceHyphenByUnderscore(guid))
	if err != nil {
		return nil, errors.Wrap(err, "Falied to JoinPath")
	}

	reqURL, err := url.Parse(result)
	if err != nil {
		return nil, errors.Wrap(err, "Error Parse url")
	}

	resp, err := http.Post(reqURL.String(), "application/json", bytes.NewBuffer([]byte(jsonString)))
	if err != nil {
		return nil, errors.Wrap(err, "Error request")
	}

	body, _ := io.ReadAll(resp.Body)
	fmt.Println(string(body))

	if resp.StatusCode != 200 {
		return nil, nil
	}

	// Parse response
	var policyRes map[string]interface{}
	err = json.Unmarshal([]byte(body), &policyRes)
	if err != nil {
		return nil, errors.Wrap(err, "Error unmarshalling OPA response")
	}

	defer resp.Body.Close()

	return &policyRes, nil
}

func ValidatePolicy(addPolicyRequest AddPolicyRequest) error {
	var validPolicyRegex = regexp.MustCompile(`^[a-zA-Z0-9=\s,\:\[\]\{\}\(\)\"\.]+$`)

	if len(addPolicyRequest.Policy) > PolicyMaxLength {
		return errors.New("Policy size error")
	}

	matched := validPolicyRegex.Match([]byte(addPolicyRequest.Policy))
	if !matched {
		return errors.New("Invalid characters found in policy")
	}

	_, err := parseRegoPolicy(addPolicyRequest.Policy)
	if err != nil {
		return err
	}

	return nil
}

func CreatePolicyOpa(addPolicyRequest AddPolicyRequest, guid uuid.UUID) error {
	url, err := url.JoinPath(APIPoliciesUrl, "g"+replaceHyphenByUnderscore(guid))
	if err != nil {
		return errors.New("Failed to JoinPath")
	}

	req, err := http.NewRequest(http.MethodPut, url, bytes.NewBuffer([]byte("package opa.opa.g"+replaceHyphenByUnderscore(guid)+"\n"+addPolicyRequest.Policy)))
	if err != nil {
		return errors.New("Failed to prepare add policy request")
	}

	req.Header.Set("Content-Type", "text/plain")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return errors.New("Failed to add policy request")
	}

	if resp.StatusCode != 200 {
		body, _ := io.ReadAll(resp.Body)
		fmt.Println(string(body))
		return errors.New(fmt.Sprintf("Bad response from add policy request %d", resp.StatusCode))
	}

	defer resp.Body.Close()

	return nil
}

func GetPolicyOpa(addPolicyRequest AddPolicyRequest, guid uuid.UUID) error {
	url, err := url.JoinPath(APIPoliciesUrl, "g"+replaceHyphenByUnderscore(guid))
	if err != nil {
		return errors.New("Failed to JoinPath")
	}

	req, err := http.NewRequest(http.MethodGet, url, nil)
	if err != nil {
		return errors.New("Failed to prepare get policy request")
	}

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return errors.New("Failed to get policy request")
	}

	if resp.StatusCode != 200 {
		return errors.New(fmt.Sprintf("Bad response from add policy request %d", resp.StatusCode))
	}

	body, _ := io.ReadAll(resp.Body)
	fmt.Println(string(body))

	defer resp.Body.Close()

	return nil
}

func AddPolicy(w http.ResponseWriter, r *http.Request) {
	var addPolicyRespone AddPolicyResponse
	var addPolicyRequest AddPolicyRequest

	decoder := json.NewDecoder(r.Body)
	if err := decoder.Decode(&addPolicyRequest); err != nil {
		respondWithError(w, http.StatusBadRequest, "Invalid request payload")
		return
	}
	defer r.Body.Close()

	fmt.Println(addPolicyRequest.Policy)

	if err := ValidatePolicy(addPolicyRequest); err != nil {
		respondWithError(w, http.StatusBadRequest, err.Error())
		return
	}

	fmt.Println("Validated")

	guid := uuid.New()

	if err := CreatePolicyOpa(addPolicyRequest, guid); err != nil {
		respondWithError(w, http.StatusBadRequest, err.Error())
		return
	}

	// For testing
	if err := GetPolicyOpa(addPolicyRequest, guid); err != nil {
		respondWithError(w, http.StatusBadRequest, err.Error())
		return
	}

	addPolicyRespone.UUID = guid.String()

	respondWithJSON(w, http.StatusOK, addPolicyRespone)
}

func EvalPolicy(w http.ResponseWriter, r *http.Request) {
	var evalPolicyRequest EvalPolicyRequest
	var evalPolicyResponse EvalPolicyResponse

	decoder := json.NewDecoder(r.Body)
	if err := decoder.Decode(&evalPolicyRequest); err != nil {
		respondWithError(w, http.StatusBadRequest, "Invalid request payload")
		return
	}
	defer r.Body.Close()

	fmt.Println(evalPolicyRequest.Input)

	policyRes, err := EvaluatePolicy(evalPolicyRequest.Input, uuid.MustParse(evalPolicyRequest.UUID))
	if err != nil {
		respondWithError(w, http.StatusBadRequest, "Evaluate failed")
		return
	}

	val, ok := (*policyRes)["result"]
	// If the key exists
	if !ok {
		val = nil
	}

	evalPolicyResponse.Res = true

	if val == nil || len(val.(map[string]interface{})) == 0 {
		evalPolicyResponse.Res = false
	}

	respondWithJSON(w, http.StatusOK, evalPolicyResponse)
}

func Index(w http.ResponseWriter, r *http.Request) {
	// Define the HTML content as a string
	html := `
		<!DOCTYPE html>
		<html>
		<head>
			<title>OPA Challenge</title>
		</head>
		<body>
			<h1>Welcome to the OPA Challenge!</h1>
		</body>
		</html>
	`

	// Write the HTML content to the response writer
	_, err := w.Write([]byte(html))
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

func main() {
	log.Print("Listening 8000")
	r := mux.NewRouter()
	r.HandleFunc("/add", AddPolicy).Methods("POST")
	r.HandleFunc("/eval", EvalPolicy).Methods("POST")
	r.HandleFunc("/", Index).Methods("GET")
	log.Fatal(http.ListenAndServe(":8000", handlers.LoggingHandler(os.Stdout, r)))
}
