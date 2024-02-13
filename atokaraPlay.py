if __name__ == "__main__":
    import argparse
    import sys
    import os
    import re
    import voicevox_client
    parser = argparse.ArgumentParser(description="voicevox_client.pyで生成したwavとtxtファイルを順に再生", epilog="")
    parser.add_argument("-b","--filename_base", default="OUT", help="ファイルの名前の先頭指定（無指定ならOUT)")
    parser.add_argument("-d","--target_directory", default="./", help="対象ファイルがあるディレクトリ（無指定なら./)")
    args = parser.parse_args()
    files = os.listdir(args.target_directory)
    files.sort()
    target = [x for x in files if re.match("^"+args.filename_base+"_" , x)]
    wavs = [x for x in target if re.match(".*\.wav$" , x)]
    txts = [x for x in target if re.match(".*\.txt$" , x)]
    #print(target)
    #print(wavs)
    #print(txts)
    for i, t in enumerate(txts):
        tt=args.target_directory+"/"+t
        ww=args.target_directory+"/"+wavs[i]
        with open(tt,"r") as f:
            print(f.read())
        voicevox_client.playWaveFile(ww)
