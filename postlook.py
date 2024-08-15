from postman_collection import postman_collections
from postman_teams import postman_teams
from postman_requests import postman_requests
import argparse

# Setting up argument parsing
parser = argparse.ArgumentParser(description="Postlook is a tool that helps extract publicly available information related to organizations on Postman.")
parser.add_argument('-q', '--query', metavar='<Organization Name>', type=str, required=True, help='Enter the keyword to search for')
parser.add_argument('-o', '--output', metavar='<Output File Name>', type=str, help='Specify the output file name')

args = parser.parse_args()
query = args.query
output_file = args.output

# ASCII art and strings (using raw string to avoid invalid escape sequences)
postman_art = r'''
    ____             __  __            __  
   / __ \____  _____/ /_/ /___  ____  / /__
  / /_/ / __ \/ ___/ __/ / __ \/ __ \/ //_/
 / ____/ /_/ (__  ) /_/ / /_/ / /_/ / ,<   
/_/    \____/____/\__/_/\____/\____/_/|_|
'''

postman_monitoring = "            POSTMAN MONITORING"
twitter = "    Follow me on Twitter: @dhananjaygarg_"

# Printing output to the console
print("\n")
print(postman_art)
print("\n")

print(" " + postman_monitoring)
print(" " + twitter)
print("\n")

print("[+] Publicly Exposed - Workspaces and Collections")
print("\n")
collections_output = postman_collections(query)
print(collections_output)

print("\n")
print("[+] Publicly Exposed - Teams")
print("\n")
teams_output = postman_teams(query)
print(teams_output)

print("\n")
print("[+] Publicly Exposed - API Requests")
print("\n")
requests_output = postman_requests(query)
print(requests_output)

print("\n" + "  " + "─" * 50 + "\n")

# Writing to output file if specified
if output_file:
    with open(output_file, 'w') as file:
        output = ""

        output += "\n"
        output += postman_art
        output += "\n"

        output += " " + postman_monitoring
        output += "\n"
        output += " " + twitter
        output += "\n"

        output += "[+] Publicly Exposed - Workspaces and Collections\n"
        output += collections_output
        output += "\n"

        output += "[+] Publicly Exposed - Teams\n"
        output += teams_output
        output += "\n"

        output += "[+] Publicly Exposed - API Requests\n"
        output += requests_output
        output += "\n"

        output += "  " + "─" * 50 + "\n"

        file.write(output)
