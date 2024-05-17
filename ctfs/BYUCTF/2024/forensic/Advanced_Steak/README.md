The Mad Cow APT has been responsible for a significant amount of attacks against organizations in the technology, finance, and energy domains. They first started their attacks around 3 years ago, though they have been dormant in the last 2 years. Recently, the APT started to resurface.

Field agents were able to conduct a raid against a known Mad Cow hideout. In the process, the agents pulled a flash drive from one of the Mad Cow computers. Unfortunately, it looks like one of the threat actors was able to begin wiping the flash drive with random data before the analyst pulled the drive. The field agent pulled the drive before the wipe was complete, but parts of the drive have been corrupted. Our team has already created a forensic image of the drive: Mad Cow.001.

Analysts who studied the Mad Cow APT two years ago are highly confident that the APT is utilizing the same tactics as they have in previous years. One such tactic is communicating through a custom file type. Fortunately, one of analysts built a decryptor for this custom file type. Using this, we can turn any .cow files into a standard PNG. The decryptor does not offer any useful information on finding these files, however.

Your job is to find any .cow files on the corrupted flash drive (Mad Cow.001) and pull them from the image file. You can use the two provided .cow files as reference to help understand what the files look like. Then, run any discovered .cow file(s) through the decryptor to determine if there is any useful data. The data will be in the format byuctf{flag}.

Note: this is not a reverse engineering challenge. The cow_decryptor.py is intentionally missing important data. You do not need to reverse engineer the script in order to find the file(s). This challenge can be solved without examining the cow_decryptor.py file.

Author: FiredPeppers
