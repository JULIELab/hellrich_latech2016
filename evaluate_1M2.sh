LOG="evaluation_1M2"
MODELS="/home/hellrich/tmp/latech2016"
rm $LOG

function do_if_ok {
	echo $@
	ok=1
	for file in "$@"
	do
		if [[ ! -e "$file" ]] ; then
    		echo "$file is missing" >> $LOG
    		ok=0
    	fi
    done
    if [ "$ok" == "1" ] ; then
    	python python/evaluate_models.py questions-words.txt $@ >> $LOG
    fi
}

for way in hierarchic negative
do
	echo $way >> $LOG
	#kim
	echo "continuous" >> $LOG
	for size in 10M 1M
	do
		echo $size >> $LOG
		echo "in runs" >> $LOG
		do_if_ok $MODELS/fiction_kim_${way}2/${size}_run{1,2,3}A/model1899*
		echo "between runs" >> $LOG
		do_if_ok $MODELS/fiction_kim_${way}2/${size}_run1{A,B,C}/model1899*
	done
done

cat $LOG