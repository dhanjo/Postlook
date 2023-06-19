from postman_collection import postman_collections
from postman_teams import postman_teams
from postman_requests import postman_requests
from colorama import init, Fore, Style
import argparse

init()

parser = argparse.ArgumentParser(description="Postlook is a tool which helps in extracting publicly available information related to organization on postman.")
parser.add_argument('-q', '--query', metavar='<Organization Name>', type=str, help='Enter the keyword to search for')
parser.add_argument('-o', '--output', metavar='<Output File Name>', type=str, help='Specify the output file name')

args = parser.parse_args()
query = args.query
output_file = args.output

if not query and not output_file:
    parser.print_help()
    exit()

postman_art = '''
    ____             __  __            __  
   / __ \____  _____/ /_/ /___  ____  / /__
  / /_/ / __ \/ ___/ __/ / __ \/ __ \/ //_/
 / ____/ /_/ (__  ) /_/ / /_/ / /_/ / ,<   
/_/    \____/____/\__/_/\____/\____/_/|_|
'''

postman_monitoring = "            POSTMAN MONITORING"
twitter = "    Follow me on Twitter: @dhananjaygarg_"
print("\n")
print(Fore.CYAN + Style.BRIGHT + postman_art + Style.RESET_ALL)
print("\n")


print(" " + Fore.YELLOW + postman_monitoring + Style.RESET_ALL)

print(" " + Fore.RED + twitter + Style.RESET_ALL)
print("\n")

print(Fore.GREEN + " [+] Publicly Exposed - Workspaces and Collections" + Style.RESET_ALL)
print("\n")
collections_output = postman_collections(query)
print(collections_output)

print("\n")
print(Fore.GREEN + " [+] Publicly Exposed - Teams" + Style.RESET_ALL)
print("\n")
teams_output = postman_teams(query)
print(teams_output)

print("\n")
print(Fore.GREEN + " [+] Publicly Exposed - API Requests" + Style.RESET_ALL)
print("\n")
requests_output = postman_requests(query)
print(requests_output)

print("\n" + Fore.YELLOW + "  " + "─" * 50 + Style.RESET_ALL + "\n")

if output_file:
    output = ""

    output += "\n"
    output += Fore.CYAN + Style.BRIGHT + postman_art + Style.RESET_ALL
    output += "\n"

    output += " " + Fore.YELLOW + postman_monitoring + Style.RESET_ALL

    output += "\n"

    output += " " + Fore.RED + twitter + Style.RESET_ALL
    output += "\n"

    output += Fore.GREEN + " [+] Publicly Exposed - Workspaces and Collections" + Style.RESET_ALL
    output += "\n"

    output += collections_output
    output += "\n"

    output += Fore.GREEN + " [+] Publicly Exposed - Teams" + Style.RESET_ALL
    output += "\n"

    output += teams_output
    output += "\n"

    output += Fore.GREEN + " [+] Publicly Exposed - API Requests" + Style.RESET_ALL
    output += "\n"

    output += requests_output
    output += "\n"

    output += Fore.YELLOW + "  " + "─" * 50 + Style.RESET_ALL + "\n"

    with open(output_file, 'w') as file:
        file.write(output)
