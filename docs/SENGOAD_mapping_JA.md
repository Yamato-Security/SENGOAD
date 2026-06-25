# SENGOAD ― GOAD → 戦国時代 ネーミング対応表（日本語）

SENGOAD は GOAD ラボ一式の『ゲーム・オブ・スローンズ』風の名称を、日本の
**戦国時代**（1467〜1615年頃）に置き換えたものです。最優先は **知名度** で、
原作の設定に無理に合わせず、誰もが知る有名な氏族・武将を用います。スパイ／
諜報の要素には忍者（忍び）を当てています。

本書は、元の GOAD 名と SENGOAD 名の対応表です。**GOAD / GOAD-Light /
GOAD-Mini**（同じ名称セットを共有）と、独立した **DRACARYS** ラボを対象とします。

> 英語版は [SENGOAD_mapping_EN.md](./SENGOAD_mapping_EN.md) にあります。

## 方針・規約

- **ログイン名／`sAMAccountName` は ASCII のまま**（例: `takeda.shingen`）。攻撃
  ツールがそのまま使えるようにし、**AD の表示名（DisplayName）は漢字**にします
  （例: `武田信玄`）。`config.json` の `displayname` フィールドを介して、
  `ad` / `onlyusers` ロールの `win_domain_user` の `attributes.displayName` に
  渡しています。
- ログイン名は日本式の順 **「姓.名」** です。
- **女性は氏（名字）を付けず単独名**にしています（例: `お市の方`・`松姫`）。
  当時の女性は名字＋名で呼ばれなかったためです。氏族との関係は AD のグループ
  所属で表現します。
- パスワード・SPN・ACL・gMSA・MSSQL リンクサーバ・脆弱性設定（自動ログイン／
  資格情報キャッシュ）も、すべて新しい名称に同期しています。

## 氏族・武将（早わかり）

| 戦国の氏族・武将 | 漢字 | 補足 | （旧）GoT の家 |
|---|---|---|---|
| 織田信長 | 織田信長 | 天下統一の覇者 | ラニスター家 |
| 豊臣秀吉 | 豊臣秀吉 | 立身出世の天下人 | バラシオン家（玉座） |
| 武田信玄 | 武田信玄 | 「甲斐の虎」 | スターク家（北部） |
| 毛利元就 | 毛利元就 | 「三本の矢」の智将 | ターガリエン家（エッソス） |
| 伊達政宗 | 伊達政宗 | 「独眼竜」 | カール・ドロゴ |
| 真田幸村 | 真田幸村 | 人気No.1の英雄 | ジョン・スノウ |
| 山本勘助 | 山本勘助 | 武田の軍師（隻眼） | サムウェル・ターリー |
| 服部半蔵 | 服部半蔵 | 伝説の忍び | ヴァリス |
| 明智光秀 | 明智光秀 | 名高い裏切り者 | ベイリッシュ |
| 千利休 | 千利休 | 茶の湯の大宗匠 | 学匠パイセル |
| 本多忠勝 | 本多忠勝 | 無双の武将 | モルモント |

## フォレスト / ドメイン

| GoT ドメイン | SENGOAD ドメイン | NetBIOS |
|---|---|---|
| `sevenkingdoms.local` | `yamato.local`（大和） | `YAMATO` |
| `north.sevenkingdoms.local` | `kai.yamato.local`（甲斐） | `KAI` |
| `essos.local` | `aki.local`（安芸） | `AKI` |

大和＝中央の都（織田・豊臣）。甲斐＝武田信玄の領国（＝北部）で大和の子ドメイン。
安芸＝毛利元就の瀬戸内の領国（エッソス）。

## コンピューター（城）

| GoT ホスト | SENGOAD ホスト | 城 |
|---|---|---|
| `kingslanding` | `osaka` | 大坂城（秀吉の居城） |
| `winterfell` | `kofu` | 甲府（甲斐の武田の本拠） |
| `castelblack` | `shirakawa` | 白河関（北の大関門） |
| `meereen` | `hiroshima` | 広島城（毛利が築城） |
| `braavos` | `sakai` | 堺（自治の自由貿易都市） |

## ユーザー

### 大和（旧 sevenkingdoms）― 織田・豊臣

| GoT ログイン | SENGOAD ログイン | 表示名 |
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

### 甲斐（旧 north）― 武田

| GoT ログイン | SENGOAD ログイン | 表示名 |
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

### 安芸（旧 essos）― 毛利

| GoT ログイン | SENGOAD ログイン | 表示名 |
|---|---|---|
| `daenerys.targaryen` | `mori.motonari` | 毛利元就 |
| `viserys.targaryen` | `mori.terumoto` | 毛利輝元 |
| `khal.drogo` | `date.masamune` | 伊達政宗 |
| `jorah.mormont` | `honda.tadatomo` | 本多忠朝 |
| `missandei` | `chiyo` | 千代 |
| `drogon` | `orochi` | オロチ |
| `sql_svc` | `sql_svc` | *（変更なし・サービスアカウント）* |

## グループ

| 領 | GoT グループ | SENGOAD グループ | 漢字 |
|---|---|---|---|
| 大和 | Lannister | Oda | 織田 |
| 大和 | Baratheon | Toyotomi | 豊臣 |
| 大和 | Small Council | Gotairo | 五大老 |
| 大和 | DragonStone | Ryujo | 竜城 |
| 大和 | KingsGuard | Hatamoto | 旗本 |
| 大和 | DragonRider | Ryuki | 竜騎 |
| 大和 | AcrossTheNarrowSea | KaikyoNoKanata | 海峡の彼方 |
| 甲斐 | Stark | Takeda | 武田 |
| 甲斐 | Night Watch | Yoban | 夜番 |
| 甲斐 | Mormont | Honda | 本多 |
| 甲斐 | AcrossTheSea | UmiNoKanata | 海の彼方 |
| 安芸 | greatmaster | Oyakata | 御屋形 |
| 安芸 | Targaryen | Mori | 毛利 |
| 安芸 | Dothraki | KibaShu | 騎馬衆 |
| 安芸 | Dragons | Ryuzoku | 竜族 |
| 安芸 | QueenProtector | JooShugo | 女王守護 |
| 安芸 | DragonsFriends | RyuNoTomo | 竜の友 |
| 安芸 | Spys | Shinobi | 忍び |

## 組織単位（OU・大和）

| GoT OU | SENGOAD OU | 漢字 |
|---|---|---|
| Vale | Shinano | 信濃 |
| IronIslands | Awaji | 淡路 |
| Riverlands | Mino | 美濃 |
| Crownlands | Yamashiro | 山城 |
| Stormlands | Sagami | 相模 |
| Westerlands | Omi | 近江 |
| Reach | Owari | 尾張 |
| Dorne | Satsuma | 薩摩 |

## その他

| GoT | SENGOAD |
|---|---|
| `gmsaDragon`（gMSA） | `gmsaRyu` |
| `StarkWallpaper`（GPO） | `TakedaWallpaper` |
| `arya.txt`（お宝ファイル） | `kikuhime.txt` |

## パスワード

各パスワードは元の「趣旨」（標語・刀の名・あえて弱い語・Kerberoast の小ネタ
など）と同程度の強度を保っており、ラボのパスワードポリシーと「割れやすさ」の
意図はそのまま成立します。

| アカウント | パスワード | 補足 |
|---|---|---|
| `takeda.shingen` | `Furinkazan!` | 風林火山（信玄の旗印） |
| `sanjo` | `katsuyorimatsuhimekikuhimeyoshinobunobukatsu` | 子供達の名 |
| `takeda.katsuyori` | `ookami` | 狼 |
| `matsuhime` | `345ertdfg` | 弱いキー配列（変更なし） |
| `kikuhime` | `Harimaru` | 針 |
| `takeda.yoshinobu` | `miraigamieru` | 未来が見える |
| `takeda.nobukatsu` | `Fuyu2022` | 冬 |
| `benkei` | `benkei` | 唯一の言葉 |
| `sanada.yukimura` | `Rokumonsen` | 六文銭（真田の家紋） |
| `yamamoto.kansuke` | `Muramasa` | 村正（名工） |
| `honda.tadakatsu` | `_Tonb0g1ri_` | 蜻蛉切（忠勝の名槍） |
| `oda.nobunaga` | `TenkaFubu135` | 天下布武 |
| `oda.nobutada` | `oichi` | 恋人の名 |
| `oichi` | `il0venobutada` | 兄を慕う |
| `oda.nobutaka` | `Sak3&Onna` | 酒と女 |
| `toyotomi.hideyoshi` | `WareKosoTenka` | 我こそ天下 |
| `toyotomi.hideyori` | `1Zankoku!` | 残酷 |
| `toyotomi.hidenaga` | `naomori` | 恋人の名 |
| `toyotomi.hidetsugu` | `Ryuj0u!` | 竜城（本拠） |
| `akechi.mitsuhide` | `@Honnoji@` | 本能寺（謀叛） |
| `hattori.hanzo` | `_Sh1nobi_$` | 忍び |
| `sen.rikyu` | `IchigoIchie` | 一期一会 |
| `mori.motonari` | `SanbonNoYa!` | 三本の矢 |
| `mori.terumoto` | `GoldKabuto` | 黄金の兜 |
| `date.masamune` | `uma` | 馬（あえて弱い） |
| `honda.tadatomo` | `Bush1do!` | 武士道 |
| `chiyo` | `Kaih0u!` | 解放 |
| `orochi` | `Karyuu!` | 火竜 |
| `sql_svc` | `KerberoastNanteMuri1` | 「Kerberoast なんて無理」 |

> 変更しないもの（テーマ名ではないため）: すべての `local_admin_password`、各
> `domain_password`、MSSQL の `sa` パスワード、証明書パスワード。

## DRACARYS ラボ（日本の竜神話）

| | GoT | SENGOAD |
|---|---|---|
| フォレスト / ドメイン | `dracarys.lab` | `ryuen.lab`（竜炎）― NetBIOS `RYUEN` |
| ホスト（DC） | `balerion` | `ryujin`（竜神） |
| ホスト（サーバ） | `vhagar` | `mizuchi`（蛟） |
| ホスト（Linux） | `syrax` | `wani`（鰐） |
| ユーザー（Domain Admin） | `drogon` | `orochi`（オロチ） |
| ユーザー | `rhaegal` | `seiryu`（青竜） |
| ユーザー | `viserion` | `hakuryu`（白竜） |
| ユーザー（glpi サービス） | `sunfyre` | `kinryu`（金竜） |

グループ名 `LinuxAdmins` / `LinuxUsers` と、このラボの（元々ランダムな）
パスワードは変更していません。名前のみ変わります。

---

*SENGOAD は Orange Cyberdefense の
[GOAD](https://github.com/Orange-Cyberdefense/GOAD) を基にしています
（`LICENSE` 参照）。*
