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
import re
import numpy as np

# -------------------------------------------------------------------------------------------------------
#                                           Connect
# -------------------------------------------------------------------------------------------------------


def server_connection_tread(object_of_class):
    comunication_socket = None
    create_socket(object_of_class)

    time.sleep(3)  # why sleeping
    thread = threading.Thread(
        target=servers, args=(object_of_class,), daemon=True)
    thread.start()

    time.sleep(3)  # why sleeping

    object_of_class.statess = "disabled"
    object_of_class.connect_btn.configure(state='disabled')


def create_socket(object_of_class):
    '''
    socket is defined
    '''
    global scks

    Host = object_of_class.host_entry.get()
    PORT = int(object_of_class.port_entry.get())
    scks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scks.bind((Host, PORT))
    scks.listen()

    print('Server is listening')


def servers(object_of_class):
    global adress
    global comunication_socket

    while True:
        comunication_socket, adress = scks.accept()
        print('communication socket', comunication_socket, 'adressss', adress, 'types', type(
            comunication_socket), 'type of the adress', type(adress))

        print(f'Connection from {adress} has been established')
        # print(type(comunication_socket))
        thread2 = threading.Thread(target=receive,
                                   args=(object_of_class,), daemon=True)
        thread2.start()

# -------------------------------------------------------------------------------------------------------
#                                           Disconnect
# -------------------------------------------------------------------------------------------------------


def disconnect_socket():
    # perhaps is should be that the socktes stops listening
    # if we mantain it using comunication maybe a message to deal with the NameError
    comunication_socket.shutdown(socket.SHUT_RDWR)
    comunication_socket.close()


def receive(object_of_class):  # do we need the (,_)
    global variables
    variables = []

    while True:
        message = comunication_socket.recv(1024).decode('utf-8')
        if not message:
            break
        print(f'Message from client is; {message}')
        message = message.replace("\r\n", "")
        print(message)
        if "Delphi" in message:
            variables.append(message)

        elif 'param' in message:
            message_processed = message.replace('param', '')
            print('====================================', message_processed)
            print(type(message))

            object_of_class.fitting_variables = message_processed

            if object_of_class.fitting_variables in object_of_class.result_dic:
                print('green')
                print('fit var does exist dictionarry')
                print('keys', object_of_class.result_dic.keys())
                object_of_class.event_generate('<<SendResultStored>>')
                print('we have it already')

            else:

                print('blue')
                object_of_class.fit_state = True
                object_of_class.event_generate('<<CalculateSend>>')
                print('do and send calculations')

        if 'TimeFrom' and 'TimeTo' in message:
            object_of_class.wimda_time = message
            print(message)
            pass


def send_function(sending_stuff):
    print('************************************************************************************************************ =>', 'SENT')
    comunication_socket.send(sending_stuff.encode('utf-8'))
    print('what is being sent', sending_stuff.encode('utf-8'))


def send_tread(data):
    thread3 = threading.Thread(target=send_function, args=(data,))
    thread3.start()

# -------------------------------------------------------------------------------------------------------
#                                           Process data
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
#                                                   Drafts
# -------------------------------------------------------------------------------------------------------
def receiver():
    threadd = threading.Thread(target=receive)
    threadd.start()


def run_updated01(object_of_class):
    object_of_class.parameters._keywords["field"] = variables[0]
