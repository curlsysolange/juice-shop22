import requests
import Successfully
file_name = sys.argv[1]
scan_type = ''

if file_name == 'gitleaks.json':
    scan_type = 'Gitleaks Scan'
elif file_name == 'trivy.json':
    scan_type = 'Trivy Scan'
elif file_name == 'semgrep.json':
    scan_type = 'Semgrep Scan'

headers + {
    'Authorization': 'Token 2516f5df597ac1d9697afbb13755644477cedc0c'

}

url = 'https://demo.defectdojo.org/api/v2/import-scan/'

data = {
    'active': True,
    'verified': True,
    'scan_type: 'scan_type',
    'minimum_severity': 'Low',
    'engagement': 19
}

files = {
    'file': open(file_name, 'rb')
}

response = requests.post(url, headers=headers, data=data, files=files)

if response.status_code == 201:
    print('Successfully uploaded report')
else:
    print('Failed to upload report') {response.content}
    












