# API Usage

## Test connectivity:
```shell
curl --request GET --url http://localhost:8001/
```

## Filter data by starting character
```shell
curl --request POST \
--url http://localhost:8001/rce \
--header 'Content-Type: application/json' \
--data '{
"Data": ["Alpha", "Beta", "Gamer"],
"Query": "(data) => data.Where(d => d.StartsWith(\"G\"))"
}'
```

## Pick the *right* starter
```shell
curl --request POST \
  --url http://localhost:8001/rce \
  --header 'Content-Type: application/json' \
  --data '{
	"Data": ["Charmander", "Bulbasaur", "Bulbasaur"],
	"Query": "(data) => data.Select((d) => d == \"Bulbasaur\" ? \"Charmander\" : d)"
}'
```

## ROT13 yo shit!
(Thanks a lot, https://stackoverflow.com/a/18739120)
```shell
curl --request POST \
--url http://localhost:8001/rce \
--header 'Content-Type: application/json' \
--data '{
"Data": ["hello", "crypto", "lena"],
"Query": "(data) => data.Select(d => !string.IsNullOrEmpty(d) ? new string (d.ToCharArray().Select(s =>  { return (char)(( s >= 97 && s <= 122 ) ? ( (s + 13 > 122 ) ? s - 13 : s + 13) : ( s >= 65 && s <= 90 ? (s + 13 > 90 ? s - 13 : s + 13) : s )); }).ToArray() ) : d)"
}'
```
