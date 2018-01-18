This example Python Script "K5 Project List Generator.py" can be used to create a text file called "projectlist.txt", that includes a list of project IDs for your K5 contact. This script will authenticate you against the global region, obtain a list of all regions, then for each region obtain a token and write the project ids to a file, one per line:

Before using the script, please edit it and update the Contract Parameters with your user credentials. Note: Ensure the account you use is a member of the DomainManager group.

Project IDs are written to the file as shown in the below example snippet:

*** The following project(s) belong to the jp-east-1 region***
fsgt32fdghf32a192c3113542b404963
5b62a2f140ad415c55954a2aa2539dfa
94a839104552401fbc96ba521f0d12d6
15c55954a3f9f837457a31ff5eaas321
e0ea6b14494542459fbe2f8fdd46ebc2
*** The following project(s) belong to the uk-1 region***
