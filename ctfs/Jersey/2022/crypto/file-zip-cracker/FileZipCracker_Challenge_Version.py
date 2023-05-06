import zipfile
import itertools
from itertools import permutations


# Function for extracting zip files to test if the password works!
def extractFile(zip_file, password):
    try:
        zip_file.extractall(pwd=password.encode())
        return True
    except KeyboardInterrupt:
        exit(0)
    except Exception as e:
        pass

# Main code starts here...
# The file name of the zip file.
zipfilename = 'secret_folder.zip'




numbers_set = '1235'

zip_file = zipfile.ZipFile(zipfilename)


for c in itertools.product(numbers_set, repeat=4):
    # Add the four numbers to the first half of the password.

        password = "Actor_Name"+''.join(c)
        # Try to extract the file.
        print("Trying: %s" % password)
        # If the file was extracted, you found the right password.
        if extractFile(zip_file, password):
            print('*' * 20)
            print('Password found: %s' % password)
            print('Files extracted...')
            exit(0)

# If no password was found by the end, let us know!
print('Password not found.')
