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

echo "run $RUN size $SIZE prefix $PREFIX"