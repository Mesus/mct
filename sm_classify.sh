#!/bin/bash
if [[ $1 == "" ]]
 then
 echo "Please set file name"
 else
 python sm_classify.py $1 $2
 #echo $1
fi
