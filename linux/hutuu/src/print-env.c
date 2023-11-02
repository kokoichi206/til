#include <stdio.h>
#include <stdlib.h>

// どのヘッダフィアルでも宣言されてないため、自分で extern 宣言が必要。
extern char **environ;

int main(int argc, char const *argv[])
{
    char **p;

    // 結構色々あるな。
    for (p = environ; *p; p++)
    {
        printf("%s\n", *p);
    }
    exit(0);
}
