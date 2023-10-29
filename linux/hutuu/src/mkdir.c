#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>

int main(int argc, char const *argv[])
{
    if (argc < 2)
    {
        fprintf(stderr, "%s: no arguments was passed\n", argv[0]);
        exit(1);
    }

    for (int i = 1; i < argc; i++)
    {
        if (mkdir(argv[i], 0x777) < 0)
        {
            perror(argv[i]);
            exit(1);
        }
    }

    exit(0);
}
