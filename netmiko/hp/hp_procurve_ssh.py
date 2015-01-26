from netmiko.ssh_connection import SSHConnection
from netmiko.netmiko_globals import MAX_BUFFER

import time

class HPProcurveSSH(SSHConnection):

    def session_preparation(self):
        '''
        Prepare the session after the connection has been established
        '''

        # HP uses - 'Press any key to continue'
        time.sleep(1)
        self.remote_conn.send("\n")
        time.sleep(1)

        # HP output contains VT100 escape codes
        self.ansi_escape_codes = True

        self.disable_paging(command="\nno page\n")
        self.find_prompt()

    def config_mode(self):
        '''
        Exit config mode
        '''
        output = self.send_command('config terminal\n')

        if self.check_config_mode():
            self.clear_buffer()
            return False
        else:
            self.clear_buffer()
            return True

    def exit_config_mode(self):
        '''
        Exit config mode
        '''
        output = self.send_command('end\n')

        if self.check_config_mode():
            self.clear_buffer()
            return False
        else:
            self.clear_buffer()
            return True

    def enable_mode(self):
        '''
        Enter enable mode
        '''
        output = self.send_command('enable\n')
        if 'sername' in output:
            output += self.send_command('manager')
        if 'assword' in output:
            output += self.send_command(self.secret)

        if self.check_enable_mode():
            self.clear_buffer()
            return True
        else:
            self.clear_buffer()
            return False

        return None
    
    def exit_enable_mode(self):
        '''
        Exit enable mode
        '''
        output = self.send_command('exit\n')

        if self.check_enable_mode():
            self.clear_buffer()
            return False
        else:
            self.clear_buffer()
            return True
    
    def check_enable_mode(self):
        '''
        Finds the HP Procurve prompt and checks if the prompt contains the right enable mode characters '#'
        
        '''
        
        self.find_prompt()
        if self.router_prompt[-1] == '#':
            return True
        else:
            return False
        
    def check_config_mode(self):
        '''
        Finds the HP Procurve prompt and checks if the prompt contains the right config mode characters '(config)#'
        
        '''
        
        self.find_prompt()
        if self.router_prompt[-9:] == '(config)#':
            return True
        else:
            return False
    