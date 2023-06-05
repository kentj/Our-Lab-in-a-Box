import os
import urllib.request
import ssl
from string import Template
import configparser

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
   print(f"Template: {template_URL}")
   print(f"File: {fileName}")
   try:
      template_data = getURLContent(template_URL).decode('utf-8')
      template = Template(template_data)
      completed_template_data = template.substitute(variables)
      writeFileContent(fileName, completed_template_data)
   except Exception as e:
      print(e)
      return False
   
   return True

def main():
   print("Lab-in-a-Box Setup and Configuration Tool v0.1")
   print("----------------------------------------------\n")

   config = configparser.ConfigParser()
   try:
      config.read('lab_config.ini')
   except:
      print("Couldn't read the config.ini. Aborting.")
      exit()

   labAbbreviation = config.get('LabInfo', 'labAbbreviation', fallback = '')
   if labAbbreviation == '':
      print("Lab abbreviation MUST be specified in config.ini.  Aborting.")
      exit()

   fqdnEnding = config.get('LabInfo', 'fqdnEnding')
   wanIP = config.get('LabInfo', 'wanIP')
   vendorNetIP = config.get('LabInfo', 'vendorNetIP')
   internalLANetwork = config.get('LabInfo', 'internalLANetwork')
   remoteVMIP = config.get('LabInfo', 'remoteVMIP')
   minioVMIP = config.get('LabInfo', 'minioVMIP')
   labPassword = config.get('LabInfo', 'labPassword')
   baseDirectory = config.get('LabInfo', 'labPath', 
                     fallback='/home/administrator')
   baseTemplateURL = config.get('LabInfo', 'templateURL',
                     fallback="https://raw.githubusercontent.com/kentj/Our-Lab-in-a-Box/main/templates/")
   
   #make sure the baseDirectory for these files ends in a foreward slash
   if baseDirectory[-1] != '/':
      baseDirectory = baseDirectory + "/"

   print("Summary of your inputs and calculated values: ")
   print(f"01: Lab Abbreviation: {labAbbreviation}")

   labName = labAbbreviation + "-lab"
   labNameUpper = labName.upper()
   labNameUnderscored = (labAbbreviation + "_lab")
   labNameUnderscoredUpper = (labAbbreviation + "_lab").upper()
   print(f"02: Lab Name: {labName}")
   print(f"03: Lab Name UnderScore Uppercase: {labNameUnderscoredUpper}")
   print(f"04: Lab password: {labPassword}")
   print(f"05: Lab FQDN ending: {fqdnEnding}")
   rootCADirectory = labAbbreviation.upper() + "-Lab-CA"
   rootCA_certificate_file = rootCADirectory + '.crt'
   rootCA_certificate_key_file = rootCADirectory + ".key"
   rootCA_certificate_pem_file = rootCADirectory + ".pem"

   print(f"06: Lab Root Certificate Authority Directory: {rootCADirectory}")
   print(f"06a. Lab Root CA Certificate File: {rootCA_certificate_file}")
   print(f"06b. Lab Root CA Certificate Key File: {rootCA_certificate_key_file}")
   print(f"06c. Lab Root CA Certficiate PEM File: {rootCA_certificate_pem_file}")

   lab_base_URL = f"{labName}.nccoe.{fqdnEnding}"
   print(f"07. Lab Base URL: {lab_base_URL}")

   certificate_file_suffix = lab_base_URL + ".crt"
   certificate_key_file_suffix = lab_base_URL + ".key"

   guacamole_certificate_file = 'guacamole.' + certificate_file_suffix
   guacamole_certificate_key_file = 'guacamole.' + certificate_key_file_suffix
   print(f"08a. Guacamole Certificate File: {guacamole_certificate_file}")
   print(f"08b. Guacamole Certificate Key File: {guacamole_certificate_key_file}")

   keycloak_certificate_file = 'keycloak.' + certificate_file_suffix
   keycloak_certificate_key_file = 'keycloak.' + certificate_key_file_suffix
   print(f"09a. Keycloak Certificate File: {keycloak_certificate_file}")
   print(f"09b. Keycloak Certificate Key File: {keycloak_certificate_key_file}")

   minio_certificate_file = 'minio.' + certificate_file_suffix
   minio_certificate_key_file = 'minio.' + certificate_key_file_suffix
   print(f"10a. MinIO Certificate File: {minio_certificate_file}")
   print(f"10b. MinIO Certificate Key File: {minio_certificate_key_file}")

   remote_certificate_file = 'remote.' + certificate_file_suffix
   remote_certificate_key_file = 'remote.' + certificate_key_file_suffix
   print(f"11a. Remote Certificate File: {remote_certificate_file}")
   print(f"11b. Remote Certificate Key File: {remote_certificate_key_file}")

   print("\nMaking system changes...\n")
   print("Step 1:  Creating directories...")

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
      directory = baseDirectory + x
      print(f'.... Creating directory{directory}')
      try:
         os.makedirs(directory)
      except FileExistsError:
         print(f"Directory exists, skipping: {directory} ")

   print("\nStep 2:  Creating files from templates...\n")

   templateSuffix = '.template'
   baseLocation = baseDirectory + "guacamole/"

   for x in [ ['Caddyfile', 'caddy/Caddyfile'],
            ['Dockerfile', 'guacamole_build/Dockerfile'],
            ['env', '.env'],
            ['caddy_reload.sh', 'caddy_reload.sh'],
            ['docker-compose.yaml', 'docker-compose.yaml'] ]:
      print(f".... Rendering template {x[0]}.template to file {x[1]}")
      templateURL = baseTemplateURL + x[0] + templateSuffix
      fileName = baseLocation + x[1]
      result = transformTemplate(locals(), templateURL, fileName)
      if result == True:
         print(f"Completion of template for {x[0]} sucessful!\n")
      else:
         print(f"Failed...\n{result}\n")

      
if __name__ == '__main__':
   main()




