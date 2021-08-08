# Compute integer factorizations of integers supplied one per line
# Usage:
#   awk -f factorize.awk filename
#   e.g. $ awk -f factorize.awk test.dat
{
    n = int($1)
    m = n = (n >= 2) ? n : 2
    factors = ""
    for (k = 2; (m > 1) && (k^2 <= n); )
    {
        if (int(m % k) != 0)
        {
            k++
            continue
        }
        m /= k
        factors = (factors == "") ? ("" k) : (factors " * " k)
    }
    if ((1 < m) && (m < n))
        factors = factors " * " m
    print n, (factors == "") ? "is prime" : ("= " factors)
}
