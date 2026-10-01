# ChainOSCPad Series Portal

同じChainOSCPadハードウェアで動作する **OSC / Keyboard / MIDI** の3プロジェクトを紹介する、日本語の静的ポータルサイトです。

## コンテンツ

- 用途別のプロジェクト紹介と、GitHub Pages・Web Installer・GitHubへのリンク
- XIAO ESP32S3 / C3 / C6 / C5の対応比較
- ファームウェアの切り替え、設定バックアップ、Bluetooth再ペアリングの案内
- 共通ピン割り当て、よくある質問、ChainOSCシリーズへのリンク

## リンク先

| プロジェクト | GitHub Pages | GitHub |
|---|---|---|
| ChainOSCPad（OSC） | https://shimez.github.io/ChainOSCPad/ | https://github.com/shimez/ChainOSCPad |
| ChainOSCPad Keyboard | https://shimez.github.io/ChainOSCPad-Keyboard/ | https://github.com/shimez/ChainOSCPad-Keyboard |
| ChainOSCPad MIDI | https://shimez.github.io/ChainOSCPad-MIDI/installer/ | https://github.com/shimez/ChainOSCPad-MIDI |

Keyboardの設定画面は https://shimez.github.io/ChainOSCPad-Keyboard/configurator.html です。

## ローカルで確認

Python 3.10以降を使用します。追加パッケージやサイトのビルドは不要です。

```powershell
python scripts/check_site.py
python -m http.server 8080 --bind 127.0.0.1 --directory site
```

ブラウザーで http://localhost:8080/ を開きます。HTMLを直接開いても閲覧できます。外部リンクのHTTP応答まで確認する場合は `python scripts/check_site.py --external` を実行してください。外部サイトの一時的なエラーやレート制限は別途確認します。

Windowsで`python`が動作しない場合は、`py -3`に置き換えて実行してください。この環境では`py -3 scripts/check_site.py --external`で確認しています。

## GitHub Pagesへ公開

想定リポジトリ名は `shimez/ChainOSCPad-Portal` です。この名前で公開した場合、URLは https://shimez.github.io/ChainOSCPad-Portal/ になります。

1. このフォルダーをGitリポジトリとして初期化し、GitHubへpushします。
2. GitHubの **Settings → Pages → Build and deployment → Source** を **GitHub Actions** に設定します。
3. **Actions → Validate and deploy portal → Run workflow** をmainブランチで実行します。
4. 以後はmainへのpushで、リンク検証後に`site/`が自動公開されます。

```powershell
git init -b main
git add .
git commit -m "Add ChainOSCPad series portal"
gh repo create shimez/ChainOSCPad-Portal --public --source . --remote origin --push
```

CLIでPagesを設定する場合：

```powershell
gh api --method POST repos/shimez/ChainOSCPad-Portal/pages -f build_type=workflow
gh workflow run pages.yml --ref main
```

Pagesの設定前に初回pushのデプロイが失敗した場合は、設定後にworkflowを再実行します。`github-pages` Environmentのデプロイルールではmainブランチを許可してください。Pull Requestは検証のみ行います。

## 構成

```text
site/
  index.html           ポータル本体
  assets/style.css     レスポンシブスタイル
  assets/chainoscpad-device.jpg  ChainOSCポータル掲載の実機写真
  assets/favicon.svg   サイトアイコン
  license.txt          公開サイト用ライセンス
scripts/check_site.py  ローカルリンク・画像・ID・外部URL確認
.github/workflows/pages.yml
```

JavaScript、外部フォント、CDN、アクセス解析は使用していません。カードのリンク、比較表、FAQはJavaScriptなしで利用できます。書き込みや設定は各プロジェクトの既存ページへ案内します。

## コンテンツ更新

- 各プロジェクトのREADMEと公開ページを基準に仕様を更新します。
- KeyboardのS3 USB版／BLE版が別ファームであること、C3/C6/C5はUSB HID／MIDI非対応であることに注意してください。
- このポータルにはファームウェアのバージョンやBINを複製せず、各公開元へのリンクを維持します。
- 仕様を見直したときはフッターの「コンテンツ確認日」を更新します。
- URL変更時は`site/index.html`と、このREADMEの両方を更新します。
- 実機写真は[ChainOSCポータルの掲載写真](https://shimez.github.io/ChainOSC/assets/chainoscpad-device.jpg)を保存して使用しています。写真はChainOSCPadのプロトタイプです。

## ライセンス

サイト独自のHTML・CSS・SVG・スクリプト・文書はMIT Licenseです。各リンク先のファームウェアと第三者コンポーネントは、それぞれのプロジェクトのライセンスに従います。
