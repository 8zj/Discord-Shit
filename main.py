#imports
import http.client,secrets,json,string,os,datetime,requests,socket

#from
from pystyle import Colors, Colorate

################
#install pystyle
################

########
#Stuff
#######
# Calculate request duration
request_start_time = datetime.datetime.now()
# Perform your API request here
# ...

# Calculate the time taken for the request in milliseconds
request_duration_ms = (datetime.datetime.now() - request_start_time).total_seconds() * 1000

# Function to generate a random cookie
def generate_random_cookie(length=16):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()_+"
    return ''.join(secrets.choice(characters) for _ in range(length))

def get_channels_info(guild_id, random_cookie, payload, headers):
    conn = http.client.HTTPSConnection("discord.com")
    conn.request("GET", f"/api/v9/guilds/{guild_id}/channels", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    
    try:
        # Ensure that the response is a valid JSON
        channels_info = json.loads(data)
    except json.JSONDecodeError:
        print("Error: Unable to decode response data as JSON.")
        return None, None

    if isinstance(channels_info, dict) and channels_info.get('message'):
        print(f"Error from Discord API: {channels_info['message']}")
        return None, None

    return channels_info, res



def get_website_info(website_url):
    try:
        # Send a HEAD request to get server information and response time
        response = requests.head(website_url)
        server_info = response.headers.get('server', 'N/A')
        response_time = response.elapsed.total_seconds() * 1000  # in milliseconds

        # Get the IP address of the website
        ip_address = socket.gethostbyname("discord.com")

        # You can add more info as needed based on your requirements

        return f"""
        Website IP Address: {ip_address}
        Server Info: {server_info}
        Response Time: {response_time:.2f} ms
        """
    except Exception as e:
        return f"Error fetching additional website info: {str(e)}"


def main():
    token = input("Bot Token : ")
    guild_id = input("Enter guild ID: ")
    random_cookie = generate_random_cookie(length=32)
    
    # Set the payload and headers
    payload = ""
    headers = {
        'cookie': f"random_cookie={random_cookie}",
        'authorization': f"Bot {token}"
    }
    
    # Get channels information
    channels_info, res = get_channels_info(guild_id, random_cookie, payload, headers)
    if channels_info is None:
        return
    
    # Count the number of channels
    channel_count = len(channels_info)
    
    # Print API request details
    website_info = get_website_info('https://discord.com')

    # Get the current timestamp when making the request
    request_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Format API request details with more information
    request_details = f"""
    API Request Details:
    Request Method: GET
    Request URL: discord.com/api/v9/guilds/{guild_id}
    Request Headers:
    {', '.join([f'{key}: {value}' for key, value in headers.items()])}
    Request Timestamp: {request_timestamp}  # Timestamp when the request was made
    Additional Website Info:
    {website_info}
    """

    # Print API response details
    quarter_length = len(random_cookie) // 1
    response_details = f"""
API Response Details:
  Response Status: {res.status}
  Response Reason: {res.reason}
  Response Headers:
  {', '.join([f'{header}: {value}' for header, value in res.getheaders()])}

                      [ + ] Other Info [ + ]
                            Cookie Used: {random_cookie[:quarter_length]}
                            Website URL: https://discord.com/api/v9/guilds/{guild_id}
                            Request Timestamp: {request_start_time.strftime('%Y-%m-%d %H:%M:%S')}
                            Response Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                            Request Took: {request_duration_ms:.2f} ms
"""
    
    os.system("cls")
    print(Colorate.Horizontal(Colors.white_to_green, f"{request_details}", 1))
    print(Colorate.Horizontal(Colors.white_to_blue, f"{response_details}", 1))

    # Assuming the response is a list of dictionaries
    channel_names = [channel['name'] for channel in channels_info]

    # Write the data to a JSON file
    with open('channel.json', 'w') as json_file:
        json.dump(channel_names, json_file, indent=4)

    print('Channels information saved to channels_info.json')



if __name__ == "__main__":
    main()
