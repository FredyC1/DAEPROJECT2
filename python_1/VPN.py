import socket
import threading

# Proxy server configuration
proxy_host = '127.0.0.1'  # Localhost for the proxy server
proxy_port = 8888          # Port on which the proxy server will listen

# Destination server configuration
destination_host = 'google.com'  # Hostname of the destination server
destination_port = 80             # Port for HTTP traffic

def handle_client(client_socket):
    """Handles communication between the client and the destination server."""
    try:
        # Create a socket to connect to the destination server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((destination_host, destination_port))  # Connect to the destination server

        # Set timeouts to avoid hanging indefinitely on reads
        client_socket.settimeout(5)
        server_socket.settimeout(5)

        while True:
            try:
                # Receive data sent by the client
                client_data = client_socket.recv(4096)  # Buffer size of 4096 bytes
                if len(client_data) == 0:
                    # No data received, exit the loop
                    break

                # Forward the received data to the destination server
                server_socket.sendall(client_data)

                # Receive the response from the destination server
                server_response = server_socket.recv(4096)  # Buffer size of 4096 bytes
                if len(server_response) == 0:
                    # No response received, exit the loop
                    break

                # Send the server's response back to the client
                client_socket.sendall(server_response)

            except socket.timeout:
                # Handle socket timeout exception
                print("Socket timeout. Closing connection.")
                break

    except Exception as e:
        # Log any error that occurs while handling the client
        print(f"Error handling client: {e}")

    finally:
        # Ensure both sockets are closed to free up resources
        client_socket.close()
        server_socket.close()

def start_proxy():
    """Initializes and starts the proxy server."""
    # Create a socket object for the proxy
    proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Set socket options to allow address reuse
    proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind the proxy server to the specified host and port
    proxy.bind((proxy_host, proxy_port))
    
    # Listen for incoming client connections, with a backlog of 5
    proxy.listen(5)

    print(f"Proxy server listening on {proxy_host}:{proxy_port}")

    try:
        while True:
            # Accept a connection from a client
            client_socket, addr = proxy.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")

            # Start a new thread to handle the client connection
            client_handle = threading.Thread(target=handle_client, args=(client_socket,))
            client_handle.start()

    except KeyboardInterrupt:
        # Gracefully shut down the proxy server on keyboard interrupt (Ctrl+C)
        print("Shutting down proxy server.")
    finally:
        # Ensure the proxy socket is closed
        proxy.close()

if __name__ == "__main__":
    start_proxy()  # Start the proxy server when the script is run

# Reqirments 
Server = True
Server = ['proxy', 'VPN', 'Socket']