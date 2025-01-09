import requests
import hashlib


def clear():
    print("\033c")


def main():
    #Account system

    q = input("Would you like to Create account or Log in [0/1]\n> ")

    if q == "0":
        clear()

        print("==============\nCreate Account\n==============\n\n")
        username = input("Enter username: ")
        password = input("Enter Password: ") #immediately hash so is never stored in memory

        hashobj = hashlib.sha256(str.encode(password))
        password = hashobj.hexdigest()

        d = {'command': "CreateAccount",
             "args" : {'username' : username, 'password' : password}}
        
        #headers = {'Content-Length': str(len(d))}
        r = requests.post("http://localhost:8000/", json = d)
        print(r.text)

    elif q == "1":
        clear()

        print("======\nLog in\n======\n\n")
    
        username = input("Enter username: ")
        password = input("Enter Password: ")

        hashobj = hashlib.sha256(str.encode(password))
        password = hashobj.hexdigest()

        d = {'command': "SignIn",
             "args" : {'username' : username, 'password' : password}}

        r = requests.post("http://localhost:8000/", json = d)
        print(r.text)

if __name__ == "__main__":
    main()








"""
accounts system to be stored on the server
folder for each account for text files to be created edited and stored in
sending get and post requests to the server to store and save files
allow editing from multiple accounts



======
SERVER
======

    ACCOUNTS
    --------
    SQL database
    hash the passwords
    possibly email system if i have time otherwise just usernames
    each user has their own folder, security tbd


    REQUESTS
    --------
    handle requests from client

        create account
        (username, password) - creates an account adds to database, hashes
                               and creates the folder and enters folder

        Login
        (username, password) - checks database for the username,
                               hashes password and checks against db
                               if correct logs in and enters folder
        
        create - create a file
        type - input the newly typed characters into the current document
        

======
CLIENT
======

    INTERFACE
    ---------
    TKinter interface essentially barebones text editor
    will add functionality if time but not main concern
    only needs to be able to 


    REQUESTS
    --------
    will have to wait maybe a second to wait for
    extra inputs to avoid sending too many requests



End to end encryption
---------------------
AES
encrypt data in requests, where to store keys on server?




record locking
serialisaion, time stamp processing
commitment ordering - incase ppl commit at same time



client sends post rq to server, server logs request with time and
sends post request back to the client with updated content

if 2 people editing will favor person whos request has the earliest timestamt


==============
ACCOUNT SYSTEM
==============

create or log into account

where start?
just prompt and hash on clientside then do sql on server

    Create
    ------
        Client
        ------
            post request consisting of username and hashed password
            hashing is done clientside obviously

        Server
        ------
            validate username and password to ensure username not in use
            add username and password to sql database


    Sign in
    -------
        Client
        ------
            Send get rq to server with username and hashed password
            once session token is recieved will store it as header for
            future requests

            store it in json file?
            On startup will attempt to use token, if invalid will prompt login


        Server
        ------
            Recieve username and password and return unique session token
            to the client and store it for that users session
            
            Token will expire after x amount of time

    
    
on window close send request to sign out
security levels on acocunts for session log in time?

"""
