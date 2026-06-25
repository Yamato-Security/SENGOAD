<div align="center">
  <h1><img alt="SENGOAD (Sengoku Game Of Active Directory)" src="./docs/mkdocs/docs/img/logo_GOAD3.png"></h1>
  <br>
</div>

**SENGOAD** — a Sengoku-jidai reskin of GOAD (v3)

:bookmark: Documentation : [https://orange-cyberdefense.github.io/GOAD/](https://orange-cyberdefense.github.io/GOAD/)

## 🏯 SENGOAD — Sengoku Jidai reskin

SENGOAD re-skins the lab's *Game of Thrones* names to the Japanese **Sengoku Jidai** (Warring States) period — famous clans and warlords (Oda, Toyotomi, Takeda, Mōri, …) with **kanji display names**. See the full name correspondence:

- 🗾 [GOAD → SENGOAD mapping (English)](./docs/SENGOAD_mapping_EN.md)
- 🇯🇵 [GOAD → SENGOAD 対応表（日本語）](./docs/SENGOAD_mapping_JA.md)

## Description
SENGOAD is a Sengoku-jidai reskin of GOAD — a pentest Active Directory lab.
The purpose of this lab is to give pentesters a vulnerable Active directory environment ready to use to practice usual attack techniques.

> [!CAUTION]
> This lab is extremely vulnerable, do not reuse recipe to build your environment and do not deploy this environment on internet without isolation (this is a recommendation, use it as your own risk).<br>
> This repository was build for pentest practice.

![goad_screenshot](./docs/img/goad_screenshot.png)

## Licenses
This lab use free Windows VM only (180 days). After that delay enter a license on each server or rebuild all the lab (may be it's time for an update ;))

## Available labs

- GOAD Lab family and extensions overview
<div align="center">
<img alt="GOAD" width="800" src="./docs/img/diagram-GOADv3-full.png">
</div>

- [SENGOAD](https://orange-cyberdefense.github.io/GOAD/labs/GOAD/) : 5 vms, 2 forests, 3 domains (full SENGOAD lab)
<div align="center">
<img alt="GOAD" width="800" src="./docs/img/GOAD_schema.png">
</div>

- [SENGOAD-Light](https://orange-cyberdefense.github.io/GOAD/labs/GOAD-Light/) : 3 vms, 1 forest, 2 domains (smaller SENGOAD lab for those with a smaller pc)
<div align="center">
<img alt="GOAD Light" width="600" src="./docs/img/GOAD-Light_schema.png">
</div>

- [MINILAB](https://orange-cyberdefense.github.io/GOAD/labs/MINILAB/): 2 vms, 1 forest, 1 domain (basic lab with one DC (windows server 2019) and one Workstation (windows 10))

- [SCCM](https://orange-cyberdefense.github.io/GOAD/labs/SCCM/) : 4 vms, 1 forest, 1 domain, with microsoft configuration manager installed
<div align="center">
<img alt="SCCM" width="600" src="./docs/img/SCCMLAB_overview.png">
</div>

- [NHA](https://orange-cyberdefense.github.io/GOAD/labs/NHA/) : A challenge with 5 vms and 2 domains. no schema provided, you will have to find out how break it.
<div align="center">
<img alt="SCCM" width="600" src="./docs/img/logo_NHA.jpeg">
</div>

- [DRACARYS](https://orange-cyberdefense.github.io/GOAD/labs/DRACARYS/) : A challenge with 3 vms and 1 domains. no schema provided, you will have to find out how break it.
<div align="center">
<img alt="SCCM" width="600" src="./docs/img/dracarys_logo.png">
</div>