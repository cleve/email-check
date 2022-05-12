import configparser
import os


class Credentials:
    """Handle credentials to provide to the core process
    Read and write access to config file.
    """
    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        try:
            if os.path.isfile('data/config.ini'):
                self.config.read('data/config.ini')
            else:
                raise Exception('File not found')
        except:
            raise Exception('Could not open config file')
    
    def read_file(self, section: str, field: str = None):
        """Get a section o a field of a section

        Args:
            section (str): section name
            field (str, optional): field associated to a section. Defaults to None.

        Returns:
            Section or str: Section if is a valid section
        """
        section_response = self.config[section]
        if field is None:
            return section_response
        else:
            return section_response[field]
    
    def create_credentials(self) -> None:
        """Create credentiald provided by the user
        """
        check = False
        
        while not check:
            user = input('Enter username: ')
            password = input('Enter password: ')
            print(f'username: {user}, pass: {password}')
            sure = input("Confirm changes? (y/n)")
            check = True if sure == 'y' else False

        # Write changes
        self.config['CRED'] = {'user': user, 'pass': password}
        with open('data/config.ini', 'w') as f:
            self.config.write(f)

    def create_timestamp_check_point(self, t_stamp: float) -> None:
        """Create timestamp register
        """
        # Write changes
        self.config['APP'] = {'timestamp': t_stamp}
        with open('data/config.ini', 'w') as f:
            self.config.write(f)

        