import datetime

def time_now():

    # Get the current date and time
    now = datetime.datetime.now()

    # Convert the date and time to an integer using the timestamp() method
    timestamp = int(now.timestamp())
    return timestamp

get_client_id_msg = "Please enter client ID:"
server_ip = "127.0.0.1"
server_port = 7999
successful_connection = "connection_established"