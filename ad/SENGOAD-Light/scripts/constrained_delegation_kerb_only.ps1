# https://www.thehacker.recipes/ad/movement/kerberos/delegations/constrained#without-protocol-transition
Set-ADComputer -Identity "shirakawa$" -ServicePrincipalNames @{Add='HTTP/kofu.kai.yamato.local'}
Set-ADComputer -Identity "shirakawa$" -Add @{'msDS-AllowedToDelegateTo'=@('HTTP/kofu.kai.yamato.local','HTTP/kofu')}
# Set-ADComputer -Identity "shirakawa$" -Add @{'msDS-AllowedToDelegateTo'=@('CIFS/kofu.kai.yamato.local','CIFS/kofu')}