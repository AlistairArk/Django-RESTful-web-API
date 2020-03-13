Using the client

To operate the client, cmd into the “myclient” directory and run the following in your terminal:

    pip install requests
    python client.py

Ensure you are using python 3. Note, you may need to run this from within a virtual environment if attempting to run it off DEC-10 machines as DEC-10’s version of requests may be out of date. 


Superuser Admin Cradentials:
    sc17jhd.pythonanywhere.com/admin
    ammar
    pass123


Command syntax:

Register to the service.
    register

Login to the service
    login sc17jhd.pythonanywhere.com

Logout from the current session
    logout

List all module instances and the professor(s) teaching each of them.
    list

View the rating of all professors
    view

View the Average rating of a certain professor in a certain module
    average professor_id module_code

Rate the teaching of a certain professor in a certain module instance
    rate professor_id module_code year semester rating

Terminate Program
    exit

List Commands
    help
