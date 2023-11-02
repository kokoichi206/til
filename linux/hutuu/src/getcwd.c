#include <stdlib.h>
#include <unistd.h>
#include <errno.h>

#define INIT_BUFSIZE 1024

char *
my_getcwd(void)
{
    char *buf, *tmp;
    // stdded に定義されてる型。
    size_t size = INIT_BUFSIZE;

    buf = malloc(size);
    if (!buf)
        return NULL;

    // 実際にバッファが足りるまでループする。
    for (;;)
    {
        errno = 0;
        if (getcwd(buf, size))
            return buf;
        if (errno != ERANGE)
            break;

        size *= 2;
        tmp = realloc(buf, size);

        if (!tmp)
            break;
        buf = tmp;
    }

    // malloc を使ったら解放を忘れない。
    free(buf);
    return NULL;
}
