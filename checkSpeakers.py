if __name__ == "__main__":
    import argparse
    import sys
    import os
    import re
    import json
    import voicevox_client
    import ast
    from pprint import pprint
    parser = argparse.ArgumentParser(description="myparse.pyで生成したjsonファイルを確認して、使ったSpeakerのリストを表示", epilog="")
    parser.add_argument("-b","--filename_base", default="OUT", help="ファイルの名前の先頭指定（無指定ならOUT)")
    parser.add_argument("-d","--target_directory", default="./", help="対象ファイルがあるディレクトリ（無指定なら./)")
    parser.add_argument("-c","--start_chapter_number", type=int, default=1, help="処理スタートする章")
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
    #pchapter=0
    mylist={}
    for i, t in enumerate(jsons):
        tt=args.target_directory+"/"+t
        with open(tt,"r") as f:
            d=ast.literal_eval(f.read())
            cchapter=d["chapter"]
            txt=d["txt"]
            name=d["name"]
            _type=d["type"]
            mylist[name]=""
            print("%s(%s),%s" % (name,_type,txt))
    print(mylist)
    pprint(mylist.keys())
    nemoflag=False
    for i in mylist.keys():
        if re.match(r'^(女|男)声[0-9]+$',i):
            nemoflag=True
        else:
            print("「VOICEVOX %s」" % i)
    if nemoflag:
            print("「VOICEVOX %s」" % "NEMO")
