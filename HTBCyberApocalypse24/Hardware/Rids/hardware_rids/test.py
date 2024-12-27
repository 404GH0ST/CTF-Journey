import socket
import json

def read_data(start_address, length):
    # Configure according to your setup
    host = '94.237.48.117'  # The server's hostname or IP address
    port = 32737            # The port used by the server
    cs = 0                  # /CS on A*BUS3 (range: A*BUS3 to A*BUS7)
    usb_device_url = 'ftdi://ftdi:2232h/1'

    # Prepare the command data for read operation
    command_data = {
        "tool": "pyftdi",
        "cs_pin":  cs,
        "url":  usb_device_url,
        "start_address": start_address,
        "length": length
    }
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        # Serialize data to JSON and send
        s.sendall(json.dumps(command_data).encode('utf-8'))
        
        # Receive and process response
        data = b''
        while True:
            data += s.recv(1024)
            if data.endswith(b'}'):
                break
                
        response = json.loads(data.decode('utf-8'))
        print(f"Received: {response}")
    return response

# Example usage
start_address = 0x1000  # Example start address to read from
length = 256            # Example length of data to read
read_result = read_data(start_address, length)
print(read_result)

