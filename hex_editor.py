'''
@brief      Module to editing and readiing Intel Hex files.
        
@author     Damian Pala
@date       29.03.2017
'''

from enum import Enum

class HexEditor:
    EXTENDED_SEGMENT_OFFSET     = 0x10
    EXTENDED_LINEAR_OFFSET      = 0x10000
    hex_file                    = ""
    hex_file_name               = ""
    
    class DataType(Enum):
        DATA                        = 0
        EOF                         = 1
        EXTENDED_SEGMENT_ADDRESS    = 2
        START_SEGMENT_ADDRESS       = 3
        EXTENDED_LINEAR_ADDRESS     = 4
        START_LINEAR_ADDRESS        = 5
    
    
    def set_file_name(self, file_name):
        self.hex_file_name = file_name
    
    
    def get_hex_file(self):
        self.hex_file = open(self.hex_file_name, 'r')
        
        
    def get_byte(self, address):
        self.get_hex_file()
        line_number, line_with_byte, byte_pos = self.get_line_with_byte(address)
        
        if self.get_byte_count(line_with_byte) - 1 >= byte_pos:
            return self.get_data_ret_str(line_with_byte)[byte_pos * 2:byte_pos * 2 + 2]
        else:
            return "Address out of range"


    def set_byte(self, address, value):
        self.get_hex_file()
        line_number, line_with_byte, byte_pos = self.get_line_with_byte(address)
        
        if self.get_byte_count(line_with_byte) - 1 >= byte_pos:
            data_to_change = self.get_data_ret_str(line_with_byte)
            
            new_data = data_to_change[:byte_pos * 2] + hex(value)[2:].upper() + data_to_change[byte_pos * 2 + 2:]
            
            modified_record = line_with_byte[:9] + new_data
            modified_record += self.calc_checksum(modified_record)[2:].upper()
            
#             print line_with_byte
            
            self.change_file(line_number, modified_record)
            return modified_record
        else:
            return "Address out of range"
        
        
    def change_file(self, line_number, new_record):
        f = open(self.hex_file_name, 'r')
        data = f.readlines()
        data[line_number] = new_record + '\n'
        
        f = open(self.hex_file_name, 'w')
        f.writelines(data)
    
    
    def get_line_with_byte(self, address):
        segment_address = 0
        record_address = 0
        line_with_byte = "";
        line_number = 0
        segment_address_with_byte = 0
        
        for i, hex_line in enumerate(self.hex_file):
            if self.get_data_type(hex_line) == self.DataType.EXTENDED_SEGMENT_ADDRESS:
                segment_address = self.get_data_ret_int(hex_line) * self.EXTENDED_SEGMENT_OFFSET
                
            if self.get_data_type(hex_line) == self.DataType.EXTENDED_LINEAR_ADDRESS:
                segment_address = self.get_data_ret_int(hex_line) * self.EXTENDED_LINEAR_OFFSET
            
            if self.get_data_type(hex_line) == self.DataType.DATA:            
                record_address = segment_address + self.get_address(hex_line)
            
                if (record_address > address):
                    break
                else:
                    line_with_byte = hex_line
                    line_number = i
                    segment_address_with_byte = segment_address
        
        record_address = segment_address_with_byte + self.get_address(line_with_byte)
        
        byte_pos = address - record_address
        
        return line_number, line_with_byte, byte_pos
        
        
    def get_byte_count(self, hex_line):
        return int(hex_line[1:3], 16)
        
        
    def get_address(self, hex_line):
        return int(hex_line[3:7], 16)
       
        
    def get_data_type(self, hex_line):
        raw_data_type = int(hex_line[7:9], 16)
        
        if raw_data_type == self.DataType.DATA.value:
            return self.DataType.DATA     
        elif raw_data_type == self.DataType.EOF.value:
            return self.DataType.EOF
        elif raw_data_type == self.DataType.EXTENDED_SEGMENT_ADDRESS.value:
            return self.DataType.EXTENDED_SEGMENT_ADDRESS
        elif raw_data_type == self.DataType.START_SEGMENT_ADDRESS.value:
            return self.DataType.START_SEGMENT_ADDRESS
        elif raw_data_type == self.DataType.EXTENDED_LINEAR_ADDRESS.value:
            return self.DataType.EXTENDED_LINEAR_ADDRESS
        elif raw_data_type == self.DataType.START_LINEAR_ADDRESS.value:
            return self.DataType.START_LINEAR_ADDRESS
        
        
    def get_data_ret_int(self, hex_line):
        n_bytes = self.get_byte_count(hex_line)
        return int(hex_line[9:9 + 2 * n_bytes], 16)
    
    
    def get_data_ret_str(self, hex_line):
        n_bytes = self.get_byte_count(hex_line)
        return hex_line[9:9 + 2 * n_bytes]
    
    
    def get_checksum(self, hex_line):
        return int(hex_line[-2:], 16)
    
    
    def calc_checksum(self, hex_line):
        bytes_to_checksum = []
        
        byte_count = self.get_byte_count(hex_line)
        
        bytes_to_checksum.append(int(hex_line[1:3], 16))
        bytes_to_checksum.append(int(hex_line[3:5], 16))
        bytes_to_checksum.append(int(hex_line[5:7], 16))
        bytes_to_checksum.append(int(hex_line[7:9], 16))
        
        for i in range(0, byte_count):
            bytes_to_checksum.append(int(hex_line[9 + i * 2:11 + i * 2], 16))
            
        return hex(0x100 - (sum(bytes_to_checksum) & 0xff))
