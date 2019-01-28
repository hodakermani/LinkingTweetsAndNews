#! /bin/bash

source scripts/vars.sh
source scripts/run_wtmf.sh $1
if [ ! -e $MODEL_DIR/smodel.p ]; then
	echo "Single Threaded Model Exist!"
	source scripts/run_wtmf_single_threaded.sh $1
fi
diff $MODEL_DIR/model.p $MODEL_DIR/smodel.p 
diff $MODEL_DIR/model.q $MODEL_DIR/smodel.q 
echo "************** Test Done *****************"