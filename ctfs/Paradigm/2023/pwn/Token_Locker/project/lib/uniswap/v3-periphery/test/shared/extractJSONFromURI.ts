export function extractJSONFromURI(uri: string): { name: string; description: string; image: string } {
  const encodedJSON = uri.substr('data:application/json;base64,'.length)
  const decodedJSON = Buffer.from(encodedJSON, 'base64').toString('utf8')
  return JSON.parse(decodedJSON)
}
