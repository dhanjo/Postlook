from postman_collection import postman_collections
from postman_teams import postman_teams
from postman_requests import postman_requests


print("\n")
print("**********POSTLOOK**********")
print("\n")
print("   Postman Monitoring Suite   ")

print("\n")
print("[+]Publicly Exposed - Workspaces and Collections")
print("\n")
postman_collections()

print("\n")
print("[+]Publicly Exposed - Teams")
print("\n")
postman_teams()

print("\n")
print("[+]Publicly Exposed - API Request")
print("\n")
postman_requests()

print("------------------------------------------")



