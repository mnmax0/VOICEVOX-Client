# VOICEVOX Client

## 概要

VOICEVOX engineをPythonから利用して音声合成するツール。

## ユーザーガイド

### 使い方(音声を生成)
手順としては以下になります。
1. VOICEVOX engine あるいは VOICEVOX NEMO engineの起動（両方でも片方でもOK)
2. ここで配布してるPythonスクリプトを利用して音声合成

#### VOICEVOX engineの起動

Dockerイメージが公開されてるので、それを使わせてもらうのが楽。

CPUバージョンなら以下で (GPUを希望の場合はそっちを）

```bash
docker pull voicevox/voicevox_engine:cpu-latest
docker run --rm -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-latest
```

#### VOICEVOX NEMO engineの起動

```bash
docker pull voicevox/voicevox_nemo_engine:cpu-ubuntu20.04-latest
docker run --rm -p '127.0.0.1:50121:50121' voicevox/voicevox_nemo_engine:cpu-ubuntu20.04-latest
```
(VOICEVOX engineと開放してるポート番号が異なります。)

#### VOICEVOX Clientを利用してファイルの文書を音声合成

読み上げしたい文書がはいっているテキストファイルがyoutube.txtで、読み上げ速度を1.4倍にする時は以下

```bash
python3.11 voicevox_client.py -i youtubeyou.txt -v 1.4 2> /dev/null
```

* iオプションで、読み上げ対象のテキストファイルを指定
* vオプションで、読み上げ速度を1.4倍に
* デフォルトは http://127.0.0.1:50121のエンジンを利用します（VOICEVOX NEMOエンジン）他のエンジンを使いたい場合は -p で違うポートを指定 ( urlも違うなら-uオプションで）
* speakerのidはデフォルトは10006です。違うidの音声を利用する場合は-s オプションで指定

以下はVOICEVOX NEMOではなくて、VOICEVOXを利用する場合で、speaker idが1の時
```bash
python3.11 voicevox_client.py -i youtubeyou.txt -u http://127.0.0.1 -s 1 -v 1.4 2> /dev/null
```

#### ファイルではなく、読ませたい文書をコマンドラインオプションで渡す
* -t オプションを使う

```bash
python3.11 voicevox_client.py -t "これよんで" -v 1.4 2> /dev/null
```

### 音声合成したデータをwavファイルとして出力
* -w オプションをつける

```bash
python3.11 voicevox_client.py -i youtubeyou.txt -v 1.4 -w 2> /dev/null
```

* -x オプションをつけると、音声合成した音を再生しない。（静かに音声合成)
```bash
python3.11 voicevox_client.py -i youtubeyou.txt -v 1.4 -w -x 2> /dev/null
```

* -tオプションと -iオプションを同時につかうと、-iオプションで指定したファイルの情報の前に、-tオプションで指定した文書を音声合成

### 辞書から登録してある単語を削除
Pythonをパイソンと発音するように辞書登録する場合

```bash
python3.11 voicevox_client.py -d "消したい登録ID"
```

### VOICEVOX engineで使えるスピーカー情報の表示(エンジンのバージョン、ユーザー辞書情報も出るようになりました）

* VOICEVOX engineがhttp://127.0.0.1のポート50021で動いている場合

```bash
python3.11 voicevox_client.py -l -p 50021
```

他のURLなら-uオプションでURL情報も渡す

```bash
python3.11 voicevox_client.py -l -p 50021 -u VOICEVOXエンジンが動いているURL
```

* 現在こちらで使ってるVOICEVOX engineでは、0から86のスピーカーidが利用可能でした

### VOICEVOX NEMO engineで使えるスピーカー情報の表示
* VOICEVOX NEMO engineがhttp://127.0.0.1のポート50121で動いている場合

```bash
python3.11 voicevox_client.py -l 
```

* 現在こちらで使ってるVOICEVOX NEMO engineだと、10000から10008のスピーカーidが利用可能でした


#### VOICEVOX Clientのオプション一覧
--helpオプションで、可能なオプションを表示します。
```bash
python3.11 voicevox_client.py --help
```

その時の出力が以下(初期バージョン)
```text
usage: voicevox_client.py [-h] [-t TEXT] [-i INPUT_FILENAME] [-u URL] [-p PORT] [-s SPEAKERID] [-l] [-o OUTPUT_FILENAME_BASE] [-w] [-x] [-f] [-d DELELTEWORDREGISTRATION] [-r WORDREGISTRATION]
                          [-v SPEEDSCALE] [--pitchScale PITCHSCALE] [--intonationScale INTONATIONSCALE] [--volumeScale VOLUMESCALE] [--prePhonemeLength PREPHONEMELENGTH]
                          [--postPhonemeLength POSTPHONEMELENGTH] [--outputSamplingRate OUTPUTSAMPLINGRATE] [--outputStereo]

VOicevox client: VOICEVOXエンジンを利用して音声合成するツール(先にVOICEVOXエンジンを動かす必要あり)

options:
  -h, --help            show this help message and exit
  -t TEXT, --text TEXT  音声合成する文書
  -i INPUT_FILENAME, --input_filename INPUT_FILENAME
                        音声合成する文書ファイル指定
  -u URL, --url URL     VoicevoxエンジンのURL
  -p PORT, --port PORT  Voicevoxエンジンのポート
  -s SPEAKERID, --speakerid SPEAKERID
                        スピーカーのID
  -l, --listspeakers    そのエンジンのバージョン、利用可能なspeakers(json形式),ユーザー辞書(json形式)の情報出力
  -o OUTPUT_FILENAME_BASE, --output_filename_base OUTPUT_FILENAME_BASE
                        出力ファイルの名前の先頭指定（無指定ならOUT)
  -w, --enable_output_file
                        ファイル出力するモード
  -x, --disable_playwith
                        音声出力しないモード
  -f, --overwritemode   出力ファイルを上書きモード
  -d DELELTEWORDREGISTRATION, --delelteWordRegistration DELELTEWORDREGISTRATION
                        登録IDの辞書登録単語を消す
  -r WORDREGISTRATION, --wordRegistration WORDREGISTRATION
                        辞書登録、||区切りで　登録単語||発音||アクセントタイプ 登録単語||発音にするとアクセントタイプは１で登録 ex. Python||パイソン||1 とか Python||パイソン
  -v SPEEDSCALE, --speedScale SPEEDSCALE
                        speedScale 話速(デフォルト1)
  --pitchScale PITCHSCALE
                        pitchScale ピッチ(デフォルト0)
  --intonationScale INTONATIONSCALE
                        intonationScale 抑揚(デフォルト1)
  --volumeScale VOLUMESCALE
                        volumeScale ボリューム(デフォルト1)
  --prePhonemeLength PREPHONEMELENGTH
                        prePhonemeLength 前の長さ(デフォルト0.1)
  --postPhonemeLength POSTPHONEMELENGTH
                        postPhonemeLength 後ろの長さ(デフォルト0.1)
  --outputSamplingRate OUTPUTSAMPLINGRATE
                        outputSamplingRate 出力周波数(デフォルト24000)
  --outputStereo        outputStereo ステレオにする？（デフォルトはfalse)

VOICEVOX engineなら docker run --rm -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-latest VOICEVOX NEMO engineなら docker run --rm --gpus all -p '127.0.0.1:50121:50121'
voicevox/voicevox_nemo_engine:cpu-ubuntu20.04-latest
```

注) Ubuntu22.04で作業しました。2024/2/12時点で、Python3.10だとpyaudioで音を再生しようとするとエラーになりました。python3.11にあげると、この問題は解消されます。私はvenvでその環境を作って動作させました。音声を再生せずに、wavファイルとして出力するだけなら、Python3.10でも問題ありません。pyaudioのかわりに、mpvとか外部コマンドで再生するようにしたら、ここらの問題は発生しないのですが、なんとなく今の感じにしました。（もともとはwavファイルを出力して、それを外部コマンドで音にしてました）

### 辞書に単語登録
* ||区切りで　登録単語||発音||アクセントタイプ 登録単語||発音にするとアクセントタイプは１で登録 ex. Python||パイソン||1 とか Python||パイソン

#### Pythonをパイソンと発音するように辞書登録する場合

```bash
python3.11 voicevox_client.py -r "Python||パイソン||1"
```

あるいは

```bash
python3.11 voicevox_client.py -r "Python||パイソン"
```

### 一括登録用スクリプト例 tourokuEx.sh

```bash
./tourokuEx.sh エンジンのポート 辞書データファイル 
あるいは
./tourokuEx.sh エンジンのポート 
あるいは
./tourokuEx.sh 
```

辞書データファイルは以下のようにvoicevox_client.pyのrオプションに渡す内容を入れたもの

```text
Python||パイソン||1
Github||ギットハブ
Docker||ドッカー
NEMO||ネモ||0
script言語||スクリプトゲンゴ||0
```

tourokuEx.shの引数を渡さない場合、ポートは50121、辞書ファイルは myjisyo.dat が対象になる。

## ファイルの説明
<dl>
  <dt>voicevox_client.py</dt> <dd>プログラム本体</dd>
  <dt>startNEMOengine.sh </dt> <dd>VOICEVOX NEMO engine起動スクリプト</dd>
  <dt>startVOICEVOXengine.sh </dt> <dd>VOICEVOX NEMO engine起動スクリプト</dd>
  <dt>tourokuEx.sh</dt> <dd>辞書登録の例</dd>
  <dt>youtubeyou.txt</dt> <dd>テスト用のテキストファイル</dd>
  <dt>atokaraPlay.py</dt> <dd>生成したwav,txtファイルを表示しながら再生するプログラム</dd>
  <dt></dt> <dd></dd>
</dl>

## ライセンス
[MIT](https://opensource.org/license/mit/ "MIT")

## 説明動画
* https://youtu.be/c7LvNuyR3oM
* https://youtu.be/0yDiLfworwI

## 関連サイト
* 私のYoutubeチャンネル https://www.youtube.com/channel/UCNko_uhYtoTowASAuOam17w
*  [VOICEVOX engine](https://github.com/VOICEVOX/voicevox_engine/tree/master) 
*  [VOICEVOX engineのDocker images](https://hub.docker.com/r/voicevox/voicevox_engine) 
*  [VOICEVOX NEMO engine](https://github.com/VOICEVOX/voicevox_nemo_engine) 
*  [VOICEVOX engineのDocker images](https://hub.docker.com/r/voicevox/voicevox_nemo_engine) 
*  [VOICEVOX](https://voicevox.hiroshiba.jp/) 
*  [VOICEVOX NEMO](https://voicevox.hiroshiba.jp/nemo/) 
*  [VOICEVOX WEB](https://www.voicevox.su-shiki.com/) 
