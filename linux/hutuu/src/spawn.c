#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main(int argc, char const *argv[])
{
    pid_t pid;

    if (argc != 3)
    {
        fprintf(stderr, "Usage: %s <command> <arg>\n", argv[0]);
        exit(1);
    }

    // 子プロセスと親プロセスの両方で呼び出しが戻る！！
    pid = fork();
    if (pid < 0)
    {
        fprintf(stderr, "fork(2) failed\n");
        exit(1);
    }
    if (pid == 0)
    {
        // 子プロセス。
        execl(argv[1], argv[1], argv[2], NULL);
        // execl が呼び出しから戻ったら失敗。
        perror(argv[1]);
        exit(99);
    }
    else
    {
        // 親プロセス。
        int status;

        waitpid(pid, &status, 0);
        printf("child (pid=%d) finished: \n", pid);

        if (WIFEXITED(status))
            printf("exit, status=%d\n", WEXITSTATUS(status));
        else if (WIFSIGNALED(status))
            printf("signal, sig=%d\n", WTERMSIG(status));
        else
            printf("abnormal exit\n");

        exit(0);
    }
}
