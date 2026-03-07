# PROJECT MIRRORFALL: The Exquisite Dilemma of Offence vs Defence

## Objective 1: Repository Forensics & Metadata Extraction

Your first task is to locate a public archive serving as an archival mirror for the 2013 intelligence disclosures.

Within this archive, locate the raw PDF classification guide dated on September 5, 2013 that corresponds to the overarching US encryption defeat program.

- Variable X: extract the first 7 characters of the latest commit SHA for this exact PDF file. Do not use the repository's main commit hash.

## Objective 2: Document Parsing & ECI Isolation

Download the raw PDF classification guide. Navigate through the dense administrative caveats to Appendix A, which lists the program's specific capabilities.

- Locate the "Remarks" column corresponding to the list of Exceptionally Controlled Information (ECI) compartments used to protect these details.
- The first ECI listed is APERIODIC. Identify the second ECI compartment listed immediately after it (an 8-letter codeword).
- Normalize this codeword.

## Objective 3: The Deterministic AI Scripting Layer

Process the extracted ECI codeword through a specific semantic embedding model.

Initialize all-MiniLM-L6-v2 model.

- Pass the normalized, 8-letter ECI codeword into the model to generate its tensor embedding array (model.encode()).
- Variable Y: Extract the first floating-point value from the resulting embedding array (Index 0) and round it to 4 decimal places.