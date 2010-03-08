#!/bin/bash

dir=`dirname $0`
log=$dir/`basename $0 .sh`.log

echo $0 executed at `date` > $log


function extractTargetSet {
    
    sourceFile="$1"
    destinationFolder="$2"
    targetSet="$3"

    full_h=`inkscape "-f$sourceFile" -C -H 2>> $log`

    for target in `cat $dir/targets/$targetSet`; do
        x=`inkscape "-f$sourceFile" -C "-I$target" -X 2>> $log`
        y=`inkscape "-f$sourceFile" -C "-I$target" -Y 2>> $log`
        w=`inkscape "-f$sourceFile" -C "-I$target" -W 2>> $log`
        h=`inkscape "-f$sourceFile" -C "-I$target" -H 2>> $log`

        # remove e notation
        if echo $y | grep e &> /dev/null; then
            y=0
        fi
        if echo $x | grep e &> /dev/null; then
            x=0
        fi

        # corrects value of y.
        y=`echo $full_h - $y | bc`

        inkscape -z -C "-f$sourceFile" "-i$target" -j "-a$x:`echo $y-$h|bc`:`echo $x+$w|bc`:$y" "-e$destinationFolder/$target.png" -b#000000 -y0.0 -d76 &>> $log
    done
}

extractTargetSet $dir/vectorial/ships/ships.svg $dir/../src/client/imgs/ships/ ships
extractTargetSet $dir/vectorial/turrets/turrets.svg $dir/../src/client/imgs/turrets/ turrets
extractTargetSet $dir/vectorial/turrets/turrets.svg $dir/../src/client/imgs/missiles/ missiles

