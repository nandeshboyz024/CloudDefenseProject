import requests
from requests.auth import HTTPBasicAuth

import re
import base64



def parse_dependencies(xml_content):
    pattern = r'<dependency>\s*<groupId>(.*?)</groupId>\s*<artifactId>(.*?)</artifactId>(?:\s*<version>(.*?)</version>)?.*?</dependency>'
    
    matches = re.findall(pattern, xml_content, re.DOTALL)
    
    for match in matches:
        groupId, artifactId, version = match
        version = version if version else "No version specified"
        print(f"GroupId: {groupId.strip()}, ArtifactId: {artifactId.strip()}, Version: {version.strip()}")


username = input("Enter your GitHub username: ")
password = input("Enter your GitHub password: ")


response = requests.get(f"https://api.github.com/users/{username}/repos", auth=HTTPBasicAuth(username, password))

if response.status_code == 200:
    print('Your repositories:')
    repositories = response.json()
    for repo in repositories:
        print(repo['name'])
else:
    print(f"Failed to fetch repositories. Status code: {response.status_code}")

repo_name= input("Enter your GitHub repo to print dependencies: ")

response = requests.get(f"https://api.github.com/repos/{username}/{repo_name}/contents", auth=HTTPBasicAuth(username, password))


if(response.status_code!=200):
    print(f"Failed to fetch contents. Status code: {response.status_code}")


response = requests.get(f"https://api.github.com/repos/{username}/{repo_name}/contents/pom.xml",
                        auth=(username, password))


if response.status_code == 200:
    file_content = response.json()['content']
    pom_content = base64.b64decode(file_content).decode('utf-8')
    parse_dependencies(pom_content)
else:
    print(f"Failed to fetch pom.xml file. Status code: {response.status_code}")


