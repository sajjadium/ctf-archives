A modern rerun of a SHA2017 challenge...

It was based on a real-life bug where the developers used this technique to turn a string containing "true" into a Python boolean:
with urllib.request.urlopen("<ATTACKER CONTROLLED>") as f:
   api_response = json.loads(f.read())
   boolean_value = eval(api_response["some_field"].title())
