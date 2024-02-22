# VOICEVOX Client

## 概要

VOICEVOX engineをPythonから利用して音声合成するツール。

## ユーザーガイド

### 必要なパッケージ
pyaudio, lark
pipを使うなどしてインストールしてください。
Ubuntu22.04の場合、python3.10だとpyaudioでエラーが発生します。python3.11をインストールして、そちらを使ってください。
再生せずにファイルに出力だけならpython3.10でもOK

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
docker run --rm -p '127.0.0.1:50121:50121' voicevox/voicevox_nemo_engine:cpu-latest
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
* -s オプションで、話者の名前や、タイプを指定できるようになりました(2024/2/20)

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
                        スピーカーのID or 話者の名前とタイプ。タイプを省略した場合ノーマルタイプのID ex. 10006, 女性6||ノーマル, 女性6
  -l, --listspeakers    そのエンジンのバージョン、利用可能なspeakers(json形式),ユーザー辞書(json形式)の情報出力
  -o OUTPUT_FILENAME_BASE, --output_filename_base OUTPUT_FILENAME_BASE
                        出力ファイルの名前の先頭指定（無指定でiオプション使ってなければOUT、iオプション使ってるなら入力ファイル名のbaseに_を追加した文字列)
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
voicevox/voicevox_nemo_engine:cpu-latest
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

## 簡易言語 
myparser.py で処理。出力ファイルの再生用が atokaraPlayV2.py

### 例 tests/youtubeyou20240221.vv という台本ファイルを処理
```bash
python3.11 myparser.py -i tests/youtubeyou20240221.vv -w -f
```

これで、wav, json, txtの３つのファイルが１行毎に作成されます。 (音声ファイル、各種情報が辞書形式ではいってるファイル、読み上げた文字の情報のテキストファイル)
(jsonファイルを、jsonライブラリでインポートしようとするとエラーになりました。astパッケージを利用すると辞書形式であつかえました。)

例 上記で作成した出力ファイルを再生
```bash
python3.11 atokaraPlayV2.py -b youtubeyou20240221 -d tests/  2> /dev/null
```
章毎に入力待ちになります。

台本ファイルの例
```bash
#c| set _x   話者:女声6 話速:1.4
#c| set _y   話者:四国めたん タイプ:あまあま 話速:1.4 音高:0.0 抑揚:1.0 音量:1.0 開始無音:0.1 終了無音:0.1
#c| set _yy  話者:四国めたん タイプ:ノーマル speedScale:1.4 pitchScale:0.0 intonationScale:1.0 volumeScale:1.0 prePhonemeLength:0.1 postPhonemeLength:0.1
#c| set _z   話者:ずんだもん タイプ:あまあま 話速:1.4 音高:0.0 抑揚:1.0 音量:1.0 開始無音:0.1 終了無音:0.1
#c| set _zz  話者:ずんだもん タイプ:ノーマル 話速:1.4 音高:0.0 抑揚:1.0 音量:1.0 開始無音:0.1 終了無音:0.1
#c| Cchange  話速:1.4
前の動画の後、いろいろ改造しました。前はSpeakerのIDで指定してましたが、名前とタイプで指定出来るようにしました。
#c| newChapter
また、ファイル出力する先が、作業ディレクトリでしたが、出力先無指定の場合は、元のファイルがあるディレクトリに出力するようにしました。
#c| newChapter
あと、簡易言語ファイルを元に音声合成と、合成時の情報をjsonファイルに、また読み上げ文字をtextファイルに出力するようにしました。
#c| newChapter
これは、後から再生するときに、背景とか、動画とか、自動入力など、音声ファイルだけではなくて、他と生成した音声を組み合わせて使いやすくするためです。
この簡易言語ファイルからの合成だと、Speakerの交代がやりやすいので、複数のSpeakerを交互に使う時にはやりやすくなります。
色々試行錯誤してるあいだに、ソースが汚くなってて恥ずかしいのですが、Githubに最新バージョンを公開してあります。
今後使いながら、使い方とか文法どんどんかわってしまうかもしれませんが、よろしくお願いいたします。
以降の動画で変更点とか、簡易言語の説明をしていく予定です。それではまたね！

_x:寿司食いたい！
_y:他に良いのあるかな？
_z:中華も良いかも
```

### help表示
```bash
python3 myparser.py --help
```
以下の出力
```text
usage: myparser.py [-h] -i INPUT_FILENAME [-o OUTPUT_FILENAME_BASE] [-w] [-f]
                   [--outputSamplingRate OUTPUTSAMPLINGRATE] [--outputStereo]

VOicevox client: VOICEVOXエンジンを利用して音声合成する簡易言語(先にVOICEVOXエンジンを動かす必要あり)

options:
  -h, --help            show this help message and exit
  -i INPUT_FILENAME, --input_filename INPUT_FILENAME
                        ソースファイル
  -o OUTPUT_FILENAME_BASE, --output_filename_base OUTPUT_FILENAME_BASE
                        出力ファイルの名前の先頭指定（無指定でiオプション使ってなければOUT、iオプション使ってるなら入力ファイル
                        名のbaseに_を追加した文字列)
  -w, --enable_output_file
                        ファイル出力するモード
  -f, --overwritemode   出力ファイルを上書きモード
  --outputSamplingRate OUTPUTSAMPLINGRATE
                        outputSamplingRate 出力周波数(デフォルト24000)
  --outputStereo        outputStereo ステレオにする？（デフォルトはfalse)
```

## 簡易言語 myparser.pyで生成したファイルで使われてるSpeakerの情報を調べるツール 
### 使用例 youtubeyou20240221-2.vvという台本ファイルから生成したファイルが /home/youtube/tmp/02にある場合
```bash
python3 checkSpeakers.py -d /home/youtube/tmp/02 -b youtubeyou20240221-2
```
出力
```text
女声6(ノーマル),簡易言語を利用して、前の動画を作りました。その手順を紹介します。
女声6(ノーマル),まず、台本ファイルを作成しました。 そのファイルがこれです。
... 省略 ...
女声6(ノーマル),話がそれましたが、前の動画の作成手順の説明をしました。
女声6(ノーマル),今後の動画では、簡易言語を使って台本を作る命令を順に説明していこうかと考えてます。それではまたね！
{'女声6': ''}
dict_keys(['女声6'])
「VOICEVOX NEMO」
```

### help表示
ヘルプ表示命令
```bash
python3 checkSpeakers.py --help
```
出力
```text
usage: checkSpeakers.py [-h] [-b FILENAME_BASE] [-d TARGET_DIRECTORY]
                        [-c START_CHAPTER_NUMBER]

myparse.pyで生成したjsonファイルを確認して、使ったSpeakerのリストを表示

options:
  -h, --help            show this help message and exit
  -b FILENAME_BASE, --filename_base FILENAME_BASE
                        ファイルの名前の先頭指定（無指定ならOUT)
  -d TARGET_DIRECTORY, --target_directory TARGET_DIRECTORY
                        対象ファイルがあるディレクトリ（無指定なら./)
  -c START_CHAPTER_NUMBER, --start_chapter_number START_CHAPTER_NUMBER
                        処理スタートする章
```


## ファイルの説明
<dl>
  <dt>voicevox_client.py</dt> <dd>プログラム本体</dd>
  <dt>startNEMOengine.sh </dt> <dd>VOICEVOX NEMO engine起動スクリプト</dd>
  <dt>startVOICEVOXengine.sh </dt> <dd>VOICEVOX NEMO engine起動スクリプト</dd>
  <dt>tourokuEx.sh</dt> <dd>辞書登録の例</dd>
  <dt>youtubeyou.txt</dt> <dd>テスト用のテキストファイル</dd>
  <dt>atokaraPlay.py</dt> <dd>生成したwav,txtファイルを表示しながら再生するプログラム</dd>
  <dt>LICENSE</dt> <dd>ライセンス情報</dd>
  <dt>README.md</dt> <dd>このファイル</dd>
  <dt>myjisyo.dat</dt> <dd>辞書ファイル</dd>
  <dt>tourokuEx.sh</dt> <dd>辞書ファイル情報を登録</dd>
  <dt>myparser.py</dt> <dd>簡易言語のパーサー</dd>
  <dt>voicevox_grammer.lark</dt> <dd>パーサーの文法ファイル</dd>
  <dt>atokaraPlayV2.py</dt> <dd>パーサーが出力したファイルの再生用。章毎に入力待ちになる</dd>
  <dt>checkSpeakers.py</dt> <dd>jsonファイルを調べて、使われてるSpeakerの名前を表示。クレジット用の文字列も生成</dd>
  <dt></dt> <dd></dd>
</dl>

## ライセンス
[MIT](https://opensource.org/license/mit/ "MIT")

## 説明動画
* 再生リスト https://www.youtube.com/playlist?list=PLAR5qAGp9riaTRKPUpIR3b_o9cWzoN-Wq
* https://youtu.be/c7LvNuyR3oM
* https://youtu.be/0yDiLfworwI
* https://youtu.be/zl3fhRXDbe8
* https://youtu.be/iFPUaPtS8HY
* https://youtu.be/BAEtagyduYw
* https://youtu.be/OyITv7kE0pU
* https://youtu.be/mD6DHtRmCe8
* https://youtu.be/2ZgiKuvd1jY

## 関連サイト
* 私のYoutubeチャンネル https://www.youtube.com/channel/UCNko_uhYtoTowASAuOam17w
*  [VOICEVOX engine](https://github.com/VOICEVOX/voicevox_engine/tree/master) 
*  [VOICEVOX engineのDocker images](https://hub.docker.com/r/voicevox/voicevox_engine) 
*  [VOICEVOX NEMO engine](https://github.com/VOICEVOX/voicevox_nemo_engine) 
*  [VOICEVOX engineのDocker images](https://hub.docker.com/r/voicevox/voicevox_nemo_engine) 
*  [VOICEVOX](https://voicevox.hiroshiba.jp/) 
*  [VOICEVOX NEMO](https://voicevox.hiroshiba.jp/nemo/) 
*  [VOICEVOX WEB](https://www.voicevox.su-shiki.com/) 
