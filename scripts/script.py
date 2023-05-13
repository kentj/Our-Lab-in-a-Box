import os
import urllib.request
import ssl
from string import Template

def getInput(prompt):
   print("\n\n")
   
   success = False
   while not success:
      result = input(prompt)
      confirmation = confirmInput(result)	    
      if confirmation in ('Y','y'):
          return result

def confirmInput(result):
   print("You entered: '" + result + "'")
   flag=''
   while flag not in ('Y','y','N','n'):
      flag = input("Is this correct? (y/n)")
   return flag

def getURLContent(URL):
   print(f"Fetching content at {URL}")
   with urllib.request.urlopen(URL, context=ssl._create_unverified_context() ) as f:
      data = f.read()
   return data

def writeFileContent(fileName, data_to_write):
   print(f"Writing file: {fileName}")
   print(f"Data: {data_to_write}")
   outputFile = open(fileName, 'w')
   outputFile.write(data_to_write)
   outputFile.close()
   return

def transformTemplate(variables, template_URL, fileName):
   print(f"Template: {template_URL}",f"File: {fileName}")
   try:
      template_data = getURLContent(templateURL).decode('utf-8')
      template = Template(template_data)
      completed_template_data = template.substitute(variables)
      writeFileContent(fileName, completed_template_data)
   except Exception as e:
      print(e)
      return False
   
   return True

variables = {'PWD' : '$PWD'}

labAbbreviation = getInput("Lab abbreviation: ")
variables['labAbbreviation'] = labAbbreviation.lower()

fqdnEnding = getInput("Final segment of lab's FQDN (org, test, etc): ")
variables['fqdnEnding'] = fqdnEnding

labPassword = getInput("Global lab administrator password: ")
variables['labPassword'] = labPassword

print("Lab-in-a-Box Setup and Configuration Tool v0.1")
print("----------------------------------------------\n")
print("Summary of your inputs and calculated values: ")
print(f"01: Lab Abbreviation: {labAbbreviation}")

labName = labAbbreviation + "-lab"
labNameUnderscoredUpper = (labAbbreviation + "_lab").upper()
variables['labName'] = labName
variables['labNameUnderscoredUpper'] = labNameUnderscoredUpper
print(f"02: Lab Name: {labName}")
print(f"03: Lab Name UnderScore Uppercase: {labNameUnderscoredUpper}")
print(f"04: Lab password: {labPassword}")
print(f"05: Lab FQDN ending: {fqdnEnding}")
rootCADirectory = labAbbreviation.upper() + "-Lab-CA"
variables['rootCADirectory'] = rootCADirectory
rootCA_certificate_file = rootCADirectory + '.crt'
variables['rootCA_certificate_file'] = rootCA_certificate_file
rootCA_certificate_key_file = rootCADirectory + ".key"
variables['rootCA_certificate_key_file'] = rootCA_certificate_key_file

print(f"06: Lab Root Certificate Authority Directory: {rootCADirectory}")
print(f"06a. Lab Root CA Certificate File: {rootCA_certificate_file}")
print(f"06b. Lab Root CA Certificate Key File: {rootCA_certificate_key_file}")

lab_base_URL = f"{labName}.nccoe.{fqdnEnding}"
variables['lab_base_URL'] = lab_base_URL
print(f"07. Lab Base URL: {lab_base_URL}")

certificate_file_suffix = lab_base_URL + ".crt"
variables['certificate_file_suffix'] = certificate_file_suffix
certificate_key_file_suffix = lab_base_URL + ".key"
variables['certificate_key_file_suffix'] = certificate_key_file_suffix

guacamole_certificate_file = 'guacamole.' + certificate_file_suffix
variables['guacamole_certificate_file'] = guacamole_certificate_file
guacamole_certificate_key_file = 'guacamole.' + certificate_key_file_suffix
variables['guacamole_certificate_key_file'] = guacamole_certificate_key_file
print(f"08a. Guacamole Certificate File: {guacamole_certificate_file}")
print(f"08b. Guacamole Certificate Key File: {guacamole_certificate_key_file}")

keycloak_certificate_file = 'keycloak.' + certificate_file_suffix
variables['keycloak_certificate_file'] = keycloak_certificate_file
keycloak_certificate_key_file = 'keycloak.' + certificate_key_file_suffix
variables['keycloak_certificate_key_file'] = keycloak_certificate_key_file
print(f"09a. Keycloak Certificate File: {keycloak_certificate_file}")
print(f"09b. Keycloak Certificate Key File: {keycloak_certificate_key_file}")

minio_certificate_file = 'minio.' + certificate_file_suffix
variables['minio_certificate_file'] = minio_certificate_file
minio_certificate_key_file = 'minio.' + certificate_key_file_suffix
variables['minio_certificate_key_file'] = minio_certificate_key_file
print(f"10a. MinIO Certificate File: {minio_certificate_file}")
print(f"10b. MinIO Certificate Key File: {minio_certificate_key_file}")

remote_certificate_file = 'remote.' + certificate_file_suffix
variables['remote_certificate_file'] = remote_certificate_file
remote_certificate_key_file = 'remote.' + certificate_key_file_suffix
variables['remote_certificate_key_file'] = remote_certificate_key_file
print(f"11a. Remote Certificate File: {remote_certificate_file}")
print(f"11b. Remote Certificate Key File: {remote_certificate_key_file}")

print("\nMaking system changes...\n")
print("Step 1:  Creating directories...")

directory_base='./home/administrator/'
for x in [ 'guacamole','guacamole/caddy',
           'guacamole/caddy/config',
           'guacamole/caddy/data',
           f'guacamole/certs/{rootCADirectory}',
           'guacamole/certs/guacamole',
           'guacamole/certs/keycloak',
           'guacamole/certs/minio',
           'guacamole/certs/remote',
           'guacamole/guacamole_build',
           'guacamole/guacdb/databases',
           'guacamole/guacdb/init',
           'guacamole/keycloakdb/databases'
         ]:
   directory = directory_base + x
   print(f'.... Creating directory{directory}')
   os.makedirs(directory)

print("\nStep 2:  Creating files from templates...\n")

baseURL = "https://raw.githubusercontent.com/kentj/Our-Lab-in-a-Box/main/templates/"
templateSuffix = '.template'
baseLocation = "./home/administrator/guacamole/"

for x in [ ['Caddyfile', 'caddy/Caddfile'],
           ['Dockerfile', 'guacamole_build/Dockerfile'],
           ['env', '.env'],
           ['caddy_reload.sh', 'caddy_reload.sh'],
           ['docker-compose.yaml.initializeOpenLDAP', 'docker-compose.yaml.initializeOpenLDAP'],
           ['docker-compose.yaml', 'docker-compose.yaml'] ]:
   print(f".... Rendering template {x[0]}.template to file {x[1]}")
   templateURL = baseURL + x[0] + templateSuffix
   fileName = baseLocation + x[1]
   result = transformTemplate(variables, templateURL, fileName)
   if result == True:
      print(f"Completion of template for {x[0]} sucessful!\n")
   else:
      print(f"Failed...\n{result}\n")

   




