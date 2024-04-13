import subprocess
from colorama import Fore, Style

with open("chal.tex", "w") as tex_file:
    tex_file.write(rf"""
\documentclass{{article}}

%%%
% Redacted
%%%

\pagenumbering{{gobble}}
\lfoot{{ % Page number formatting 
    \hspace*{{\fill}} Page \arabic{{page}} % of \protect\pageref{{LastPage}}
    }}

\newif\iflong

%%%
% Redacted
%%%

\begin{{document}}
%%%
% Redacted
%%%
""")

    print("")
    print(Fore.RED + "Insert your message in a LaTeX syntax. (For example, \\texttt{b01ler up!})")
    print("")
    print(Fore.RED + "Hit Enter once you are done.")
    print(Style.RESET_ALL)
    
    input_value = input()

    print("")
    print(Fore.RED + "Compiling...")
    print(Fore.RED + "(This might take a while. Feel free to hit Enter multiple times if that'd reduce your anxiety lol.)")

    tex_file.write(rf"""

    Here is my response to your message. It should all be in text. I hope you can see it.

    You said:

    {input_value}

    My reply:

    %%%
    % Redacted
    %%%
\end{{document}}
""")

subprocess.run(["pdflatex", "chal.tex"], stdout=subprocess.DEVNULL)

print("")
print(Fore.RED + "This is what it looks like when the PDF file is converted to a txt file:")
print("")
print(Style.RESET_ALL)

# %%%
# % Redacted
# %%%

print(Fore.RED + "End of the file.")
print("")

print(Fore.RED + "Due to security reasons, we will not be giving you the PDF or log files. Sorry =(")
print("")
print(Style.RESET_ALL)
