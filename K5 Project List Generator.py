# Author : Ian Purvis
# Date:    12/01/18
#
# Purpose: Script to obtain list of projects for each region within a contract

import requests
import json
import sys

# Define contract parameters
adminUser = '<USERNAME>'
adminPassword = '<PASSWORD>'
contract = '<CONTRACTID>'


def get_globally_unscoped_token(adminUser, adminPassword, contract):
    """Get a global auth token that is not scoped to any project
    Returns:
        Python Object: Globally Unscoped Token Object
    Args:
        adminUser (string): Administrative user name
        adminPassword (string): Password for above user
        contract (string): Contract name

    """
    #URL for global Identity service
    identityURL = 'https://identity.gls.cloud.global.fujitsu.com/v3/auth/tokens'
    print "*** Obtaining Unscoped token for the global region"
    try:
        response = requests.post(identityURL,
                                     headers={'Content-Type': 'application/json',
                                              'Accept': 'application/json'},
                                     json={"auth":
                                             {"identity":
                                              {"methods": ["password"], "password":
                                               {"user":
                                               {"domain":
                                                   {"name": contract},
                                                "name": adminUser,
                                                "password": adminPassword
                                                }}}}})
        #set token variable to equal the value of the returned header X-Subject-Token which contains the recently obtained token
        token  = response.headers['X-Subject-Token']
    
        return token
    except:
        return "*** Global Token Error for gls region "

def get_regionally_unscoped_token(adminUser, adminPassword, contract, region):
    """Get a regional auth token that is not scoped to any project
    Returns:
        A Python Dictionary Object: Containing key:token containing the token value and key:user containing the ID of the user whose credentials were supplied
    Args:
        adminUser (string): Administrative user name
        adminPassword (string): Password for above user
        contract (string): Contract name
        region (string): region code
    """
    #constructs the regional identity url, based on the region supplied to the function
    identityURL = 'https://identity.'+region+'.cloud.global.fujitsu.com/v3/auth/tokens'

    print "*** Obtaining Unscoped token for the " + str(region) + " Region"
    # Creating empty dictionary to be used for response
    dicresponse = {}
    try:
        response = requests.post(identityURL,
                                     headers={'Content-Type': 'application/json',
                                              'Accept': 'application/json'},
                                     json={"auth":
                                             {"identity":
                                              {"methods": ["password"], "password":
                                               {"user":
                                               {"domain":
                                                   {"name": contract},
                                                "name": adminUser,
                                                "password": adminPassword
                                                }}}}})
        #set token variable to equal the value of the returned header X-Subject-Token which contains the recently obtained token
        token  = response.headers['X-Subject-Token']
        #set userid variable to equal the ID of the user that is returned in the body of the response to the authentication request
        userid = response.json()["token"]["user"]["id"]

        #constructed the dictonary object to be returned
        dicresponse = {"token":token,"userid":userid}
        
    
        return dicresponse
    except:
        return "*** Unable to obtain a token for the " + str(region) + " Region. This probably means the Region has not yet been enabled within this contract"

def get_regions(k5token):
    """Function to obtain and return a list of the K5 regions
    Returns:
        A Python List Object: Containing all current K5 regions
    Args:
        k5token (string): Global unscoped token 
    """

    #URL for global contract service
    regionsURL = 'https://contract.gls.cloud.global.fujitsu.com/v1/regions'

    #creating empty list 
    regionlist = []
    print "*** Obtaining the current list of K5 regions"
    try:
        response = requests.get(regionsURL,headers={'X-Auth-Token': k5token,'Content-Type': 'application/json','Accept': 'application/json'})
        #Process the return JSON body response
        regions = response.json()["regions"]
        #For each region found
        for item in regions :
            #Store the ID value
            regionid = item.get("id")
            regionlist.append(regionid)
            #then add it to the regional list object
            print "****** Found " + str(regionid) + " Region"
        return regionlist
    except:
        return "*** Error obtaining Region List."

def create_regional_project_list(region, k5token, userid):
    """Writes the list of obtained projects for a particular user to a file 
    Returns:
        Success flag. This function writes to an file the list of obtained projects for a particular region/user
    Args:
        region (string): region code
        k5token (string): auth token for the region
        userid (string): id of the user to obtain the list of projects from
        
    """
    #constructs the regional project url, based on the region and user id supplied to the function
    projectURL = 'https://identity.' + region + '.cloud.global.fujitsu.com/v3/users/' + userid + '/projects'
    try:
        response = requests.get(projectURL,headers={'X-Auth-Token': k5token,'Content-Type': 'application/json','Accept': 'application/json'})
        #opens a file for appending to
        file = open("projectlist.txt",'a')
        #writes a line to indicated the region the 
        file.write("*** The following project(s) belong to the "+region+" region***\n")
        #process the returned json response
        projects = response.json()["projects"]
        #for each project found
        for item in projects :
            #obtain the project id only
            test = item.get("id")
            #then write it to the opened file
            file.write(test+"\n")
        print "****** Writing project list to file for region " + str(region)
        return "Success"
    except:
        return "*** Error writing the project list to the file"


#Main Section of Code
    
#initialse a new empty file for writing to
file = open("projectlist.txt","w")

# Get a global unscoped token 
k5auth = get_globally_unscoped_token(adminUser,adminPassword,contract)
if "Global Token Error" in k5auth :
    print k5auth
else:
    token = k5auth
    print "*** Your Global Security Token is : " + str(token)

#obtain list of regions
regionlist = get_regions(token)

#for each region in the list, including regions that have not been enabled within the contract do the follwoing
for region in regionlist :
    # Get an unscoped regional token
    k5auth = get_regionally_unscoped_token(adminUser,adminPassword,contract,region)
    if "Region has not yet been enabled" in k5auth :
        print k5auth
    else:
        token = k5auth.get("token")
        print "****** Your Regional Security Token for region " + str(region) + " is : " + str(token)
        userid = k5auth.get("userid")
        print "****** Your Current User ID is : " + str(userid)
        #obtain and write project list to file
        result = create_regional_project_list(region,token,userid)

