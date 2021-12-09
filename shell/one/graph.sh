#! /bin/bash -
# cat /dev/urandom | LC_CTYPE=C tr -dc 0-9 | fold -w 5 | sed 's@^@0.@' | xargs -n 12 2>/dev/null | head -n 1000 | \
# awk '{for(i=0; i<=int(NF) ;i++){{if(i==0){a = 0}else{a += $i}}{if(i == NF){print 2*a/NF}}}}' |\

usage()
{
    echo "Usage: $PROGRAM [OPTION] FILE"
    echo "  -c, --average-count"
    echo "      average counts"
    echo "  -h, --help, -help"
    echo "      print manual"
    echo "  -l, --max-length"
    echo "      max length of the graph"
    echo "  -s, --shape"
    echo "      shape of the graph" 
}

usage_and_exit()
{
    usage
    exit $1
}

DIVIDER=4
AVERAGE_COUNT=12
MAX_LENGTH=60
SHAPE="■"
PROGRAM=`basename $0`

for i in "$@"; do
    case $i in
    -c | --average-count)
        if [[ -z "$2" ]] || [[ ! "$2" =~ [0-9]+ ]]; then
            echo "option requires an integer -- $1"
            usage_and_exit 1
        fi
        echo "$2"
        AVERAGE_COUNT="$2"
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
        echo "$2"
        MAX_LENGTH="$2"
        shift 2
        ;;
    -s | --shape)
        if [[ -z "$2" ]] || [[ "$2" =~ ^-+ ]]; then
            echo "option requires an argument -- $1"
            usage_and_exit 1
        fi
        echo "$2"
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
            shift 1
        fi
        ;;
    esac
done
echo $1
if [[ "$FILE" ]] ; then
    echo "file $FILE exists"
    cat "$FILE" |\
    awk -v i=1 -v max_length="$MAX_LENGTH" -v shape="$SHAPE" 
    '{b[i]=$1; a[i]=$2; i=i+1; if($2 > max){max = $2}}
    END{for(j=1; j<=length(a); j++){printf "%1.2f: ", b[j]; 
    for(k=0; k<int(max_length*a[j]/max); k++){printf shape}{printf "\n"}}}'
else
    echo "file $1 does NOT exist"
    usage_and_exit 1
fi
