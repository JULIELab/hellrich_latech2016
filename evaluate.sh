LOG="evaluation"
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
		do_if_ok $MODELS/fiction_kim_$way/${size}_run{1,2,3}A/model1900_1900
		echo "between runs" >> $LOG
		do_if_ok $MODELS/fiction_kim_$way/${size}_run1{A,B,C}/model1900_1900
	done
done

#kulk
echo "isolated" >> $LOG
echo "hierarchic" >> $LOG
for epoch in  {1..10}
do
	echo $epoch >> $LOG
	do_if_ok $MODELS/kulkarni_hierarchic_inter2/all-5Y_run{1,2,3}/model1900_1904_epoch_$epoch
done
echo "negative" >> $LOG
for epoch in  {1..10}
do
	echo $epoch >> $LOG
	do_if_ok $MODELS/kulkarni_neg_inter2/all-5Y_run{1,2,3}/model1900_1904_epoch_$epoch
done
cat $LOG