import sys
import os

from s1_api_wrapper import *




##################################################
## Helper functions
def writeJsonToFile(filename, jsondata):
    with open(filename, 'w', encoding='utf-8') as outfile:
        json.dump(jsondata, outfile, indent=4)

    return 1

def printSep():
    i=os.get_terminal_size().columns
    while i > 0: i-=1; print("-", end = '')







##################################################
## Call functions
def executeCall(s1client, command, filter, data):
    print(f'Command {command} called')
    try:
        if command == 's1_get_agents':
            # Get the Agents, and their data
            resp = get_agents(s1client)
            return resp

        elif command == 's1_get_agents_filter':
            # Get the Agents, and their data
            resp = get_agents_filter(s1client, filter)
            return resp

        elif command == 's1_get_threats_filter':
            # Get the Threats, and their data
            resp = get_threats_filter(s1client, filter)
            return resp

        elif command == 's1_disconnect_from_network':
            # Disconnect client from network
            resp = disconnect_from_network(s1client, data)
            return resp

        elif command == 's1_update_threat':
            # Update threat
            resp = update_threat(s1client, data)
            return resp

        else:
            errmsg = f'Command {command} not found'
            print(errmsg)
            raise ApiError(errmsg)

    # Log exceptions
    except Exception as e:
        error_message = f'Failed to execute {command} command. Error: '
        print(error_message + str(e.args[0]))

    return 0



##################################################
## SentinelOne test playbook
def s1playbook(config_file):
    # Create SentinalOne api client
    client = S1Client(config_file)

    #Get Agents
    print('\n\n### Get Agents')
    command = 's1_get_agents'
    resp = executeCall(client, command, None, None)
    if resp != 0:
        print("\nResult:\n" + resp)
        printSep()

    #Get Agents Filter by groupid
    print('\n\n### Get Agents filter by groupid')
    command = 's1_get_agents_filter'
    with open("./examples/in_get-agents.json", "r") as read_file:
        filter = json.dumps(json.load(read_file), indent=4)
    resp = executeCall(client, command, filter, None)
    if resp != 0:
        print("\nResult:\n" + resp)
        printSep()

    #Disconnect a given client
    print('\n\n### Disconnect a given client')
    command = 's1_disconnect_from_network'
    with open("./examples/in_disconnect.json", "r") as read_file:
        data = json.dumps(json.load(read_file), indent=4)

    resp = executeCall(client, command, None, data)
    if resp != 0:
        print("\nResult:\n" + resp)
        printSep()

    #Get Threats filtered by groupid
    print('\n\n### Update Threats')
    command = 's1_update_threat'
    with open("./examples/in_update-threats.json", "r") as read_file:
        data = json.dumps(json.load(read_file), indent=4)
    resp = executeCall(client, command, None, data)
    if resp != 0:
        print("\nResult:\n" + resp)
        printSep()





if __name__ in ('__main__'):
    if len(sys.argv) < 2:
        print('Provide the path to the SentinelOne API config file as argument')
        sys.exit()

    config_file = sys.argv[1]

    if not os.path.isfile(config_file):
        print('The specified file does not exist')
        sys.exit()

    # Read config file
    with open(config_file, "r") as read_file:
        config = json.load(read_file)

    # Run a test on the sentinal one api
    s1playbook(config)
