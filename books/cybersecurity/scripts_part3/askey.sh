# functions to convert decimal to ascii and vice-versa

function aschar ()
{
    local ashex
    printf -v ashex '\\x%02x' $1
    printf '%b' $ashex
}

function asnum ()
{
    printf '%d' \"$1
}
