# Axel '0vercl0k' Souchet - 28th March 2019
# ./mach build-backend -b CompileDB
OUT_DIR=ff-woboq
DATA_DIR=/data
rm -rf $OUT_DIR
codebrowser_generator -a -o $OUT_DIR -b obj-x86_64-pc-linux-gnu -d $DATA_DIR -p Firefox:$(pwd) 
codebrowser_indexgenerator -d $DATA_DIR $OUT_DIR
cp -R ../woboq_codebrowser/data $OUT_DIR
