Medium Shaym Malware Analysis Threat Intel

An employee has been compromised following a malicious email campaign. In order to allow him to resume his activities, we have entrusted you with analyzing the email.

    Find the 3 CVEs that the attacker is trying to exploit
    Find the name of the object containing the malicious payload
    Find the family name of this malware

Format: GCC{CVE-ID_CVE-ID_CVE-ID:object_name:malware_family}

Example of flag: GCC{CVE-2022-39998_CVE-2022-39999_CVE-2023-29999:Object.XYZ:Qakbot}

NOTES:

    Order of the CVEs is alphabetical
    Don't include null bytes (if you find ObjEct.XYZ\x00, put ObjEct.XYZ)
    The flag is case sensitive
    ZIP password: infected
