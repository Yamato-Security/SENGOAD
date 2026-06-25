Set-ADComputer -Identity "mizuchi$" -ServicePrincipalNames @{Add='WSMAN/mizuchi.ryuen.lab'}
Set-ADComputer -Identity "mizuchi$" -Add @{'msDS-AllowedToDelegateTo'=@('WSMAN/mizuchi.ryuen.lab')}
