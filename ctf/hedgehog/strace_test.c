#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
    pid_t pid;
    char buf[16];
    int user_input;

    pid = fork();
    if (pid == 0)
    {
        puts("Segmentation Fault");
        exit(0);
    }
    else
    {
        puts("Enter the pid of the child process.");
        fgets(buf, sizeof(buf), stdin);
        user_input = atoi(buf);
        if (pid == user_input)
        {
            puts("Conguratulations! Your FLAG is ctf4b{xxeeyyea}");
        }
    }

    return 0;
}
