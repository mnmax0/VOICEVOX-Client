#!/bin/bash
T="myjisyo.dat"
P=50121
if [ $# == 2 ]
then
	P=$1
	T=$2
else
	if [ $# == 1 ]
	then
		P=$1
	else
		if [ $# != 0 ]
		then
			echo "使い方：引数はエンジンのポート番号 辞書ファイル名 ex ./$0 50021 my.dat"
			echo "あるいは 引数は、登録したいエンジンのポート番号。　ex ./$0 50021"
			echo "引数を省略したらmyjisyo.datの内容を50121ポートのエンジンに登録"
			exit 1
		fi
	fi
fi

echo "ポート番号:$P 辞書ファイル:$T"

function t() {
	echo ">>$1:$2<<"
	python3 voicevox_client.py -r "$2" -p $1
}

cat $T | while read X
do
	#echo ">>$X:$P"
	t $P $X
done
