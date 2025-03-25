import subprocess
import optparse
import re


def informations():
    """
    Prints the available network interfaces and their current MAC addresses.

    This function does not take any parameters and does not return any value.
    """
    
    print("\n[!] Info: Available Network Interfaces and their MAC addresses:\n")
    # For each Element (interface) in getInterfaces() list
    for interface in getInterfaces():
        # Get the current MAC address of this interface
        mac = getCurrentMac(interface)
        # Print the interface name and its MAC address
        print(f"\t[{getInterfaces().index(interface) + 1}] {interface} : {mac}")


def get_Arguments():
    """
    Get the command line options and arguments.

    Returns:
        options: The object containing the options and arguments.
    """
    
    # Create an OptionParser object
    parse = optparse.OptionParser()
    
    # Define "-i" and "--interface" option for specifying the network interface
    parse.add_option("-i", "--interface", dest="Network_Interface", help="Interface to change its MAC address")
    # Define "-m" and "--newMac" option for specifying the new MAC address
    parse.add_option("-m", "--mac", dest="New_Mac_Address", help="New MAC address")
    # Reads the command line arguments and options
    (options, arguments) = parse.parse_args()

    # Check if both options are specified
    if not options.Network_Interface and not options.New_Mac_Address:
        informations()
        print("\n[-] Error: Please specify an interface and a new MAC address, use --help for more info.")
        exit()
    # Check if only Network Interface is specified
    elif not options.Network_Interface:
        informations()
        print("\n[-] Error: Please specify an interface, use --help for more info.")
        exit()
    # Check if only New Mac Address is specified
    elif not options.New_Mac_Address:
        informations()
        print("\n[-] Error: Please specify a new MAC address, use --help for more info.")
        exit()

    # When calling this function, then options will be returned
    return options



def getCurrentMac(interface):
    """
    Get the current MAC address of the specified network interface.

    :param Network_Interface: The network interface to query.
    :return: The current MAC address as a string if found, or No MAC address found if not found.
    """
    
    try:
        # Execute the 'ifconfig' command to get details of the network interface
        ifconfigResult = subprocess.check_output(["ifconfig", interface], shell=False).decode("utf-8")
        
        # Use a regular expression to search for a MAC address pattern in the output
        mac = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfigResult)
        
        # If a MAC address is found, return it
        if mac:
            return mac.group(0)
        else:
            return "No MAC address found"
    except subprocess.CalledProcessError:
        # Return it if "try" block fails ('ifconfig' command fails) or interface not found
        return "Interface not found"

def getInterfaces():
    """
    Get a list of network interface names.

    Execute the 'ifconfig' command to retrieve network interface details, and
    then use a regular expression to find all interface names at the start of a
    line in the output. The list of interface names is then returned.

    :return: A list of network interface names.
    """

    # Execute the 'ifconfig' command to retrieve network interface details
    ifconfigResult = subprocess.check_output("ifconfig", shell=True).decode("utf-8")
    
    # Use a regular expression to find all interface names at the start of a line
    # "^" Check for the start of a line that starts with a word not spaces or tabs or etc....
    # "\w+" Check first word in the line
    # "MULTILINE" Makes "^" match the start of each line in the string not just the start of the string
    interfaces = re.findall(r'^\w+', ifconfigResult, re.MULTILINE)
    
    # Return the list of interface names
    return interfaces


def changeMac(Network_Interface, New_Mac_Address):
    """
    Change the MAC address of the specified network interface.

    :param New_Mac_Address: The new MAC address.
    :param Network_Interface: The network interface.
    """
    
    # Turn the network interface off
    subprocess.call(f"ifconfig {Network_Interface} down", shell=True)
    
    # Change the hardware address (MAC address) for the network interface with the new MAC address
    subprocess.call(f"ifconfig {Network_Interface} hw ether {New_Mac_Address}", shell=True)
    
    # Turn the network interface back on
    subprocess.call(f"ifconfig {Network_Interface} up", shell=True)
    
 

def validate_mac_address(mac_address):
    """
    Validate a MAC address.

    :param mac_address: The MAC address to validate.
    :return: True if the MAC address is valid, False otherwise.
    """
    if re.match(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", mac_address):
        return True
    return False
        
        
# Checks if this script is being run directly (not being imported) and if so, then the code under this line is executed.
if __name__ == "__main__":
    # Get command-line arguments and options
    options = get_Arguments()
    
    # Validate the format of the new MAC address
    if not validate_mac_address(options.New_Mac_Address):
        print("[-] Invalid MAC address format.")
        exit(1)  # Exit if the MAC address format is invalid

    # Change the MAC address of the specified network interface
    changeMac(options.Network_Interface, options.New_Mac_Address)

    # Retrieve the new MAC address to verify the change
    new_mac = getCurrentMac(options.Network_Interface)

    # Check if the MAC address was successfully changed
    if new_mac == options.New_Mac_Address:
        print(f"[+] MAC address of {options.Network_Interface} changed to: {options.New_Mac_Address}")
    else:
        print("[-] MAC address did not get changed.")