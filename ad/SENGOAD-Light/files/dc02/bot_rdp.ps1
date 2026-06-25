# https://learn.microsoft.com/fr-fr/troubleshoot/windows-server/user-profiles-and-logon/turn-on-automatic-logon
if(-not(query session takeda.katsuyori /server:shirakawa)) {
  #kill process if exist
  Get-Process mstsc -IncludeUserName | Where {$_.UserName -eq "KAI\takeda.katsuyori"}|Stop-Process
  #run the command
  mstsc /v:shirakawa
}