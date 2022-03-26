import os
import shutil

class FilesTools():

    @staticmethod
    def remove_from_dir(dir):

        try: 
            os.chdir(dir)
            shutil.rmtree(dir)
        except FileNotFoundError:
            print(f'Seems no data was loaded to {dir}')
        except:
            raise
