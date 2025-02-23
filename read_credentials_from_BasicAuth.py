import base64


def generate_basic_auth_token(username, password):
    # Concatenate username and password with a colon
    credentials = f"{username}:{password}"
    
    # Encode the credentials in base64
    encoded_bytes = base64.b64encode(credentials.encode("utf-8"))
    
    # Convert the bytes to a string
    encoded_str = encoded_bytes.decode("utf-8")
    
    # Add the "Basic " prefix
    return f"Basic {encoded_str}"


def extract_credentials(auth_token):
    # Remove the "Basic " prefix if present
    if auth_token.startswith("Basic "):
        auth_token = auth_token[6:]

    # Decode the base64-encoded string
    decoded_bytes = base64.b64decode(auth_token)
    decoded_str = decoded_bytes.decode("utf-8")

    # Split the decoded string into username and password
    username, password = decoded_str.split(":", 1)
    return username, password

# Example Usage
username = "username"
password = "password"
auth_token = generate_basic_auth_token(username, password)
print(f"Generated Auth Token: {auth_token}")

username, password = extract_credentials(auth_token)
print(f"Username: {username}")
print(f"Password: {password}")
