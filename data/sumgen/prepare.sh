#!/usr/bin/env bash

set -x # Add this line to enable debugging

CURRENT_DIR=`pwd`
HOME_DIR=`realpath ../..`;

DATA_DIR=${CURRENT_DIR}/processed
SPM_DIR=${HOME_DIR}/sentencepiece
LANG_EN=en_XX


function spm_preprocess () {

LANG=$1
for SPLIT in train valid test; do
    if [[ ! -f $DATA_DIR/${SPLIT}.$LANG-en.spm.$LANG ]]; then
        python encode.py \
            --model_file ${SPM_DIR}/sentencepiece.bpe.model \
            --input_source $DATA_DIR/${SPLIT}.$LANG-$LANG_EN.$LANG \
            --input_target $DATA_DIR/${SPLIT}.$LANG-$LANG_EN.$LANG_EN \
            --output_source $DATA_DIR/${SPLIT}.$LANG-$LANG_EN.spm.$LANG \
            --output_target $DATA_DIR/${SPLIT}.$LANG-$LANG_EN.spm.$LANG_EN \
            --max_len 510 \
            --workers 60;
    fi
done

}


function binarize () {

LANG=$1

fairseq-preprocess \
    --source-lang $LANG \
    --target-lang $LANG_EN \
    --trainpref $DATA_DIR/train.$LANG-$LANG_EN.spm \
    --validpref $DATA_DIR/valid.$LANG-$LANG_EN.spm \
    --testpref $DATA_DIR/test.$LANG-$LANG_EN.spm \
    --destdir $DATA_DIR/binary \
    --workers 60 \
    --srcdict ${SPM_DIR}/dict.txt \
    --tgtdict ${SPM_DIR}/dict.txt;

fairseq-preprocess \
    --source-lang $LANG_EN \
    --target-lang $LANG \
    --trainpref $DATA_DIR/train.$LANG-$LANG_EN.spm \
    --validpref $DATA_DIR/valid.$LANG-$LANG_EN.spm \
    --testpref $DATA_DIR/test.$LANG-$LANG_EN.spm \
    --destdir $DATA_DIR/binary \
    --workers 60 \
    --srcdict ${SPM_DIR}/dict.txt \
    --tgtdict ${SPM_DIR}/dict.txt;

}


mkdir -p $DATA_DIR;
export PYTHONPATH=${HOME_DIR};
for lang in java python cpp; do
    python process.py \
        --lang $lang \
        --out_dir $DATA_DIR \
        --root_folder ${HOME_DIR}/third_party;
    spm_preprocess $lang && binarize $lang
done
