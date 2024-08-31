"""
Project: Simulations for muSR data Analysis Industrial Placement
Author: Paula Franco
Date: February 2024

Summary:
    Sockets are created and listens until the program is closes, here ports are descibed.
    The sockets recieve and send informtaion here.
"""
import threading
import socket
import time


# -------------------------------------------------------------------------------------------------------
#                                           Connect
# -------------------------------------------------------------------------------------------------------
def start_server_connection_thread(handler):
    """
    Initializes the socket server, sets it to listen for multiple clients, 
    and starts receiving and interpreting incoming messages from clients.

    Args:
        handler (object): An instance of a class that manages UI elements and server settings.
    """
    comunication_socket = None # Variable initialization (not strictly necessary)

    #Retrieve Host and Port values from the UI
    Host = handler.host_entry.get()
    PORT = int(handler.port_entry.get())

    # Create the socket and start listening for connections
    initialize_and_start_socket_server(Host,PORT)

    # Pause briefly to ensure all variables and components are initialized
    time.sleep(3)  

    # Start a thread to handle client connections and receive messages continuously
    thread = threading.Thread(
        target=handle_connection_receive_thread, args=(handler,), daemon=True)
    thread.start()
    
    # Disable the connect button on the UI once the socket server is running
    handler.statess = "disabled" 
    handler.connect_btn.configure(state='disabled')

def initialize_and_start_socket_server(host,Port):
    '''
    Defines and creates a global socket server,and starts listening for incoming connections.
    
    Args:
        host
        port
    '''
    global scks

    # Define the socket type and start the listening process
    scks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scks.bind((host, Port))
    scks.listen()

    # Debug Message to confirm that the server is now listening
    print('Server is listening')

def handle_connection_receive_thread(object):
    """
    Establishes a connection to the client, prints connection details, 
    and starts a thread to receive and process incoming messages.
    
    Args:
        handler (object): An instance of a class that manages simulation parameters and states.
    """
    # Define address and communication_socket as global variables to reference and intercept the connection
    global adress
    global comunication_socket

    # Continuously listen for and accept connections from clients
    while True:
        comunication_socket, adress = scks.accept()
        print('communication socket', comunication_socket, 'adressss', adress, 'types', type(
            comunication_socket), 'type of the adress', type(adress))

        print(f'Connection from {adress} has been established')
        
        # Start a new thread to receive and process incoming message
        receive_message_thread = threading.Thread(target=receive_and_process_socket_message,
                                   args=(object,), daemon=True)
        receive_message_thread.start()

# -------------------------------------------------------------------------------------------------------
#                                           Disconnect
# -------------------------------------------------------------------------------------------------------

def close_socket_connection():
    """
    Gracefully disconnects the socket from the client and closes the connection.    
    """
    # Shutdown the socket to disable further send and receive operations
    comunication_socket.shutdown(socket.SHUT_RDWR)

    # Close the socket to release the resource
    comunication_socket.close()

# -------------------------------------------------------------------------------------------------------
#                                           Recieve
# -------------------------------------------------------------------------------------------------------

keys=['param','Delphi','timefrom + timeto']

def receive_and_process_socket_message(object_of_class):  
    """
    Receives and interprets messages from a socket, then performs actions based on specific keywords.

    Args:
        handler (object): An instance of a class that handles simulation parameters and states.
    """
    
    # The socket continuously waits to receive messages
    while True:
         # Decode the received message from the socket
        message = comunication_socket.recv(1024).decode('utf-8')

        # Handling the absence of a message
        if not message:
            break

        # Clean up the message by removing unwanted characters
        message = message.replace("\r\n", "")

        # Check if the message contains the 'param' keyword for parameter fitting
        if 'param' in message:
            # Remove the 'param' keyword from the message
            message_processed = message.replace('param', '')

            # Store the processed message as parameters to generate a new simulation            
            object_of_class.fit_params_to_generate_simulation = message_processed

            # DEBUG: Print information about received parameters
            print('################################ IF WE RECIEVE A MESSAGE WITH THE KEY PARAM',object_of_class.fit_params_to_generate_simulation, object_of_class.fit_state)
            
            # Check if these parameters have been received before
            if object_of_class.fit_params_to_generate_simulation in object_of_class.result_dic:
                # Trigger an event to send stored results
                object_of_class.event_generate('<<SendResultStored>>')
                # DEBUG: Print a message indicating the parameters were previously received
                print(f'---------------------------------------------- The set of parameters {object_of_class.fit_params_to_generate_simulation} has been recieved before              The simulation results sent were stored previously')            
            else:
                # Mark the fitting state as activ
                object_of_class.fit_state = True
                # Trigger an event to calculate and send new simulation results
                object_of_class.event_generate('<<CalculateSend>>')
                # DEBUG: Print a message indicating new simulation results are being generated
                print(f'++++++++++++++++++++++++++++++++++++++++++++++ The set of parameters {object_of_class.fit_params_to_generate_simulation} have been used to generate new simmulation       The results will be sent shortly')
        
        # Handle the case where the fitting process is completed
        elif message == 'Fit Completed':
            # Mark the fitting process as complete
            object_of_class.fit_state = False
            # Trigger an event indicating the thread has finished processing
            object_of_class.event_generate('<<ThreadFinished>>')
            # DEBUG: Print a message indicating the fitting process is completedt
            print(f'=================================================== The following message was recieved {message} ')

        # Handle messages related to system characterization from WiMDA
        if 'TimeFrom' and 'TimeTo' in message:
            # Store the time range information in the handler objec
            object_of_class.wimda_time = message
            # Debug print
            print(message)

# -------------------------------------------------------------------------------------------------------
#                                           Send
# -------------------------------------------------------------------------------------------------------
def send_data(processed_data):
    """
    send the processed simulation results  to the client
    Args:
        processed_data (str): The simulation results that have been processed and are ready to be sent to the client.
    """
    #Debug Message
    print('The following message has been sent to the client:  ', processed_data.encode('utf-8'))
    
    # Sending data to the client
    comunication_socket.send(processed_data.encode('utf-8'))
   
# -------------------------------------------------------------------------------------------------------
