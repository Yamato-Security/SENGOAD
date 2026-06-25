# GOAD-Light

![GOAD Light overview](../../docs/img/GOAD-Light_schema.png)

This is a light version of goad without the aki (Mori) domain. This lab was build for computer with less performance.
Missing scenarios:
- cross forest exploitation (no more external forest)
- mssql trusted link
- some old computer vulnerabilities (zero logon, petitpotam unauthent,...)
- ESC4, ESC2/3

### Servers
This lab is actually composed of three virtual machines:
- **osaka** : DC01  running on Windows Server 2019 (with windefender enabled by default)
- **kofu**   : DC02  running on Windows Server 2019 (with windefender enabled by default)
- **shirakawa**  : SRV02 running on Windows Server 2019 (with windefender **disabled** by default)

#### domain : kai.yamato.local
- **kofu**     : DC01
- **shirakawa**    : SRV02 : MSSQL / IIS

#### domain : yamato.local
- **osaka**   : DC02


The lab setup is automated using vagrant and ansible automation tools.
You can change the vm version in the Vagrantfile according to Stefan Scherer vagrant repository : https://app.vagrantup.com/StefanScherer


### Users/Groups and associated vulnerabilites/scenarios

- You can find a lot of the available scenarios on [https://mayfly277.github.io/categories/ad/](https://mayfly277.github.io/categories/ad/)

KAI.YAMATO.LOCAL
- TAKEDA:              RDP on KOFU AND SHIRAKAWA
  - kikuhime:        Execute as user on mssql
  - takeda.shingen:      DOMAIN ADMIN KAI/ (bot 5min) LLMRN request to do NTLM relay with responder
  - sanjo:     
  - takeda.katsuyori:        bot (3min) RESPONDER LLMR
  - matsuhime:       
  - takeda.yoshinobu:     ASREP_ROASTING
  - takeda.nobukatsu:      
  - theon.greyjoy:
  - sanada.yukimura:          mssql admin / KERBEROASTING / group cross domain / mssql trusted link
  - benkei:             PASSWORD SPRAY (user=password)
- YOBAN:         RDP on SHIRAKAWA
  - yamamoto.kansuke:     Password in ldap description / mssql execute as login
                       GPO abuse (Edit Settings on "TAKEDAWALLPAPER" GPO)
  - sanada.yukimura:          (see takeda)
  - honda.tadakatsu:      (see honda)
- HONDA:             RDP on SHIRAKAWA
  - honda.tadakatsu:      ACL writedacl-writeowner on group Yoban
- UmiNoKanata :       cross forest group

YAMATO.LOCAL
- ODA
  - oda.nobunaga:   ACL forcechangepassword on oda.nobutada
  - oda.nobutada:   ACL genericwrite-on-user toyotomi.hideyori
  - oda.nobutaka:   ACL self-self-membership-on-group Gotairo
  - oichi:  DOMAIN ADMIN YAMATO
- TOYOTOMI:           RDP on OSAKA
  - toyotomi.hideyoshi:  DOMAIN ADMIN YAMATO
  - toyotomi.hideyori: ACL Write DACL on oda.nobutaka
  - toyotomi.hidenaga:
  - toyotomi.hidetsugu: ACL genericall-on-computer osaka / ACL writeproperty-self-membership Domain Admins
- GOTAIRO :      ACL add Member to group Ryujo / RDP on OSAKA
  - akechi.mitsuhide:    ACL writeproperty-on-group Domain Admins
  - hattori.hanzo:        ACL genericall-on-group Domain Admins / Acrossthenarrossea
  - sen.rikyu:   ACL write owner on group Domain Admins
- RYUJO :        ACL Write Owner on HATAMOTO
- HATAMOTO :         ACL generic all on user toyotomi.hidetsugu
- KaikyoNoKanata:       cross forest group


### Computers Users and group permissions

- YAMATO
  - DC01 : osaka.yamato.local (Windows Server 2019) (YAMATO DC)
    - Admins : toyotomi.hideyoshi (U), oichi (U)
    - RDP: Gotairo (G)

- KAI
  - DC02 : kofu.kai.yamato.local (Windows Server 2019) (KAI DC)
    - Admins : takeda.shingen (U), sanjo (U), takeda.katsuyori (U)
    - RDP: Takeda(G)

  - SRV02 : shirakawa.aki.local (Windows Server 2019) (IIS, MSSQL, SMB share)
    - Admins: honda.tadakatsu (U)
    - RDP: Yoban (G), Honda (G), Takeda (G)
    - IIS : allow asp upload, run as NT Authority/network
    - MSSQL:
      - admin : sanada.yukimura
      - impersonate : 
        - execute as login : samwel.tarlly -> sa
        - execute as user : kikuhime -> dbo
