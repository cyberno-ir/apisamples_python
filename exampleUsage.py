import os
import sys
import time
import CyUtils


# Clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def check_response_result(response):
    if response["success"] is False:
        print(CyUtils.CyUtils.get_error(response))
        sys.exit(0)
    clear_screen()


print("""
  ______ ____    ____ .______    _______ .______      .__   __.   ______   
 /      |\   \  /   / |   _  \  |   ____||   _  \     |  \ |  |  /  __  \  
|  ,----' \   \/   /  |  |_)  | |  |__   |  |_)  |    |   \|  | |  |  |  | 
|  |       \_    _/   |   _  <  |   __|  |      /     |  . `  | |  |  |  | 
|  `----.    |  |     |  |_)  | |  |____ |  |\  \----.|  |\   | |  `--'  | 
 \______|    |__|     |______/  |_______|| _| `._____||__| \__|  \______/  
""")
# Get user input
server_address = input("Please insert API server address [Default=https://multiscannerdemo.cyberno.ir/]: ")
if server_address == "":
    server_address = "https://multiscannerdemo.cyberno.ir/"
muutils = CyUtils.CyUtils(server_address)
username = input("Please insert identifier (email): ")
password = input("Please insert your password: ")

# Log in
login_response = muutils.call_with_json_input('user/login',
                                              {'email': username, 'password': password})
check_response_result(login_response)
apikey = login_response["data"]

index = input("Please select scan mode:\n1- Scan local folder\n2- Scan file\nEnter Number=")
if index == "1":
    # Initialize scan
    file_path = input("Please enter the paths of file to scan (with spaces): ").split()
    avs = input("Enter the name of the selected antivirus (with spaces): ").split()
    scan_response = muutils.call_with_json_input('scan/init', {'token': apikey, 'avs': avs, 'paths': file_path})
    check_response_result(login_response)
else:
    # Initialize scan
    file_path = input("Please enter the path of file to scan: ")
    avs = input("Enter the name of the selected antivirus (with spaces): ")

    # Get file hash
    file_hash = muutils.get_sha256(file_path)
    scan_response = muutils.call_with_form_input('scan/multiscanner/init',
                                                 {'token': apikey, 'avs': avs, 'file': file_hash},
                                                 'file', file_path)
check_response_result(scan_response)

guid = scan_response["guid"]
# Check Password  in Path Address
if scan_response["password_protected"]:
    for item in scan_response["password_protected"]:
        password = input(f"|Enter the Password file -> {item} |: ")
        scan_extract_response = muutils.call_with_json_input(f'scan/extract/{guid}',
                                                             {'token': apikey, 'path': item,
                                                              'password': password})

        if scan_extract_response["success"] is False:
            print(CyUtils.CyUtils.get_error(scan_extract_response))

print("=========  Start Scan ===========")
scan_start_response = muutils.call_with_json_input(f'scan/start/{guid}', {'token': apikey})
check_response_result(scan_start_response)
# Wait for scan results
if scan_response["success"] is True:
    is_finished = False
    while not is_finished:
        print("Waiting for result ...")
        scan_result_response = muutils.call_with_json_input(f'scan/result/{guid}', {'token': apikey})
        try:
            if scan_result_response["data"]["finished_at"]:
                is_finished = True
                print(scan_result_response["data"])
                time.sleep(2)
        except KeyError:
            continue
else:
    print(muutils.get_error(scan_response))
sys.exit(0)
