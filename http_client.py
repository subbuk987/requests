import http.client
import json

def send_to_server(filename, data):
    """
    Sends a POST request to the local server at http://localhost:8000/append
    with a JSON body containing the filename and content to be appended.

    Parameters:
    - filename (str): The name of the file to which the content will be appended.
    - data (str): The content to be appended to the file.

    This function:
    - Sends the data in JSON format.
    - Adds a custom header ("X-User") to identify the user.
    - Reads the response from the server.
    - Prints the status code, reason, custom header, and the response body.
    """
    # Establish HTTP connection to the server
    conn = http.client.HTTPConnection("localhost", 8000)

    # Define request headers
    headers = {
        "Content-Type": "application/json",  # Inform server the body is JSON
        "X-User": "Subramanyam"              # Custom header to send user info
    }

    # Prepare the JSON body
    data = json.dumps({
        "filename": filename,
        "data": data
    })

    # Send POST request to the server at path "/append"
    conn.request("POST", "/append", headers=headers, body=data)

    # Get the response from the server
    response = conn.getresponse()
    response_data = response.read().decode()  # Decode the byte response

    # Print response details
    print("Response Status: ", response.status)
    print("Response Reason:", response.reason)
    print("Custom Header:", response.getheader("X-File-Appended"))
    print("Response Data: ", response_data)

    # Close the connection
    conn.close()


if __name__ == "__main__":
    # Get user inputs
    file_name = input("Enter the File Name: ")
    content = input("Enter the content to be appended: ")

    # Send data to the server
    send_to_server(file_name, content)
