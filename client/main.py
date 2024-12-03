import requests


def main():
    #r = requests.get('http://10.0.125.138:8000/a.txt')
    r = requests.get('http://localhost:8000/')

    #print(r.text)
    print(r)

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

"""
