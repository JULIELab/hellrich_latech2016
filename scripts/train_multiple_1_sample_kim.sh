#!/bin/bash
#SBATCH -p express
#SBATCH --cpus-per-task 4
WORKER=8
EPOCHS=10
HS=0
NEG=5
SAMPLE="1e-3"
_CORPUS="/data/data_hellrich/google_books_parts/sampled/fiction/"
_TARGET="/home/hellrich/tmp/latech2016/fiction_1_sample/"


function train {
	size=$1
	min=$2
	run=$3
	convergence=$4

	corpus=$_CORPUS/${size}M
	name="${size}M_${min}min_con${convergence}_run${run}"
	target=$_TARGET/${name}

	what=$(
		what=""
		cd $corpus
		for x in 18{5..9}?_* 19??_* 2*_*
		do
			what="$what $x"
		done
		echo $what
	)

	mkdir -p $target logs
	python ../python/train.py $target $corpus $WORKER $EPOCHS $min $HS $NEG $SAMPLE convergence $what &> logs/$name
	echo $name >> completed
}

rm completed

for x in {1..5}
do
	train 10 10 $x 3 &
	train 10 10 $x 4 &
done