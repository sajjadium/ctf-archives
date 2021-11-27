You just popped a machine on your engagement and are spawned inside a powershell session. But wait! It got no scripting support and a very wierd environment. Are you just-enough-attacker to read the flag?

The following need to be run as admin:

winrm quickconfig

Set-Item WSMan:localhost\client\trustedhosts -value powerhell.rumble.host

$cred = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList ("powerhell", (ConvertTo-SecureString -String "CSR2021!@" -AsPlainText -Force))

Enter-PSSession -ComputerName powerhell.rumble.host -Credential $cred -Authentication Negotiate

After the challenge please make sure to stop the service Windows Remote Management (winrm) and set the start mode to manual (unless you know that you actually need WinRM).

Linux Users: You can use PowerShell Remoting from Linux.

docker run --rm=false --name=hell -d mcr.microsoft.com/powershell /bin/sleep inf

docker exec -t -i hell pwsh -c 'Install-Module -Name PSWSMan'

docker exec -t -i hell pwsh -c 'Install-WSMan'

docker exec -t -i hell pwsh

$cred = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList ("powerhell", (ConvertTo-SecureString -String "CSR2021!@" -AsPlainText -Force))

Enter-PSSession -ComputerName powerhell.rumble.host -Credential $cred -Authentication Negotiate
