# SENGOAD — GOAD → Sengoku Jidai Name Mapping (English)

SENGOAD re-skins the GOAD lab family from its *Game of Thrones* naming to the
Japanese **Sengoku Jidai** (Warring States period, ~1467–1615). The guiding
principle is **recognizability**: the most famous clans and warlords are used,
rather than strict parallels to the original lore. Ninja (忍び) cover the
spy / intrigue elements.

This document is the name correspondence between the original GOAD names and
the SENGOAD names. It covers the **GOAD / GOAD-Light / GOAD-Mini** labs (which
share one name set) and the separate **DRACARYS** lab.

> A Japanese version of this document is available at
> [SENGOAD_mapping_JA.md](./SENGOAD_mapping_JA.md).

## Conventions

- **Logins / `sAMAccountName` stay ASCII** (e.g. `takeda.shingen`) so attack
  tooling keeps working; the **AD DisplayName is kanji** (e.g. `武田信玄`).
  This is wired via `win_domain_user`'s `attributes.displayName` in the
  `ad` / `onlyusers` roles, fed by a `displayname` field in `config.json`.
- Logins use Japanese order: **`surname.firstname`**.
- **Women take a single period name with no clan surname** (e.g. `お市の方`,
  `松姫`), matching how Sengoku-era women were actually known. Their clan tie is
  carried by AD group membership, not by the name.
- Passwords, SPNs, ACLs, gMSA, MSSQL linked servers and the vulnerable configs
  (autologon / cached credentials) are all kept in sync with these names.

## Clans (who's-who)

| Sengoku clan / figure | Kanji | Note | (was) GoT house |
|---|---|---|---|
| Oda Nobunaga | 織田信長 | the great unifier | Lannister |
| Toyotomi Hideyoshi | 豊臣秀吉 | the risen "Taikō" ruler | Baratheon (the throne) |
| Takeda Shingen | 武田信玄 | the "Tiger of Kai" | Stark (the North) |
| Mōri Motonari | 毛利元就 | the "Three Arrows" lord | Targaryen (Essos) |
| Date Masamune | 伊達政宗 | the "One-Eyed Dragon" | Khal Drogo |
| Sanada Yukimura | 真田幸村 | the fan-favourite hero | Jon Snow |
| Yamamoto Kansuke | 山本勘助 | Takeda's one-eyed strategist | Samwell Tarly |
| Hattori Hanzō | 服部半蔵 | the legendary ninja | Varys |
| Akechi Mitsuhide | 明智光秀 | the famous betrayer | Petyr Baelish |
| Sen no Rikyū | 千利休 | the great tea master | Maester Pycelle |
| Honda Tadakatsu | 本多忠勝 | peerless warrior | Mormont |

## Forest / Domains

| GoT domain | SENGOAD domain | NetBIOS |
|---|---|---|
| `sevenkingdoms.local` | `yamato.local` (大和) | `YAMATO` |
| `north.sevenkingdoms.local` | `kai.yamato.local` (甲斐) | `KAI` |
| `essos.local` | `aki.local` (安芸) | `AKI` |

Yamato = the central realm (Oda & Toyotomi). Kai = Takeda Shingen's province
(the North), a child of Yamato. Aki = Mōri Motonari's Inland-Sea realm (Essos).

## Computers (castles)

| GoT host | SENGOAD host | Castle |
|---|---|---|
| `kingslanding` | `osaka` | Osaka castle (Hideyoshi's seat) |
| `winterfell` | `kofu` | Kōfu (Takeda's seat in Kai) |
| `castelblack` | `shirakawa` | Shirakawa barrier (the great northern gate) |
| `meereen` | `hiroshima` | Hiroshima castle (built by the Mōri) |
| `braavos` | `sakai` | Sakai (the free merchant city) |

## Users

### Yamato (was sevenkingdoms) — Oda & Toyotomi

| GoT login | SENGOAD login | Display name |
|---|---|---|
| `tywin.lannister` | `oda.nobunaga` | 織田信長 |
| `jaime.lannister` | `oda.nobutada` | 織田信忠 |
| `cersei.lannister` | `oichi` | お市の方 |
| `tyron.lannister` | `oda.nobutaka` | 織田信孝 |
| `robert.baratheon` | `toyotomi.hideyoshi` | 豊臣秀吉 |
| `joffrey.baratheon` | `toyotomi.hideyori` | 豊臣秀頼 |
| `renly.baratheon` | `toyotomi.hidenaga` | 豊臣秀長 |
| `stannis.baratheon` | `toyotomi.hidetsugu` | 豊臣秀次 |
| `petyer.baelish` | `akechi.mitsuhide` | 明智光秀 |
| `lord.varys` | `hattori.hanzo` | 服部半蔵 |
| `maester.pycelle` | `sen.rikyu` | 千利休 |

### Kai (was north) — Takeda

| GoT login | SENGOAD login | Display name |
|---|---|---|
| `eddard.stark` | `takeda.shingen` | 武田信玄 |
| `catelyn.stark` | `sanjo` | 三条の方 |
| `robb.stark` | `takeda.katsuyori` | 武田勝頼 |
| `sansa.stark` | `matsuhime` | 松姫 |
| `arya.stark` | `kikuhime` | 菊姫 |
| `brandon.stark` | `takeda.yoshinobu` | 武田義信 |
| `rickon.stark` | `takeda.nobukatsu` | 武田信勝 |
| `hodor` | `benkei` | 弁慶 |
| `jon.snow` | `sanada.yukimura` | 真田幸村 |
| `samwell.tarly` | `yamamoto.kansuke` | 山本勘助 |
| `jeor.mormont` | `honda.tadakatsu` | 本多忠勝 |

### Aki (was essos) — Mōri

| GoT login | SENGOAD login | Display name |
|---|---|---|
| `daenerys.targaryen` | `mori.motonari` | 毛利元就 |
| `viserys.targaryen` | `mori.terumoto` | 毛利輝元 |
| `khal.drogo` | `date.masamune` | 伊達政宗 |
| `jorah.mormont` | `honda.tadatomo` | 本多忠朝 |
| `missandei` | `chiyo` | 千代 |
| `drogon` | `orochi` | オロチ |
| `sql_svc` | `sql_svc` | *(unchanged — service account)* |

## Groups

| Realm | GoT group | SENGOAD group | Kanji |
|---|---|---|---|
| Yamato | Lannister | Oda | 織田 |
| Yamato | Baratheon | Toyotomi | 豊臣 |
| Yamato | Small Council | Gotairo | 五大老 |
| Yamato | DragonStone | Ryujo | 竜城 |
| Yamato | KingsGuard | Hatamoto | 旗本 |
| Yamato | DragonRider | Ryuki | 竜騎 |
| Yamato | AcrossTheNarrowSea | KaikyoNoKanata | 海峡の彼方 |
| Kai | Stark | Takeda | 武田 |
| Kai | Night Watch | Yoban | 夜番 |
| Kai | Mormont | Honda | 本多 |
| Kai | AcrossTheSea | UmiNoKanata | 海の彼方 |
| Aki | greatmaster | Oyakata | 御屋形 |
| Aki | Targaryen | Mori | 毛利 |
| Aki | Dothraki | KibaShu | 騎馬衆 |
| Aki | Dragons | Ryuzoku | 竜族 |
| Aki | QueenProtector | JooShugo | 女王守護 |
| Aki | DragonsFriends | RyuNoTomo | 竜の友 |
| Aki | Spys | Shinobi | 忍び |

## Organisational Units (Yamato)

| GoT OU | SENGOAD OU | Kanji |
|---|---|---|
| Vale | Shinano | 信濃 |
| IronIslands | Awaji | 淡路 |
| Riverlands | Mino | 美濃 |
| Crownlands | Yamashiro | 山城 |
| Stormlands | Sagami | 相模 |
| Westerlands | Omi | 近江 |
| Reach | Owari | 尾張 |
| Dorne | Satsuma | 薩摩 |

## Other

| GoT | SENGOAD |
|---|---|
| `gmsaDragon` (gMSA) | `gmsaRyu` |
| `StarkWallpaper` (GPO) | `TakedaWallpaper` |
| `arya.txt` (loot file) | `kikuhime.txt` |

## Passwords

Each password keeps the *spirit* of the original (a motto, a sword name, a
weak-on-purpose word, the kerberoast joke, …) and a comparable strength, so the
lab's password policy and intended crackability still hold.

| Account | Password | Note |
|---|---|---|
| `takeda.shingen` | `Furinkazan!` | 風林火山 — Shingen's banner motto |
| `sanjo` | `katsuyorimatsuhimekikuhimeyoshinobunobukatsu` | her children's names |
| `takeda.katsuyori` | `ookami` | 狼 (wolf) |
| `matsuhime` | `345ertdfg` | weak keyboard pattern (unchanged) |
| `kikuhime` | `Harimaru` | 針 (needle) |
| `takeda.yoshinobu` | `miraigamieru` | "I can see the future" |
| `takeda.nobukatsu` | `Fuyu2022` | 冬 (winter) |
| `benkei` | `benkei` | his only word |
| `sanada.yukimura` | `Rokumonsen` | 六文銭 — the Sanada crest |
| `yamamoto.kansuke` | `Muramasa` | 村正 — legendary swordsmith |
| `honda.tadakatsu` | `_Tonb0g1ri_` | 蜻蛉切 — Tadakatsu's famed spear |
| `oda.nobunaga` | `TenkaFubu135` | 天下布武 — Nobunaga's motto |
| `oda.nobutada` | `oichi` | his lover's name |
| `oichi` | `il0venobutada` | loves her brother |
| `oda.nobutaka` | `Sak3&Onna` | sake & women |
| `toyotomi.hideyoshi` | `WareKosoTenka` | "I am the realm" |
| `toyotomi.hideyori` | `1Zankoku!` | 残酷 (cruel) |
| `toyotomi.hidenaga` | `naomori` | a lover's name |
| `toyotomi.hidetsugu` | `Ryuj0u!` | 竜城 — his seat |
| `akechi.mitsuhide` | `@Honnoji@` | 本能寺 — Akechi's coup |
| `hattori.hanzo` | `_Sh1nobi_$` | 忍び (shinobi) |
| `sen.rikyu` | `IchigoIchie` | 一期一会 — Rikyū's tea maxim |
| `mori.motonari` | `SanbonNoYa!` | 三本の矢 — the Three Arrows |
| `mori.terumoto` | `GoldKabuto` | a golden helmet |
| `date.masamune` | `horse` | 馬 (horse) — weak, on purpose |
| `honda.tadatomo` | `Bush1do!` | 武士道 (a warrior's honor) |
| `chiyo` | `Kaih0u!` | 解放 (liberation) |
| `orochi` | `Karyuu!` | 火竜 (fire dragon) |
| `sql_svc` | `KerberoastNanteMuri1` | "you'll never kerberoast me" |

> Unchanged because they are not themed names: all `local_admin_password`
> values, every `domain_password`, the MSSQL `sa` passwords, and cert passwords.

## DRACARYS lab (Japanese dragon myth)

| | GoT | SENGOAD |
|---|---|---|
| Forest / domain | `dracarys.lab` | `ryuen.lab` (竜炎) — NetBIOS `RYUEN` |
| Host (DC) | `balerion` | `ryujin` (竜神) |
| Host (server) | `vhagar` | `mizuchi` (蛟) |
| Host (linux) | `syrax` | `wani` (鰐) |
| User (Domain Admin) | `drogon` | `orochi` (オロチ) |
| User | `rhaegal` | `seiryu` (青竜) |
| User | `viserion` | `hakuryu` (白竜) |
| User (glpi svc) | `sunfyre` | `kinryu` (金竜) |

Group names `LinuxAdmins` / `LinuxUsers` and the (already random) passwords in
this lab are unchanged; only the names differ.

---

*SENGOAD is derived from [GOAD](https://github.com/Orange-Cyberdefense/GOAD)
by Orange Cyberdefense (see `LICENSE`).*
