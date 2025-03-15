# フラクタルジェネレータ インストールガイド

## はじめに

このガイドでは、フラクタルジェネレータのインストール方法について説明します。フラクタルジェネレータは、美しいフラクタル画像を作成するためのPythonアプリケーションです。

## 目次

1. [システム要件](#システム要件)
2. [インストール方法](#インストール方法)
   - [Windows](#windows)
   - [macOS](#macos)
   - [Linux](#linux)
3. [起動方法](#起動方法)
4. [アップデート方法](#アップデート方法)
5. [アンインストール方法](#アンインストール方法)
6. [トラブルシューティング](#トラブルシューティング)

## システム要件

フラクタルジェネレータを実行するには、以下の要件を満たす必要があります：

### 最小要件

- **OS**: 
  - Windows 10/11
  - macOS 10.14以降
  - Linux (Ubuntu 20.04以降推奨)
- **プロセッサ**: デュアルコア 2GHz以上
- **メモリ**: 4GB RAM
- **ディスク容量**: 500MB以上の空き容量
- **ディスプレイ**: 1280x720以上の解像度
- **Python**: バージョン3.8以上（インストーラーに同梱）

### 推奨要件

- **プロセッサ**: クアッドコア 3GHz以上
- **メモリ**: 8GB RAM以上
- **グラフィックス**: 専用GPUメモリ2GB以上
- **ディスク容量**: 1GB以上の空き容量
- **ディスプレイ**: 1920x1080以上の解像度

## インストール方法

### Windows

#### インストーラーを使用する方法（推奨）

1. [公式サイト](https://fractal-generator.example.com/download)から最新のインストーラー（`fractal_generator_setup.exe`）をダウンロードします
2. ダウンロードしたインストーラーをダブルクリックして実行します
3. 画面の指示に従ってインストールを進めます
   - インストール先フォルダを選択します（デフォルト: `C:\Program Files\FractalGenerator`）
   - スタートメニューフォルダを選択します
   - デスクトップショートカットを作成するかどうかを選択します
4. 「インストール」ボタンをクリックしてインストールを開始します
5. インストールが完了したら「完了」ボタンをクリックします

#### ZIPファイルを使用する方法

1. [公式サイト](https://fractal-generator.example.com/download)から最新のZIPパッケージ（`fractal_generator_windows.zip`）をダウンロードします
2. ダウンロードしたZIPファイルを任意の場所に展開します
3. 展開したフォルダ内の `setup.bat` を実行して必要な依存関係をインストールします
4. インストールが完了すると、フォルダ内に `fractal_generator.bat` が作成されます

### macOS

#### DMGファイルを使用する方法（推奨）

1. [公式サイト](https://fractal-generator.example.com/download)から最新のDMGファイル（`fractal_generator.dmg`）をダウンロードします
2. ダウンロードしたDMGファイルをダブルクリックして開きます
3. アプリケーションアイコンをApplicationsフォルダにドラッグ＆ドロップします
4. 初回起動時にセキュリティ警告が表示される場合は、「システム環境設定」→「セキュリティとプライバシー」で「このまま開く」を選択します

#### ZIPファイルを使用する方法

1. [公式サイト](https://fractal-generator.example.com/download)から最新のZIPパッケージ（`fractal_generator_macos.zip`）をダウンロードします
2. ダウンロードしたZIPファイルを任意の場所に展開します
3. ターミナルを開き、展開したフォルダに移動します
4. `./setup.sh` を実行して必要な依存関係をインストールします
5. インストールが完了すると、フォルダ内に `fractal_generator.command` が作成されます

### Linux

#### Debianパッケージを使用する方法（Ubuntu/Debian）

1. [公式サイト](https://fractal-generator.example.com/download)から最新のDEBパッケージ（`fractal-generator_1.0.0_amd64.deb`）をダウンロードします
2. ターミナルを開き、ダウンロードしたファイルのあるディレクトリに移動します
3. 以下のコマンドを実行してインストールします：

```bash
sudo apt install ./fractal-generator_1.0.0_amd64.deb
```

4. 依存関係が自動的にインストールされます

#### RPMパッケージを使用する方法（Fedora/CentOS）

1. [公式サイト](https://fractal-generator.example.com/download)から最新のRPMパッケージ（`fractal-generator-1.0.0.x86_64.rpm`）をダウンロードします
2. ターミナルを開き、ダウンロードしたファイルのあるディレクトリに移動します
3. 以下のコマンドを実行してインストールします：

```bash
sudo dnf install ./fractal-generator-1.0.0.x86_64.rpm
```

4. 依存関係が自動的にインストールされます

#### ソースからインストールする方法

1. [公式サイト](https://fractal-generator.example.com/download)から最新のソースパッケージ（`fractal_generator_source.tar.gz`）をダウンロードします
2. ターミナルを開き、ダウンロードしたファイルのあるディレクトリに移動します
3. 以下のコマンドを実行して展開します：

```bash
tar -xzf fractal_generator_source.tar.gz
cd fractal_generator
```

4. 依存関係をインストールします：

```bash
sudo apt install python3-pip python3-tk python3-dev
# または
sudo dnf install python3-pip python3-tkinter python3-devel
```

5. Pythonの依存パッケージをインストールします：

```bash
pip3 install -r requirements.txt
```

6. インストールスクリプトを実行します：

```bash
./install.sh
```

## 起動方法

### Windows

- デスクトップのショートカットをダブルクリックします
- または、スタートメニューから「フラクタルジェネレータ」を選択します
- または、インストールフォルダ内の `fractal_generator.exe` を実行します

### macOS

- Launchpadから「フラクタルジェネレータ」を選択します
- または、Applicationsフォルダから「フラクタルジェネレータ」をダブルクリックします
- または、ZIPからインストールした場合は `fractal_generator.command` をダブルクリックします

### Linux

- アプリケーションメニューから「フラクタルジェネレータ」を選択します
- または、ターミナルで `fractal-generator` コマンドを実行します
- または、ソースからインストールした場合はインストールディレクトリで `./run.sh` を実行します

## アップデート方法

### 自動アップデート

フラクタルジェネレータは起動時に自動的に更新を確認します。新しいバージョンが利用可能な場合は、通知が表示されます。「今すぐ更新」ボタンをクリックすると、アップデートがダウンロードされ、インストールされます。

### 手動アップデート

#### Windows

1. 既存のバージョンをアンインストールします（データは保持されます）
2. 新しいバージョンのインストーラーをダウンロードして実行します

#### macOS

1. 古いバージョンをApplicationsフォルダからゴミ箱に移動します
2. 新しいバージョンのDMGファイルをダウンロードし、アプリケーションをApplicationsフォルダにドラッグします

#### Linux

##### Debian/Ubuntu

```bash
sudo apt update
sudo apt install --only-upgrade fractal-generator
```

##### Fedora/CentOS

```bash
sudo dnf upgrade fractal-generator
```

##### ソースからインストールした場合

```bash
cd fractal_generator
git pull
pip3 install -r requirements.txt --upgrade
./install.sh
```

## アンインストール方法

### Windows

1. 「設定」→「アプリ」→「アプリと機能」を開きます
2. リストから「フラクタルジェネレータ」を選択します
3. 「アンインストール」ボタンをクリックし、画面の指示に従います

または、コントロールパネルの「プログラムのアンインストール」からも削除できます。

### macOS

1. Applicationsフォルダから「フラクタルジェネレータ」をゴミ箱に移動します
2. 関連設定ファイルを削除するには、以下のフォルダも削除します：
   - `~/Library/Application Support/FractalGenerator`
   - `~/Library/Preferences/com.example.fractal-generator.plist`

### Linux

#### Debian/Ubuntu

```bash
sudo apt remove fractal-generator
# 設定ファイルも削除する場合
sudo apt purge fractal-generator
```

#### Fedora/CentOS

```bash
sudo dnf remove fractal-generator
```

#### ソースからインストールした場合

```bash
cd fractal_generator
./uninstall.sh
```

## トラブルシューティング

### 一般的な問題

#### アプリケーションが起動しない

1. システム要件を満たしているか確認します
2. 最新バージョンをインストールしているか確認します
3. 依存関係が正しくインストールされているか確認します

#### エラーメッセージ「ModuleNotFoundError」

必要なPythonパッケージがインストールされていません。以下のコマンドを実行してください：

```bash
pip3 install -r requirements.txt
```

#### 画面が表示されない、または表示が乱れる

1. グラフィックドライバーが最新であることを確認します
2. ディスプレイ解像度が最小要件を満たしているか確認します
3. 別のディスプレイで試してみます

### プラットフォーム固有の問題

#### Windows

- **「VCRUNTIME140.dll が見つかりません」エラー**：
  Visual C++ 再頒布可能パッケージをインストールしてください。[Microsoft公式サイト](https://support.microsoft.com/ja-jp/help/2977003/the-latest-supported-visual-c-downloads)からダウンロードできます。

- **「Python38.dll が見つかりません」エラー**：
  インストーラーを再実行するか、[Python公式サイト](https://www.python.org/downloads/)から Python 3.8 以上をインストールしてください。

#### macOS

- **「開発元を確認できないため開けません」エラー**：
  Controlキーを押しながらアプリケーションをクリックし、「開く」を選択します。その後、「開く」ボタンをクリックします。

- **「ライブラリをロードできません」エラー**：
  ターミナルで以下のコマンドを実行してください：
  ```bash
  xcode-select --install
  ```

#### Linux

- **「libGL error」エラー**：
  OpenGLライブラリをインストールしてください：
  ```bash
  # Ubuntu/Debian
  sudo apt install libgl1-mesa-glx
  
  # Fedora/CentOS
  sudo dnf install mesa-libGL
  ```

- **「Tkinter」関連のエラー**：
  Tkinterパッケージをインストールしてください：
  ```bash
  # Ubuntu/Debian
  sudo apt install python3-tk
  
  # Fedora/CentOS
  sudo dnf install python3-tkinter
  ```

### ログファイル

問題が解決しない場合は、ログファイルを確認してください。ログファイルは以下の場所にあります：

- **Windows**: `%APPDATA%\FractalGenerator\logs\`
- **macOS**: `~/Library/Logs/FractalGenerator/`
- **Linux**: `~/.local/share/fractal-generator/logs/`

ログファイルを添えて、[サポートフォーラム](https://fractal-generator.example.com/support)または[GitHub Issues](https://github.com/example/fractal-generator/issues)で問題を報告してください。

---

このインストールガイドは、フラクタルジェネレータの基本的なインストール方法と一般的な問題の解決方法を説明しています。さらに詳しい情報や最新の更新については、[公式サイト](https://fractal-generator.example.com)をご参照ください。
