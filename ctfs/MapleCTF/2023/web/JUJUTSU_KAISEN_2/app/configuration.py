import os


PORT = os.environ.get('PORT', 9080)
GRAPHQL_ENDPOINT = "http://jjk_db:9090"
ADMIN_NAME = os.environ.get('ADMIN_NAME', 'via')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'via')

QUERY = '''
            { 
            getCharacters {
            edges {
            node {
                name,
                occupation,
                cursedTechnique,
                notes
            }
            }
        }
        }
        '''

MUTATION = '''
                mutation {{
                    addNewCharacter (input:{{
                        name:"{name}"
                        occupation: "{occupation}",
                        notes: "{notes}"
                        cursedTechnique: "{ct}"
                    }}) {{
                    status
                    }}
                }}
        '''
