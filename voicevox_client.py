import urllib.request
import json
#import subprocess
import wave
import pyaudio
import io
from pprint import pprint
import sys

class Voicevox_client:
    def __init__(self, burl='http://127.0.0.1:50121', speaker=10006):
        # Voicevox engine URL 
        self.burl = burl            
        # speaker id
        self.speaker = int(speaker)
        # audio_queryの保持用
        self.qd = json.loads(json.dumps({}))
        # 設定ファイル
        self.conf = json.loads(json.dumps({ 'speedScale': 1.0, 'pitchScale': 0.0, 'intonationScale': 1.0, 'volumeScale': 1.0, 'prePhonemeLength': 0.1, 'postPhonemeLength': 0.1, 'outputSamplingRate': 24000, 'outputStereo': False }))
        # 合成したwavデータ保存用
        self.d = None
        # スピーカーの表用
        self.dic1 = {}
        self.dic2 = {}
        # スピーカーの逆引き用
        self.rdic1 = {}
        self.rdic2 = {}
        self.mkdic()
        #print(type(self.speaker),self.speaker)
        if self.speaker not in self.dic2.keys():
            self.speaker=min(self.dic2.keys())
            print(speaker,"はこのVOICEVOXエンジンでは使えないので",self.speaker,"を話者idとして設定しました")
            #print(self.dic2.keys())
        # スピーカーの一覧を得る
    def speakers(self):
        with urllib.request.urlopen(self.burl+'/speakers') as response:
            return response.read()
        # 名前で話者を変更,タイプは前のタイプを継承
    def isEnableSpeaker(self,name,_type="ノーマル"):
        return (name,_type) in self.rdic2.keys()
    def isEnableSpeakerName(self,name):
        return name in self.rdic1.keys()
    def isEnableSpeakerID(self,_id):
        return int(_id) in self.dic2.keys()
    def setSpeakerWithName(self,name):
        if name in self.rdic1.keys():
            ctype=self.dic2[self.speaker][1]
            self.setSpeakerWithNameType(name,ctype)
        else:
            print(name,"はこのVOICEVOXエンジンでは使えません")
            print("利用可能な一覧")
            pprint(self.rdic1.keys())
            sys.exit(1)
        # 名前とタイプで話者を変更
    def setSpeakerWithNameType(self,name,_type):
        if (name,_type) in self.rdic2.keys():
            self.speaker=self.rdic2[(name,_type)]
        else:
            print((name,_type),"はこのVOICEVOXエンジンでは使えません")
            print("利用可能な一覧")
            pprint(self.rdic2.keys())
            sys.exit(1)
        # ユーザー辞書の一覧を得る
        # ユーザー辞書の一覧を得る
    def setSpeakerWithID(self,_id):
        if self.isEnableSpeakerID(int(_id)):
            self.speaker=int(_id)
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
    def mkdic(self):
        self.dic1={}
        self.rdic1={}
        self.dic2={}
        self.rdic2={}
        for i,d in enumerate(json.loads(self.speakers())):
            self.dic1[d["speaker_uuid"]]=d["name"]
            self.rdic1[d["name"]]=d["speaker_uuid"]
            for j in d["styles"]:
                self.dic2[j["id"]]=[d["name"],j["name"]]
                self.rdic2[d["name"],j["name"]]=j["id"]
    def printSpeakers_old(self):
        for i,d in enumerate(json.loads(self.speakers())):
            print(d["name"],",",d["speaker_uuid"])
            for j in d["styles"]:
                if "type" in j.keys():
                    print(j["id"],j["type"],j["name"])
                else:
                    print(j["id"],j["name"])
            print("\n")
    def printSpeakers(self):
        print("******** 名前,uuid ******** ")
        pprint(self.rdic1)
        print("\n")
        print("******** id,(名前、タイプ) ******** ")
        pprint(self.dic2)
        print("\n")
        print("******** (名前、タイプ),id ******** ")
        pprint(self.rdic2)
        print("\n")
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
        #print("********** voicevox_client set:",self.qd,"***************")
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
    def changeConf(self,newconf={ 'speedScale': 1.0, 'pitchScale': 0.0, 'intonationScale': 1.0, 'volumeScale': 1.0, 'prePhonemeLength': 0.1, 'postPhonemeLength': 0.1, 'outputSamplingRate': 24000, 'outputStereo': False} ):
        #print("********************* changeConf start")
        #pprint(self.conf)
        for k in newconf.keys():
            if k in self.conf.keys():
                self.conf[k]=newconf[k]
            elif k == "話速" or k == 'speedScale':
                self.conf['speedScale']=newconf[k]
            elif k == "音高" or k == 'pitchScale':
                self.conf['pitchScale']=newconf[k]
            elif k == "抑揚" or k == 'intonationScale':
                self.conf['intonationScale']=newconf[k]
            elif k == "音量" or k == 'volumeScale':
                self.conf['volumeScale']=newconf[k]
            elif k == "開始無音" or k == 'prePhonemeLength':
                self.conf['prePhonemeLength']=newconf[k]
            elif k == "終了無音" or k == 'postPhonemeLength':
                self.conf['postPhonemeLength']=newconf[k]
            else:
                raise RuntimeError("Voicevox_client changeConf ERR: %sという設定項目無い" % k)
        #pprint(self.conf)
        #print("********************* changeConf end\n\n")
    def printInfo(self):
        print("*** voicevox_client Info")
        print(self.burl,self.speaker,self.dic2[self.speaker])
        pprint(self.qd)


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
    parser = argparse.ArgumentParser(description="VOicevox client: VOICEVOXエンジンを利用して音声合成するツール(先にVOICEVOXエンジンを動かす必要あり)", epilog="VOICEVOX engineなら\ndocker run --rm -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-latest\nVOICEVOX NEMO engineなら\ndocker run --rm --gpus all -p '127.0.0.1:50121:50121' voicevox/voicevox_nemo_engine:cpu-latest\n")
    parser.add_argument("-t","--text", default=None, help="音声合成する文書")
    parser.add_argument("-i","--input_filename", default=None, help="音声合成する文書ファイル指定")
    parser.add_argument("-u", "--url", default="http://127.0.0.1", help="VoicevoxエンジンのURL")
    parser.add_argument("-p","--port", default="50121", help="Voicevoxエンジンのポート")
    parser.add_argument("-s","--speakerid",  default=10006, help="スピーカーのID or 話者の名前とタイプ。タイプを省略した場合ノーマルタイプのID ex. 10006,  女性6||ノーマル, 女性6")
    parser.add_argument("-l","--listspeakers",  action="store_true", help="そのエンジンのバージョン、利用可能なspeakers(json形式),ユーザー辞書(json形式)の情報出力")
    parser.add_argument("-o","--output_filename_base", default="", help="出力ファイルの名前の先頭指定（無指定でiオプション使ってなければOUT、iオプション使ってるなら入力ファイル名のbaseに_を追加した文字列)")
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
        c=Voicevox_client(url2)
        print("エンジンのバージョン", c.version())
        print("******************* 利用可能なSpeakers")
        print(c.dumps(c.speakers(),5))
        print("******************* 表")
        c.printSpeakers()
        print("******************* ユーザー辞書")
        print(c.dumps(c.userdict(),5))
    if args.text is not None:
        target.append(args.text)
    if args.input_filename is not None:
        with open(args.input_filename, 'r') as f:
            for line in f:
                line2=str.strip(line)
                if len(line2)!=0:
                    target.append(line2)
    if args.delelteWordRegistration!="":
        c=Voicevox_client(url2)
        c.delelteWordRegistration(args.delelteWordRegistration)
    if len(args.wordRegistration)!=0:
        tmp_wr=re.split(r"\|\|",args.wordRegistration)
        c=Voicevox_client(url2)
        print(args.wordRegistration,len(args.wordRegistration))
        if( len(tmp_wr)>2 ):
            c.wordRegistration(tmp_wr[0],tmp_wr[1],tmp_wr[2])
        else:
            c.wordRegistration(tmp_wr[0],tmp_wr[1])
    output_filename_base="OUT"
    if args.input_filename is not None:
        if args.output_filename_base == "":
            #output_filename_base=os.path.splitext(os.path.basename(args.input_filename))[0]
            output_filename_base=os.path.join(os.path.dirname(args.input_filename),os.path.splitext(os.path.basename(args.input_filename))[0])
    speakerid=args.speakerid
    tmp=Voicevox_client(url2)
    #print(tmp.rdic2.keys())
    if re.match(r'[0-9]+',str(args.speakerid)):
        tmp=Voicevox_client(url2,speakerid)
        #print(">----------------------<")
        #print(tmp.speaker,args.speakerid, tmp.speaker!=args.speakerid,"<")
        if not tmp.isEnableSpeakerID(int(args.speakerid)):
            print("ERR:",args.speakerid,"は使えません。利用可能なidは以下")
            pprint(tmp.dic2.keys())
            sys.exit(1)
        else:
            speakerid=int(args.speakerid)
    elif re.match(r'.*\|\|.*',args.speakerid):
        tmp1=re.sub(r'\|\|.*',"",args.speakerid)
        tmp2=re.sub(r'.*\|\|',"",args.speakerid)
        if (tmp1,tmp2) in tmp.rdic2.keys():
            tmp.setSpeakerWithNameType(tmp1,tmp2)
            speakerid=tmp.speaker
        else:
            print(args.speakerid,"は使えません。利用可能は以下")
            pprint(tmp.rdic2.keys())
            sys.exit(1)
    elif (args.speakerid,"ノーマル") in tmp.rdic2.keys():
            tmp.setSpeakerWithNameType(args.speakerid,"ノーマル")
            speakerid=tmp.speaker
    else:
            print([args.speakerid,"ノーマル"],"は使えません。利用可能は以下")
            pprint(tmp.rdic2.keys())
            sys.exit(1)

    if tmp.speaker != args.speakerid:
        #print(tmp.speaker,speakerid)
        speakerid=tmp.speaker
        #print("***new speakerid ***",speakerid)
    for i, ttext in enumerate(target):
        print(i,target[i])
        if ttext != "":
            c=mySynthesis(args.url,args.port,speakerid,ttext,setting)
            ofilenamebase="%s_%05d" % (output_filename_base,i)
            if args.enable_output_file: 
                if args.overwritemode or (not os.path.isfile(ofilenamebase+".wav")):
                    c.writeb(ofilenamebase+".wav",c.d)
                    #sys.stdout.buffer.write(c.d)
                else:
                    print(ofilenamebase+".wav が存在していて上書きしません。終了します。上書きするなら-fオプションをつけて再度実行してください")
                    sys.exit(1)
                if args.overwritemode or (not os.path.isfile(ofilenamebase+".txt")):
                    with open(ofilenamebase+".txt","w") as f:
                        f.write(target[i])
                else:
                    print(ofilename+".txt が存在していて上書きしません。終了します。上書きするなら-fオプションをつけて再度実行してください")
                    sys.exit(1)
            if not args.disable_playwith:
                #playWavBinary(c.d)
                c.play()
