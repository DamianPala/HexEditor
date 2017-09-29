'''
@brief      Command Line Interface to editing Intel Hex files.

            Usage:
            -gb <hex filename> <address>            Get Byte value from specified address
            -sb <hex filename> <address> <value>    Set Byte value at specified addres
            -gs <hex filename> <address>            Get String from specified address
            -ss <hex filename> <address> <string>   Set String at specified addres 
        
@author     Damian Pala
@date       28.09.2017
'''

import os
import sys
from hex_editor import HexEditor

PATH_TO_SCRIPT = os.path.dirname(sys.argv[0])

EXIT_CODE_SUCCESS                  =  0
EXIT_CODE_SYNTAX_ERROR             = -1
EXIT_CODE_UNKNOWN_COMMAND          = -2
EXIT_CODE_FILE_NOT_EXISTS          = -3
EXIT_CODE_INVALID_PARAMETER        = -4
EXIT_CODE_UNKNOWN_ERROR            = -5

if __name__ == "__main__":
    hex_editor = HexEditor()
    
    """Set Byte"""
#     sys.argv.append("-sb")
#     sys.argv.append("SM_RF_PIC18.production.hex")
#     sys.argv.append("0x5FF0")
#     sys.argv.append("0x47")
    
    """Get Byte"""
#     sys.argv.append("-gb")
#     sys.argv.append("SM_RF_PIC18.production.hex")
#     sys.argv.append("0x5FF0")

    """Get String"""
#     sys.argv.append("-gs")
#     sys.argv.append("DR_203_Recorder.hex")
# #     sys.argv.append("0x0803FFE0")
#     sys.argv.append("0x0802BFE0")
    
    """Set String"""
#     sys.argv.append("-ss")
#     sys.argv.append("SM_RF_PIC18.production.hex")
#     sys.argv.append("0x5FF0")
#     sys.argv.append("Tiso")
    
#     sys.argv.append("--help")
    
    if len(sys.argv) == 2 and sys.argv[1] == "--help":
        print(
"""Intel Hex File Editor.
Usage:
    -gb <hex filename> <address>            Get Byte value from specified address
    -sb <hex filename> <address> <value>    Set Byte value at specified addres
    -gs <hex filename> <address>            Get String from specified address
    -ss <hex filename> <address> <string>   Set String at specified addres"""
            )
        sys.exit(EXIT_CODE_SUCCESS)   
    elif len(sys.argv) > 3 and len(sys.argv) < 6:
        if len(sys.argv) == 4: 
            command_action = sys.argv[1]
            hex_file_name = sys.argv[2]
            address = sys.argv[3]
        elif len(sys.argv) == 5: 
            command_action = sys.argv[1]
            hex_file_name = sys.argv[2]
            address = sys.argv[3]
            value = sys.argv[4]
    else:
        print("Syntax error")
        sys.exit(EXIT_CODE_SYNTAX_ERROR)
        
    if not os.path.isfile(os.path.join(PATH_TO_SCRIPT, hex_file_name)):
        sys.exit(EXIT_CODE_FILE_NOT_EXISTS)
        
    hex_editor.set_file_name(os.path.join(PATH_TO_SCRIPT, hex_file_name))
        
    try:
        if command_action == "-gb":
            print(str(hex_editor.get_byte(int(address, 16))))
            sys.exit(EXIT_CODE_SUCCESS)
        elif command_action == "-sb":
            hex_editor.set_byte(int(address, 16), int(value, 16))
            print("Byte set successfully")
            sys.exit(EXIT_CODE_SUCCESS)   
        elif command_action == "-gs":
            byte_addr = int(address, 16)
            byte_value = int(hex_editor.get_byte(byte_addr), 16)
            if byte_value != 0:
                str_out = ""
                cnt = 0
                while byte_value != 0 and cnt < 10000:
                    byte_addr += 1
                    str_out += chr(byte_value)
                    byte_value = int(hex_editor.get_byte(byte_addr), 16)
                    cnt += 1
                print(str(str_out))
            sys.exit(EXIT_CODE_SUCCESS)
        elif command_action == "-ss":
            if len(value) > 0:
                byte_cnt = 0
                byte_addr = int(address, 16)
                byte_value = ord(value[byte_cnt])
                while byte_cnt < len(value):
                    byte_value = ord(value[byte_cnt])
                    hex_editor.set_byte(byte_addr, byte_value)
                    byte_addr += 1
                    byte_cnt += 1
                hex_editor.set_byte(byte_addr, 0)
                print("String inserted successfully")
                sys.exit(EXIT_CODE_SUCCESS)
            else:
                sys.exit(EXIT_CODE_INVALID_PARAMETER)
        else:
            print("Unknown command.")
            sys.exit(EXIT_CODE_UNKNOWN_COMMAND)
    except Exception:
        print("Unknown Error")
        sys.exit(EXIT_CODE_UNKNOWN_ERROR)
