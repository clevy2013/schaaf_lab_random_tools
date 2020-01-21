#!/bin/bash

usage="Usage: cmd [-s start date] [-e end date] [-n product short name] [-t tile] [-d download dir]"
while getopts ":s:e:n:t:d:" arg; do
    echo $OPTARG
    case $arg in
	s) start_date=$OPTARG;;
	e) end_date=$OPTARG;;
	n) short_name=$OPTARG;;
	t) tile=$OPTARG;;
	d) dl_dir=$OPTARG;;
	\?) echo $usage
    esac
done

if [ -z $start_date ] || [ -z $end_date ] || [ -z $short_name ] || [ -z $tile ] || \
       [ -z $dl_dir ]; then
    echo $usage
    exit
else
    echo "All ok"
fi

