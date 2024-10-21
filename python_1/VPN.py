import socket
import threading

# Proxy server configuration
proxy_host = '127.0.0.1'
proxy_port = 8888

# Destination server configuration
destination_host = 'google.com'
destination_port = 80

def handle_client(client_socket):
    try:
        # Connect to the destination server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((destination_host, destination_port))

        # Set timeouts to avoid hanging
        client_socket.settimeout(5)
        server_socket.settimeout(5)

        while True:
            try:
                # Receive data from the client
                client_data = client_socket.recv(4096)
                if len(client_data) == 0:
                    break

                # Forward data to the destination server
                server_socket.sendall(client_data)

                # Receive data from the destination server
                server_response = server_socket.recv(4096)
                if len(server_response) == 0:
                    break

                # Forward the server's response back to the client
                client_socket.sendall(server_response)
            
            except socket.timeout:
                # Timeout occurred, break out of the loop
                print("Socket timeout. Closing connection.")
                break

    except Exception as e:
        print(f"Error handling client: {e}")
    
    finally:
        # Close the connections
        client_socket.close()
        server_socket.close()
# runs the proxy
def start_proxy():
    # Create a socket object
    proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Reuse the address to avoid 'address already in use' errors
    proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to a host and port
    proxy.bind((proxy_host, proxy_port))
    # Listen for incoming connections
    proxy.listen(5)

    print(f"Proxy server listening on {proxy_host}:{proxy_port}")

    try:
        while True:
            client_socket, addr = proxy.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")

            # Start a new thread to handle the client
            client_handle = threading.Thread(target=handle_client, args=(client_socket,))
            client_handle.start()

    except KeyboardInterrupt:
        print("Shutting down proxy server.")
    finally:
        proxy.close()

if __name__ == "__main__":
    start_proxy()

# Reqirments 
Server = True
Server = ['proxy', 'VPN', 'Socket']