$flag = "/J7O8=.;4R0.Q<3&G@@;IJ:J@-6f".ToCharArray()

$r = "HKLM:\Software\Microsoft\Windows NT\CurrentVersion"
$v = (gpv -Path $r -Name "CurrentBuild").ToCharArray()
$w = [string](gpv -Path $r -Name "UBR")
$w = $w.ToCharArray()

$i = 0; foreach ($l in $flag)
    {
    $flag[$i] = [char]([byte]$l + (($v[$i % $v.Length]) + ($w[$i % $w.Length]))); $i += 1
    }

$flag = ([string]$flag) -replace ' ',''; Write-Output $flag