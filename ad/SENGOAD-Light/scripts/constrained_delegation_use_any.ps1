# https://www.thehacker.recipes/ad/movement/kerberos/delegations/constrained#with-protocol-transition
Set-ADUser -Identity "sanada.yukimura" -ServicePrincipalNames @{Add='CIFS/kofu.kai.yamato.local'}
Get-ADUser -Identity "sanada.yukimura" | Set-ADAccountControl -TrustedToAuthForDelegation $true
Set-ADUser -Identity "sanada.yukimura" -Add @{'msDS-AllowedToDelegateTo'=@('CIFS/kofu.kai.yamato.local','CIFS/kofu')}