from lark import Lark, v_args
from lark import Transformer
#import subprocess
#import time
import voicevox_client
import json
import sys

import lark

@v_args(inline=True)    # Affects the signatures of the methods
class CalculateTree(Transformer):
    def __init__(self):
        self.speaker = "女性6"
        self.speakerId = 10006
        self.enginePort = 50121
        self.engineBaseUrl = "http://127.0.0.1"
        self.type = "ノーマル"
        self.d = { 'speedScale': 1.0, 'pitchScale': 0.0, 'intonationScale': 1.0, 'volumeScale': 1.0, 'prePhonemeLength': 0.1, 'postPhonemeLength': 0.1, 'outputSamplingRate': 24000, 'outputStereo': False} 
    def endchapter(self, name, name2):
        try:
            print("Endchapter",name,name2)
        except KeyError:
            #raise Exception("Variable not found: %s" % name)
            print("Err Endchapter",name)
    def command(self, name, value):
        #list(map(lambda x:x.children[0].expandtabs(),d.children[5].children[0].children[2::2]))
        try:
            print("command",name,name2)
        except KeyError:
            #raise Exception("Variable not found: %s" % name)
            print("Err command",name)
    def readit(self, name, value):
        try:
            print("readit",name,name2)
        except KeyError:
            #raise Exception("Variable not found: %s" % name)
            print("Err readit",name)
    def comment(self, name, value):
        try:
            print("comment",name,name2)
        except KeyError:
            #raise Exception("Variable not found: %s" % name)
            print("Err comment",name)

class MySpeaker:
    def __init__(self,i=1):
        self.engs=[voicevox_client.Voicevox_client("http://127.0.0.1:50021"), voicevox_client.Voicevox_client("http://127.0.0.1:50121")]
        self.i=i
    def xi(self):
        return (self.i+1)%2
    def setSpeakerWithName(self,name):
        if self.engs[self.i].isEnableSpeakerName(name):
            self.engs[self.i].setSpeakerWithName(name)
        elif  self.engs[self.xi()].isEnableSpeakerName(name):
            self.i=self.xi()
            self.engs[self.i].setSpeakerWithName(name)
        else:
            print("話者を",name,"に設定不可能")
            sys.exit(1)
    def setSpeakerWithNameType(self,name,_type):
        if self.engs[self.i].isEnableSpeaker(name,_type):
            self.engs[self.i].setSpeakerWithNameType(name,_type)
        elif self.engs[self.xi()].isEnableSpeaker(name,_type):
            self.engs[self.xi()].setSpeakerWithNameType(name,_type)
            self.i=self.xi()
        else:
            print("話者を",name,_type,"に設定不可能")
            sys.exit(1)
    def setSpeakerWithID(self,_id):
        print("***setSpeakerWithID",_id)
        if self.engs[self.i].isEnableSpeakerID(_id):
            print("***setSpeakerWithID 1",_id)
            self.engs[self.i].setSpeakerWithID(_id)
        elif self.engs[self.xi()].isEnableSpeakerID(_id):
            print("***setSpeakerWithID 2",_id)
            self.engs[self.xi()].setSpeakerWithID(_id)
            self.i=self.xi()
        else:
            print("話者を",_id,"に設定不可能")
            sys.exit(1)
    def writeb(self,filename):
        self.engs[self.i].writeb(filename,self.engs[self.i].d)
    def play(self):
        self.engs[self.i].play()
    def getId(self):
        return self.engs[self.i].speaker
    def getName(self):
        return self.engs[self.i].dic2[ self.engs[self.i].speaker][0]
    def getType(self):
        return self.engs[self.i].dic2[ self.engs[self.i].speaker][1]
    def isEnableSpeakerName(self,name):
        return self.engs[0].isEnableSpeakerName(name) | self.engs[1].isEnableSpeakerName(name) 
    def isEnableSpeakerNameType(self,name,_type):
        return self.engs[0].isEnableSpeaker(name,_type) | self.engs[1].isEnableSpeaker(name,_type) 
    def isEnableSpeakerID(self,_id):
        return self.engs[0].isEnableSpeakerID(_id) | self.engs[1].isEnableSpeakerID(_id) 
    def audio_query(self,text):
        return self.engs[self.i].audio_query(text)
    def synthesis(self):
        return self.engs[self.i].synthesis()
    def changeConf(self,x,y="女声6"):
        name=""
        _type=""
        for i in x:
            j=i.split(":")
            if len(j)>=2:
                k={j[0]:j[1]}
                print(k)
                if j[0]=="話者":
                    name=j[1]
                elif j[0]=="タイプ":
                    _type=j[1]
                else:
                    self.engs[0].changeConf(k)
                    self.engs[1].changeConf(k)
        print("changeConf",name,_type)
        if name!="":
            if _type!="":
                self.setSpeakerWithNameType(name,_type)
            else:
                self.setSpeakerWithName(name)
        else: 
            if _type!="":
                self.setSpeakerWithNameType(y,_type)
    def printInfo(self):
        print("MyspeakerInfo:",self.i)
        self.engs[0].printInfo()
        self.engs[1].printInfo()
    def set(self, d={ 'speedScale': 1.0, 'pitchScale': 0.0, 'intonationScale': 1.0, 'volumeScale': 1.0, 'prePhonemeLength': 0.1, 'postPhonemeLength': 0.1, 'outputSamplingRate': 24000, 'outputStereo': False} ):
        self.engs[self.i].set(d)



class MyDirector:
    def __init__(self, output_filename_base="OUT", enable_output_file=True, overwritemode=False, disable_playwith=False, freq=24000):
        self.output_filename_base=output_filename_base
        self.enable_output_file=enable_output_file
        self.overwritemode=overwritemode
        self.disable_playwith=disable_playwith
        self.freq=freq
        self.defaultConf = { 'speedScale': 1.0, 'pitchScale': 0.0, 'intonationScale': 1.0, 'volumeScale': 1.0, 'prePhonemeLength': 0.1, 'postPhonemeLength': 0.1, 'outputSamplingRate': 24000, 'outputStereo': False} 

        self.xconf=[]
        self.c_speaker=MySpeaker()
        self.sbank={}
        self.counter=1
        self.chapter=1
        self.print=""
        self.printz=""
    def write(self,text,sp,spname="self.c_speaker"):
        ofilenamebase="%s_%03d_%05d" % (self.output_filename_base,self.chapter,self.counter)
        #print("****write",ofilenamebase,text,self.enable_output_file,self.overwritemode)
        if self.enable_output_file:
            print("enable output")
            if self.overwritemode or (not os.path.isfile(ofilenamebase+".wav")):
                print("write wav")
                sp.writeb(ofilenamebase+".wav")
            else:
                print(ofilenamebase+".wav が存在していて上書きしません。終了します。上書きするなら-fオプションをつけて再度実行してください")
                sys.exit(1)
            if self.overwritemode or (not os.path.isfile(ofilenamebase+".txt")):
                print("write txt")
                with open(ofilenamebase+".txt","w") as f:
                    f.write(text)
            else:
                print(ofilename+".txt が存在していて上書きしません。終了します。上書きするなら-fオプションをつけて再度実行してください")
                sys.exit(1)
            if self.overwritemode or (not os.path.isfile(ofilenamebase+".json")):
                print("write json")
                data={"chapter":self.chapter, "counter":self.counter, "txt":text, "spname":spname, "id":sp.getId(), "name":sp.getName(), "type":sp.getType(), "conf":sp.engs[sp.i].conf, "ofilenamebase":ofilenamebase, "xset":self.xconf,"print":self.print,"printz":self.printz}
                with open(ofilenamebase+".json","w") as f:
                    f.write(str(data))
                self.xconf=[]
                self.print=""
                self.printz=""
            else:
                print(ofilename+".json が存在していて上書きしません。終了します。上書きするなら-fオプションをつけて再度実行してください")
                sys.exit(1)
            self.counter=self.counter+1
    def run_instruction(self,t):
        # 各種命令
        if t.data == 'command':
            print(t.data,t.children)
            c=t.children[0].children[0].expandtabs()
            args=list(map(lambda x:x.children[0].expandtabs(), t.children[0].children[2::2]))
            #print(t.data,c,args)
            #print()
            # 話者指定
            if c == "setSpeakerWithName":
                print("**setSpeakerWithName")
                if self.c_speaker.isEnableSpeakerName(args[0]):
                    self.c_speaker.setSpeakerWithName(args[0])
            # 話者指定
            elif c == "setSpeakerWithNameType":
                print("**setSpeakerWithNameType")
                if self.c_speaker.isEnableSpeakerNameType(args[0],args[1]):
                    self.c_speaker.setSpeakerWithNameType(args[0],args[1])
            # 話者指定
            elif c == "setSpeakerWithID":
                print("**setSpeakerWithID")
                if self.c_speaker.isEnableSpeakerID(args[0]):
                    self.c_speaker.setSpeakerWithID(args[0])
            # 各種設定
            elif c == "setDefaultConf":
                print("**setDefaultConf")
                print(c,args[0])
                self.defaultConf=args[1:].deepcopy()
            # 各種設定を初期値に
            elif c == "resetConf":
                print("**resetConf")
                self.c_speaker.resetConf()
            # 短縮名設定 set 登録したい名前 設定情報 ex set _x 話速:1.4 抑揚:0.5
            elif c == "set":
                print("**set")
                print(c,args[0])
                self.sbank[args[0]]=MySpeaker()
                self.sbank[args[0]].changeConf(args[1:])
            # 登録したものの設定変更 change 登録名 設定情報
            elif c == "change":
                print("**change")
                print(c,args[0])
                self.sbank[args[0]].changeConf(args[1:])
            # デフォルト話者の設定変更 change 設定情報
            elif c == "Cchange":
                print("**Cchange")
                print(c,args)
                self.c_speaker.changeConf(args)
            # エキストラオプション設定(背景とか自動操作とか再生する時に活用する用)
            elif c == "setX":
                print("**setX")
                print(c,args)
                self.xconf=args.deepcopy()
            # 新しい章
            elif c == 'newChapter':
                print("**newChapter")
                self.counter=1
                self.chapter+=1
            # 再生時に１行表示 (再生前
            elif c == 'print':
                print("**print")
                self.print=" ".join(args)
            # 再生時に１行表示 (再生後
            elif c == 'printz':
                print("**printz")
                self.printz=" ".join(args)
            # 話者情報表示
            elif c == 'list':
                print("**list")
                self.c_speaker.printInfo()
                for k in self.sbank.keys():
                    self.sbank[k].printInfo()
            else:
                raise SyntaxError('Unknown instruction: %s' % c)
                print()
        # 読む
        elif t.data == 'readit':
            print(t.data,t.children)
            tmp=t.children[0].children[0].expandtabs()
            print(1,tmp)
            self.c_speaker.audio_query(tmp)
            self.c_speaker.set(self.c_speaker.engs[self.c_speaker.i].conf)
            self.c_speaker.synthesis()
            if not self.disable_playwith:
                self.c_speaker.play()
            self.write(tmp,self.c_speaker)
            print()
        # 人物指定で読む
        elif t.data == 'xreadit':
            print(t.data,t.children)
            tmpsp=t.children[0].children[0].expandtabs()
            tmpspc=list(map(lambda x: x.children[0].expandtabs(), t.children[0].children[2::2]))
            tmp=t.children[1].children[0].expandtabs()
            print("話者",tmpsp)
            print("話者データ",tmpspc)
            print("話す文書",tmp)
            if tmpsp in self.sbank.keys():
                self.sbank[tmpsp].audio_query(tmp)
                self.sbank[tmpsp].set(self.sbank[tmpsp].engs[self.sbank[tmpsp].i].conf)
                self.sbank[tmpsp].synthesis()
                if not self.disable_playwith:
                    self.sbank[tmpsp].play()
                self.write(tmp,self.sbank[tmpsp],tmpsp)
            else:
                raise RuntimeError("%sは話者として登録されてません" % tmpsp)
            print()
        # コメント
        elif t.data == 'comment':
            print(t.data,t.children)
            print()
        # 将来実装するかも
        elif t.data == 'system':
            #print(t.data,t.children)
            c=t.children[0].children[0].expandtabs()
            args=list(map(lambda x:x.children[0].expandtabs(), t.children[0].children[2::2]))
            #print(t.data,[c]+args)
            #print()
            #result = subprocess.run( [c]+args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            #print(result)
        # 将来実装するかも
        elif t.data == 'sleep':
            print(t.data,t.children)
            print()
            #time.sleep(int(children[0].expandtabs()))
        else:
            raise SyntaxError('Unknown instruction: %s' % t.data)
            print()
            #elif t.data == 'readit':
            #elif t.data == 'comment':
            #    else:


def test():
    #x=lark.Lark(grammer,parser='lalr', transformer=CalculateTree())
    #x=lark.Lark(grammer,parser='lalr')
    grammer =""
    with open("voicevox_grammer.lark", 'r') as f:
        grammer=f.read()
    test=""
    with open("test.vv", 'r') as f:
        test=f.read()
    x=lark.Lark(grammer)
    #print("*******************************start parse")
    d=x.parse(test)
    print(d.pretty())

    for inst in d.children:
        run_instruction(inst)

md=MyDirector()
d=None
if __name__ == "__main__":
    import argparse
    import sys
    import os
    import re
    parser = argparse.ArgumentParser(description="VOicevox client: VOICEVOXエンジンを利用して音声合成する簡易言語(先にVOICEVOXエンジンを動かす必要あり)", epilog="")
    parser.add_argument("-i","--input_filename", help="ソースファイル", required=True)
    parser.add_argument("-o","--output_filename_base", default="", help="出力ファイルの名前の先頭指定（無指定でiオプション使ってなければOUT、iオプション使ってるなら入力ファイル名のbaseに_を追加した文字列)")
    parser.add_argument("-w","--enable_output_file", action="store_true", help="ファイル出力するモード")
    parser.add_argument("-f","--overwritemode", action="store_true", help="出力ファイルを上書きモード")
    parser.add_argument("--outputSamplingRate", type=int, default=24000, help="outputSamplingRate 出力周波数(デフォルト24000)")
    parser.add_argument("--outputStereo", action="store_true", help="outputStereo ステレオにする？（デフォルトはfalse)")
    args = parser.parse_args()
    setting={ 'outputSamplingRate': args.outputSamplingRate, 'outputStereo': args.outputStereo}
    grammer =""
    with open("voicevox_grammer.lark", 'r') as f:
        grammer=f.read()
    x=lark.Lark(grammer)
    with open(args.input_filename, 'r') as f:
        source=f.read()
        #-- 全角空白は半角空白にしてから行前後の空白除去。最後の行の後に改行追加
        source=re.sub('　',' ',source)
        source=re.sub(r' +',' ',source)
        tmp=re.split('\n',source)
        tmp=list(map(lambda x: x.strip(), tmp ))
        source="\n".join(tmp)+"\n"
        #-- 全角空白は半角空白にしてから行前後の空白除去。最後の行の後に改行追加
        d=x.parse(source)
        print(d.pretty())
        chapter=1
        output_filename_base=os.path.join(os.path.dirname(args.input_filename),os.path.splitext(os.path.basename(args.input_filename))[0])
        md=MyDirector(output_filename_base, args.enable_output_file, args.overwritemode)
        print("###",chapter,output_filename_base)
        for inst in d.children:
            md.run_instruction(inst)
