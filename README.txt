Client provides email and password, which is sent to the server
Server then verifies that email and password are correct and responds with an auth token
Client stores the token and sends it along with all subsequent requests to the API
Server decodes the token and validates it