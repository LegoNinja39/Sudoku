#!/bin/bash

bFile="./board.txt"

function solve {
    if [ -f $bFile ]; then
        python3 -c "import sys; import Sudoku; Sudoku.solve(sys.argv[1])" ${bFile}
    else echo "No board to solve."
    fi
}

function remove {
    if ! [[ $1 =~ ^[0-9]+$ ]]; then echo "Argument is not a number"; return; fi
    if [ -f $bFile ]; then
        python3 -c 'from sys import argv; import Sudoku; Sudoku.remove(argv[1], int(argv[2]))' ${bFile} $1
    else echo "No board to remove from."
    fi
}

function usage {
    echo "Script Usage:"
    echo -e "\t[-b]: Build a Sudoku"
    echo -e "\t[-r num]: Remove [num] from Sudoku"
    echo -e "\t[-s]: Solve the Sudoku"
}

while getopts ":bsr:" flags; do
    case $flags in
        b) python3 -c 'import sys; import Sudoku; Sudoku.build(sys.argv[1])' ${bFile};;
        s) solve ;;
        r) remove ${OPTARG} ;;
        ?) echo -n "Invalid flag - "; usage ;;
    esac
done
