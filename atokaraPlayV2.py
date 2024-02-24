if __name__ == "__main__":
    import argparse
    import sys
    import os
    import re
    import json
    import voicevox_client
    import ast
    from pprint import pprint
    parser = argparse.ArgumentParser(description="myparse.pyで生成したwavとtxtファイルを順に再生 章毎に入力待ちに", epilog="")
    parser.add_argument("-b","--filename_base", default="OUT", help="ファイルの名前の先頭指定（無指定ならOUT)")
    parser.add_argument("-d","--target_directory", default="./", help="対象ファイルがあるディレクトリ（無指定なら./)")
    parser.add_argument("-c","--start_chapter_number", type=int, default=1, help="対象ファイルがあるディレクトリ（無指定なら./)")
    args = parser.parse_args()
    files = os.listdir(args.target_directory)
    files.sort()
    #print(files)
    target = [x for x in files if re.match("^"+args.filename_base+"_" , x)]
    #print(target)
    wavs = [x for x in target if re.match(".*\.wav$" , x)]
    txts = [x for x in target if re.match(".*\.txt$" , x)]
    jsons = [x for x in target if re.match(".*\.json$" , x)]
    #print(jsons)
    #print(target)
    #print(wavs)
    #print(txts)
    pchapter=0
    for i, t in enumerate(jsons):
        tt=args.target_directory+"/"+t
        with open(tt,"r") as f:
            d=ast.literal_eval(f.read())
            cchapter=d["chapter"]
            txt=d["txt"]
            printTxt=d["print"]
            printzTxt=d["printz"]
            if cchapter>=args.start_chapter_number:
                if pchapter!=cchapter:
                    print("***HitEnter***")
                    val=input()
                #print("****************",i)
                #pprint(d)
                if len(printTxt)>0:
                    print(printTxt)
                print(txt)
                fname=args.target_directory+"/"+os.path.basename(d["ofilenamebase"])+".wav"
                voicevox_client.playWaveFile(fname)
                if len(printzTxt)>0:
                    print(printzTxt)
            pchapter=cchapter

