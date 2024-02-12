import urllib.request
import json
#import subprocess
import wave
import pyaudio
import io

class Voicevox_client:
    def __init__(self, burl='http://127.0.0.1:50121', speaker=10006):
        # Voicevox engine URL 
        self.burl = burl            
        # speaker id
        self.speaker = speaker
        # audio_queryの保持用
        self.qd = json.loads(json.dumps({ 'speedScale': 1.0, 'pitchScale': 0.0, 'intonationScale': 1.0, 'volumeScale': 1.0, 'prePhonemeLength': 0.1, 'postPhonemeLength': 0.1, 'outputSamplingRate': 24000, 'outputStereo': False }))
        # 合成したwavデータ保存用
        self.d = None
        # スピーカーの一覧を得る
    def speakers(self):
        with urllib.request.urlopen(self.burl+'/speakers') as response:
            return response.read()
        # ユーザー辞書の一覧を得る
    def userdict(self):
        with urllib.request.urlopen(self.burl+'/user_dict') as response:
            return response.read()
        # バージョンを得る
    def version(self):
        with urllib.request.urlopen(self.burl+'/version') as response:
            return response.read()
        # jsonを整形して返す
    def dumps(self,data,indent=2):
        d = json.loads(data.decode('utf-8'))
        return json.dumps(d, indent=indent, ensure_ascii=False)
        # audio_query用内部関数
    def baudio_query(self, speaker, text):
        url = '{}?{}'.format( self.burl+'/audio_query', urllib.parse.urlencode({'speaker':speaker,'text':text}))
        request = urllib.request.Request(url, method="POST")
        with urllib.request.urlopen(request) as response:
            self.qd = response.read()
            return self.qd
        # audio_queryを実行
    def audio_query(self, text):
        return self.baudio_query(self.speaker,text)
        # audio_queryの結果を変更用（話速、ピッチ等)
    def set(self, d={ 'speedScale': 1.0, 'pitchScale': 0.0, 'intonationScale': 1.0, 'volumeScale': 1.0, 'prePhonemeLength': 0.1, 'postPhonemeLength': 0.1, 'outputSamplingRate': 24000, 'outputStereo': False} ):
        #print(d)
        tmpqd=json.loads(self.qd)
        for k,v in d.items():
            #print(">")
            #print(k,v)
            #print("<")
            if tmpqd[k]!=v :
                #print(">>",k,v)
                #print( tmpqd[k] )
                tmpqd[k]=v
                #print( tmpqd[k] )
                #print("<<")
                self.qd=json.dumps(tmpqd).encode('UTF-8')
        # 音声合成用メソッド（内部で利用）
    def bsynthesis(self, speaker, data, enable_interrogative_upspeak=True):
        url2 = '{}?{}'.format( self.burl+'/synthesis', urllib.parse.urlencode({'speaker':speaker,'enable_interrogative_upspeak':enable_interrogative_upspeak}))
        headers = {"Content-Type" : "application/json"}
        request = urllib.request.Request(url2, data=data, method="POST", headers=headers)
        with urllib.request.urlopen(request) as response2:
            return response2.read()
        # audio_queryの保持データを用いて、音声合成して、dメンバ変数に結果を保持
    def synthesis(self, enable_interrogative_upspeak=True):
        self.d=self.bsynthesis(self.speaker,self.qd,enable_interrogative_upspeak)
        # ファイル出力用関数
    def writeb(self, fname, data):
        with open(fname, 'wb') as f:
            f.write(data) 
    def play(self):
        playWavBinary(self.d)
    def wordRegistration(self, surface, pronunciation, accent_type="1"):
        url = '{}?{}'.format( self.burl+'/user_dict_word', urllib.parse.urlencode({'surface':surface,'pronunciation':pronunciation,'accent_type':accent_type}))
        print(url)
        request = urllib.request.Request(url, method="POST")
        with urllib.request.urlopen(request) as response:
            self.qd = response.read()
            return self.qd
    def delelteWordRegistration(self, word_uuid):
        url = '{}/{}'.format( self.burl+'/user_dict_word', word_uuid)
        print(url)
        request = urllib.request.Request(url, data={}, method='DELETE' )
        with urllib.request.urlopen(request) as response:
            self.qd = response.read()
            return self.qd


# デバッグ用テスト関数
def test01():
    #speaker=1
    #burl='http://127.0.0.1:50021'
    burl='http://127.0.0.1:50121'
    speaker=10006
    c=Voicevox_client(burl,speaker)
    print(c.dumps(c.speakers(),5))
    print(c.version())
    c.audio_query("はじめまして")
    #     { 'speedScale': 1.0, 'pitchScale':  0.0, 'intonationScale':  1.0, 'volumeScale': 1.0, 'prePhonemeLength': 0.1, 'postPhonemeLength': 0.1, 'outputSamplingRate': 24000, 'outputStereo': False}
    c.set({ 'speedScale': 1.5, 'pitchScale': 0.05, 'intonationScale': 0.75, 'volumeScale': 1.0, 'prePhonemeLength': 0.1, 'postPhonemeLength': 0.1, 'outputSamplingRate': 24000, 'outputStereo': False} )
    #c.set({ 'speedScale': 1.5, 'pitchScale': -0.05, 'intonationScale': 0.5, 'volumeScale': 1.0, 'prePhonemeLength': 0.1, 'postPhonemeLength': 0.1, 'outputSamplingRate': 24000, 'outputStereo': False} )
    c.synthesis()
    c.writeb("11.wav",c.d)
    #result = subprocess.run( ["mpv", "11.wav"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    playWaveFile("11.wav")
    print(result.returncode) 
    print(result.stdout) 

def mySynthesis(url,port,speakerid,text,setting):
    url2=url+":"+port
    c=Voicevox_client(url2,speakerid)
    c.audio_query(text)
    c.set(setting)
    c.synthesis()
    return c

def playWaveFile(wavefilename,CHUNK = 1024):
    with wave.open(wavefilename, 'rb') as wf:
        # Instantiate PyAudio and initialize PortAudio system resources (1)
        p = pyaudio.PyAudio()

        # Open stream (2)
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # Play samples from the wave file (3)
        while len(data := wf.readframes(CHUNK)):  # Requires Python 3.8+ for :=
            stream.write(data)

        # Close stream (4)
        stream.close()

        # Release PortAudio system resources (5)
        p.terminate()

def playWavBinary(wavefiledata):
    buffer=io.BytesIO(wavefiledata)
    playWaveFile(buffer)

if __name__ == "__main__":
    #test01()
    #  python3.11 voicevox_client.py -i test.txt  2> /dev/null  ファイルのテキストを１行ずつ読み上げ
    #  python3.11 voicevox_client.py -s 10006 -i test.txt --speedScale 1.5 --pitchScale 0.05 --intonationScale 0.75           発音のみ
    #  python3.11 voicevox_client.py -s 10006 -i test.txt --speedScale 1.5 --pitchScale 0.05 --intonationScale 0.75 -w        ファイルに書き出す(上書きしない)
    #  python3.11 voicevox_client.py -s 10006 -i test.txt --speedScale 1.5 --pitchScale 0.05 --intonationScale 0.75 -w -f     上書きで書き出す
    #  python3.11 voicevox_client.py -s 10006 -i test.txt --speedScale 1.5 --pitchScale 0.05 --intonationScale 0.75 -w -f -x  上書きで書き出す、音声なし
    #  python3.11 voicevox_client.py -s 10006 -t "こんにちは" -i test.txt -w -f --speedScale 1.5 --pitchScale 0.05 --intonationScale 0.75  連番でファイル書き出し
    #  python3.11 voicevox_client.py -s 10006 -t "こんにちは" -i test.txt -w -f --speedScale 1.5 --pitchScale 0.05 --intonationScale 0.75  連番でファイル書き出し
    #  python3.11 voicevox_client.py -i youtubeyou.txt -v 1.4 2> /dev/null 
    #  python3.11 voicevox_client.py -r "Python||パイソン||1"   #辞書登録
    #  python3.11 voicevox_client.py -d "30ce92f9-7338-4f31-ad28-8d1207c69368" #辞書削除

    import argparse
    import sys
    import os
    import re
    #parser = argparse.ArgumentParser(description='VOicevox client', epilog='--textも--input_filenameオプションもない場合、標準入力の文書を合成')
    parser = argparse.ArgumentParser(description="VOicevox client: VOICEVOXエンジンを利用して音声合成するツール(先にVOICEVOXエンジンを動かす必要あり)", epilog="VOICEVOX engineなら\ndocker run --rm -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-latest\nVOICEVOX NEMO engineなら\ndocker run --rm --gpus all -p '127.0.0.1:50121:50121' voicevox/voicevox_nemo_engine:cpu-ubuntu20.04-latest\n")
    parser.add_argument("-t","--text", default=None, help="音声合成する文書")
    parser.add_argument("-i","--input_filename", default=None, help="音声合成する文書ファイル指定")
    parser.add_argument("-u", "--url", default="http://127.0.0.1", help="VoicevoxエンジンのURL")
    parser.add_argument("-p","--port", default="50121", help="Voicevoxエンジンのポート")
    parser.add_argument("-s","--speakerid",  type=int, default=10006, help="スピーカーのID")
    parser.add_argument("-l","--listspeakers",  action="store_true", help="そのエンジンのバージョン、利用可能なspeakers(json形式),ユーザー辞書(json形式)の情報出力")
    parser.add_argument("-o","--output_filename_base", default="OUT", help="出力ファイルの名前の先頭指定（無指定ならOUT)")
    parser.add_argument("-w","--enable_output_file", action="store_true", help="ファイル出力するモード")
    parser.add_argument("-x","--disable_playwith", action="store_true", help="音声出力しないモード")
    parser.add_argument("-f","--overwritemode", action="store_true", help="出力ファイルを上書きモード")
    parser.add_argument("-d","--delelteWordRegistration", default="", help="登録IDの辞書登録単語を消す")
    parser.add_argument("-r","--wordRegistration", default=[], help="辞書登録、||区切りで　登録単語||発音||アクセントタイプ 登録単語||発音にするとアクセントタイプは１で登録 ex. Python||パイソン||1 とか Python||パイソン")
    parser.add_argument("-v","--speedScale", type=float, default=1.0, help="speedScale 話速(デフォルト1)")
    parser.add_argument("--pitchScale", type=float, default=0.0, help="pitchScale ピッチ(デフォルト0)")
    parser.add_argument("--intonationScale", type=float, default=1.0, help="intonationScale 抑揚(デフォルト1)")
    parser.add_argument("--volumeScale", type=float, default=1.0, help="volumeScale ボリューム(デフォルト1)")
    parser.add_argument("--prePhonemeLength", type=float, default=0.1, help="prePhonemeLength 前の長さ(デフォルト0.1)")
    parser.add_argument("--postPhonemeLength", type=float, default=0.1, help="postPhonemeLength 後ろの長さ(デフォルト0.1)")
    parser.add_argument("--outputSamplingRate", type=int, default=24000, help="outputSamplingRate 出力周波数(デフォルト24000)")
    parser.add_argument("--outputStereo", action="store_true", help="outputStereo ステレオにする？（デフォルトはfalse)")
    args = parser.parse_args()
    url=args.url+":"+args.port
    setting={ 'speedScale': args.speedScale, 'pitchScale': args.pitchScale, 'intonationScale': args.intonationScale, 'volumeScale': args.volumeScale, 'prePhonemeLength': args.prePhonemeLength, 'postPhonemeLength': args.postPhonemeLength, 'outputSamplingRate': args.outputSamplingRate, 'outputStereo': args.outputStereo}
    #print(url)
    target=[]
    url2=args.url+":"+args.port
    if args.listspeakers:
        c=Voicevox_client(url2,args.speakerid)
        print("エンジンのバージョン", c.version())
        print("******************* 利用可能なSpeakers")
        print(c.dumps(c.speakers(),5))
        print("******************* ユーザー辞書")
        print(c.dumps(c.userdict(),5))
    if args.text is not None:
        target.append(args.text)
    if args.input_filename is not None:
        with open(args.input_filename, 'r') as f:
            for line in f:
                target.append(line)
    if args.delelteWordRegistration!="":
        c=Voicevox_client(url2,args.speakerid)
        c.delelteWordRegistration(args.delelteWordRegistration)
    if len(args.wordRegistration)!=0:
        tmp_wr=re.split(r"\|\|",args.wordRegistration)
        c=Voicevox_client(url2,args.speakerid)
        print(args.wordRegistration,len(args.wordRegistration))
        if( len(tmp_wr)>2 ):
            c.wordRegistration(tmp_wr[0],tmp_wr[1],tmp_wr[2])
        else:
            c.wordRegistration(tmp_wr[0],tmp_wr[1])
    for i, ttext in enumerate(target):
        print(i,target[i])
        if ttext != "":
            c=mySynthesis(args.url,args.port,args.speakerid,ttext,setting)
            ofilename="%s_%05d.wav" % (args.output_filename_base,i)
            if args.enable_output_file: 
                if args.overwritemode or (not os.path.isfile(ofilename)):
                    c.writeb(ofilename,c.d)
                    #sys.stdout.buffer.write(c.d)
                else:
                    print(ofilename+" が存在していて上書きしません。終了します。上書きするなら-zオプションをつけて再度実行してください")
                    exit(1)
            if not args.disable_playwith:
                #playWavBinary(c.d)
                c.play()
