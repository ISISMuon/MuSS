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



def server_connection_tread(object_of_class):
    """
    initiate the socket, have it lsitening (to multiple clients), recieving and interpreting incoming messages from client
    """
    comunication_socket = None #is it necessaary?

    # the socket is created and listening
    define_and_create_socket(object_of_class)

    #time laps to guaratee all varaibles have been created
    time.sleep(3)  

    # inable the socket to always be lookung for clients and messages
    thread = threading.Thread(
        target=handle_connection_receive_thread, args=(object_of_class,), daemon=True)
    thread.start()
    
    #once the socket has been connected desable the btn
    object_of_class.statess = "disabled" 
    object_of_class.connect_btn.configure(state='disabled')


def define_and_create_socket(object_of_class):
    '''
    sockets server is defined as global scks, retrieving Host and Port values fom UI 
    '''
    global scks

    #Retrieve host and Port from UI corresponding entries
    Host = object_of_class.host_entry.get()
    PORT = int(object_of_class.port_entry.get())

    # define soxket type and start the lsitening process
    scks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scks.bind((Host, PORT))
    scks.listen()

    # Debug Message
    print('Server is listening')


def handle_connection_receive_thread(object_of_class):
    """
    The connection to the client is established and the information printed
    thread starts to recieve any ongoing messages
    """
    # adress and comunication_socke are defined as a way to reference and intercept the connection
    global adress
    global comunication_socket

    # retrive the information on the connection and start recieving in commung messages from client
    # this allow the multiple client to connect to the server aat differents times
    while True:
        comunication_socket, adress = scks.accept()
        print('communication socket', comunication_socket, 'adressss', adress, 'types', type(
            comunication_socket), 'type of the adress', type(adress))

        print(f'Connection from {adress} has been established')
        
        #ready  to receive aand interpret in coming messages
        receive_message_thread = threading.Thread(target=sckt_receive_and_interpret_message,
                                   args=(object_of_class,), daemon=True)
        receive_message_thread.start()

# -------------------------------------------------------------------------------------------------------
#                                           Disconnect
# -------------------------------------------------------------------------------------------------------

def disconnect_socket():
    """
    Disconnect the socket from the client and closes it
    """
    
    comunication_socket.shutdown(socket.SHUT_RDWR)
    comunication_socket.close()

# -------------------------------------------------------------------------------------------------------
#                                           Recieve
# -------------------------------------------------------------------------------------------------------

keys=['param','Delphi','timefrom + timeto']

def sckt_receive_and_interpret_message(object_of_class):  
    """
    Interprets the message recieved and according to the key perform the next task
    """
    
    # the socket is waiting to recieve a message at any point
    while True:
        #decode the message so it can be interpreted
        message = comunication_socket.recv(1024).decode('utf-8')
        # handling the absence of a message ()
        if not message:
            break
        # the recieved data (a string) is processed
        message = message.replace("\r\n", "")

        # when fitting the parameters the kry 'param' is send in the beguining of the sting from WiMDA
        if 'param' in message:
            # key word 'param' is eliminated
            message_processed = message.replace('param', '')
            # the data recieved is stored as 'fit_params_to_generate_simulation' as is the current parameters generating new simulation data
            object_of_class.fit_params_to_generate_simulation = message_processed
            # DEBUG1
            print('################################ IF WE RECIEVE A MESSAGE WITH THE KEY PARAM',object_of_class.fit_params_to_generate_simulation, object_of_class.fit_state)
            #in the case this is a repeated set of parameters (by checking the stored paraneters)
            if object_of_class.fit_params_to_generate_simulation in object_of_class.result_dic:
                object_of_class.event_generate('<<SendResultStored>>')
                # Debug print
                print(f'---------------------------------------------- The set of parameters {object_of_class.fit_params_to_generate_simulation} has been recieved before              The simulation results sent were stored previously')  

            # new set of parameters has been recieved                
            else:
                # reenforce that the fitting is in process
                object_of_class.fit_state = True
                # the parameters are updated as the new atomistic variables and the calculations run to be later sent
                # DEBUG1
                print('################################ IF THE MESSAGE HAS NOT BEEN RECIEVED BEFORE',object_of_class.fit_params_to_generate_simulation, object_of_class.fit_state)
                object_of_class.event_generate('<<CalculateSend>>')
                # Debug print
                print(f'++++++++++++++++++++++++++++++++++++++++++++++ The set of parameters {object_of_class.fit_params_to_generate_simulation} have been used to generate new simmulation       The results will be sent shortly')
        
        #completed message on fitting (this was used in case of abort fitting but dind work as intended)
        elif message == 'Fit Completed':
            # assert that the fitting process is terminated as to enable MuSS for other taks
            object_of_class.fit_state = False
            object_of_class.event_generate('<<ThreadFinished>>')
            # Debug print
            print(f'=================================================== The following message was recieved {message} ')

        # Recieveing initial characterization of the system in WiMDA (to be completed)
        if 'TimeFrom' and 'TimeTo' in message:
            object_of_class.wimda_time = message
            # Debug print
            print(message)

# -------------------------------------------------------------------------------------------------------
#                                           Send
# -------------------------------------------------------------------------------------------------------
def sckt_send_function(processed_data):
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
