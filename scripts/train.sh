#!/bin/bash
#SBATCH -p express
#SBATCH --cpus-per-task 4
WORKER=8


#read config
source $1
run=$2

corpus=$CORPUS/$SIZE
name="$SIZE_${MIN}MIN_con${CONVERGENCE}_run${run}"
target=$TARGET/${name}
cat $1 > $TARGET/${name}/config

what=$(
	what=""
	cd $corpus
	for x in ${WHAT//;/ }
	do
		what="$what $x"
	done
	echo $what
)

mkdir -p $target logs

if [ "$INDEPENDENT" = true ]; then
	for w in $what
	do
		python python/train.py $target $corpus $WORKER $EPOCHS $MIN $HS $NEG $SAMPLE $CONVERGENCE $w &> logs/$name
	done
else
	python python/train.py $target $corpus $WORKER $EPOCHS $MIN $HS $NEG $SAMPLE $CONVERGENCE $what &> logs/$name
fi

echo $name >> completed
