import requests
import json

# Replace these with your vROps details
vrops_host = 'https://ariaops.ntpro.local'
username = 'admin'
password = 'VMware1!'

# Endpoints
auth_url = f'{vrops_host}/suite-api/api/auth/token/acquire'
vm_search_url = f'{vrops_host}/suite-api/api/resources'
metrics_url_template = f'{vrops_host}/suite-api/api/resources/{{}}/stats'

# Authenticate and Get Token
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
payload = {'username': username, 'password': password}
response = requests.post(auth_url, headers=headers, data=json.dumps(payload), verify=False)
token = response.json().get('token')

if not token:
    raise Exception("Authentication failed")

# Update headers with the token
headers['Authorization'] = f'vRealizeOpsToken {token}'

# Function to get the ID of a VM by its name
def get_vm_id(vm_name):
    vm_url = f'{vrops_host}/suite-api/api/resources'
    response = requests.get(vm_url, headers=headers, verify=False)
    if response.status_code == 200:
        resources = response.json()['resourceList']
        for resource in resources:
            if resource['resourceKey']['name'] == vm_name:
                return resource['identifier']
    return None

# Function to get metrics for a VM by its ID
def get_vm_metrics(vm_id):
    metrics_url = f'{vrops_host}/suite-api/api/resources/{vm_id}/stats'
    response = requests.get(metrics_url, headers=headers, verify=False)
    if response.status_code == 200:
        return response.json()
    return None

# Main script execution
vm_id = get_vm_id('raspberry')
if vm_id:
    vm_metrics = get_vm_metrics(vm_id)
    if vm_metrics:
        print("Metrics for VM 'raspberry':")
        print(json.dumps(vm_metrics, indent=4))
    else:
        print("Failed to retrieve metrics for VM 'raspberry'")
else:
    print("VM 'raspberry' not found")
