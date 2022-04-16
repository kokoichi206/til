#! /bin/bash -
# 
# Description
#   Make a gaussian graph by the following steps.
#       1. Make a uniform distributions from /dev/random.
#       2. Get a gauss distribution by averaging the uniform distributions.
#       3. Write them to a temporary file.
#       4. Make a graph by using graph.sh
#       5. Remove the temporary file.
#
# Usage: bash ./graph_gaussian.sh [OPTIONS]
#   bash graph_gaussian.sh -s \# -d 1 -c 4 -n 1000
#

no_praph_script_error()
{
    echo "You need the file \"$PATH_TO_GRAPH_SCRIPT\" to make a graph"
    exit 1
}

usage()
{
    echo "Usage: $PROGRAM [OPTION] FILE"
    echo "  -c, --average-count"
    echo "      average counts"
    echo "      default value 12"
    echo "  -d, --divider"
    echo "      accuracy of the graph"
    echo "      default value 4"
    echo "  -h, --help, -help"
    echo "      print manual"
    echo "  -l, --max-length"
    echo "      max length of the graph"
    echo "      default value 60"
    echo "  -n, --num"
    echo "      number of the points"
    echo "      default value 2000"
    echo "  -s, --shape"
    echo "      shape of the graph" 
    echo "      default value ■"
}

usage_and_exit()
{
    usage
    exit $1
}

# PARAMS
PATH_TO_GRAPH_SCRIPT="./graph.sh"
AVERAGE_COUNT=12
DIVIDER=4
MAX_LENGTH=60
NUM=2000
SHAPE="■"
PROGRAM=`basename $0`

# if there's no file to make a graph, exit with error.
if [[ ! "$PATH_TO_GRAPH_SCRIPT" ]] ; then
    no_praph_script_error
fi

for i in "$@"; do
    case $i in
    -c | --average-count)
        if [[ -z "$2" ]] || [[ ! "$2" =~ [0-9]+ ]]; then
            echo "option requires an integer -- $1"
            usage_and_exit 1
        fi
        AVERAGE_COUNT="$2"
        shift 2
        ;;
    -d | --divider)
        if [[ -z "$2" ]] || [[ ! "$2" =~ [0-9]+ ]]; then
            echo "option requires an integer -- $1"
            usage_and_exit 1
        fi
        DIVIDER="$2"
        shift 2
        ;;
    -h | --help | -help)
        usage_and_exit 0
        ;;
    -l | --max-length)
        if [[ -z "$2" ]] || [[ ! "$2" =~ ^[0-9]+$ ]]; then
            echo "option requires an integer -- $1"
            usage_and_exit 1
        fi
        MAX_LENGTH="$2"
        shift 2
        ;;
    -n | --num)
        if [[ -z "$2" ]] || [[ ! "$2" =~ ^[0-9]+$ ]]; then
            echo "option requires an integer -- $1"
            usage_and_exit 1
        fi
        NUM="$2"
        shift 2
        ;;
    -s | --shape)
        if [[ -z "$2" ]] || [[ "$2" =~ ^-+ ]]; then
            echo "option requires an argument -- $1"
            usage_and_exit 1
        fi
        SHAPE="$2"
        shift 2
        ;;
    -*)
        echo "Unknown option $1"
        usage_and_exit 1
        ;;
    *)
        if [[ ! -z "$1" ]] && [[ -f "$1" ]]; then
            FILE="$1"
            echo "FILE FOUND"
            echo "$1"
            shift 1
        fi
        ;;
    esac
done

TMP_FILE=`date +%Y_%m%d_%H%M%S`

# step 1,2,3 make a temporary file
cat /dev/urandom | LC_CTYPE=utf_8 tr -dc 0-9 | fold -w 5 | sed 's@^@0.@' | xargs -n "$AVERAGE_COUNT" 2>/dev/null | head -n "$NUM" | \
    awk '{for(i=0; i<=int(NF) ;i++){{if(i==0){a = 0}else{a += $i}}{if(i == NF){print 2*a/NF}}}}' |\
    awk -v g="$DIVIDER" '{print substr(g*$0,1,3)/g}' | sort | uniq -c | awk '{print $2,$1}' > "$TMP_FILE"

# 4. Make a graph by using graph.sh
bash "$PATH_TO_GRAPH_SCRIPT" -c "$AVERAGE_COUNT" -l "$MAX_LENGTH" -s "$SHAPE" "$TMP_FILE"

# wait until the scripts writes a graph to the terminal
sleep 4
# 5. Remove the temporary file.
rm "$TMP_FILE"
