#!/bin/bash
#SBATCH -p express
#SBATCH --cpus-per-task 4
WORKER=8


#read config
source $1
run=$2
size=$3
prefix=$4

if [ "$run" ] ; then
	RUN=$run
else
	RUN=1
fi

if [ "$size" ] ; then
	SIZE=$size
fi

if [ "$prefix" ] ; then
	PREFIX=$prefix
fi

corpus=$CORPUS$PREFIX/$SIZE
name="${SIZE}_run${run}$PREFIX"
target=$TARGET/${name}
mkdir -p $target logs

cat $1 > $TARGET/${name}/config
echo "run $RUN size $SIZE prefix $PREFIX" >> $TARGET/${name}/config

what=$(
	what=""
	cd $corpus
	for x in ${WHAT//;/ }
	do
		what="$what $x"
	done
	echo $what
)

if [ "$INDEPENDENT" = true ]; then
	for w in $what
	do
		python python/train.py $target $corpus $WORKER $EPOCHS $MIN $HS $NEG $SAMPLE $CONVERGENCE $ALPHA $w &> logs/$name
	done
else
	python python/train.py $target $corpus $WORKER $EPOCHS $MIN $HS $NEG $SAMPLE $CONVERGENCE $ALPHA $what &> logs/$name
fi

echo $name >> completed
