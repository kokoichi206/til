#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(int argc, char **argv)
{
    if (argc != 3)
    {
        fprintf(stderr, "Usage: %s <command1> <command2>\n", argv[0]);
        exit(1);
    }

    int fds[2];
    // 両端とも自プロセスに繋がったストリームを生成する。
    // fds[0] は読み込み専用 fds[1] は書き込み専用。
    pipe(fds);

    // 子プロセスと親プロセスの両方で呼び出しが戻る！！
    int pid = fork();
    if (pid < 0)
    {
        fprintf(stderr, "fork(2) failed\n");
        exit(1);
    }

    if (pid == 0)
    {
        // 子プロセス。

        // 書き込みのストリーム用の fd を閉じる。
        close(fds[1]);
        // 読み込みを標準入力のストリームに複製する。
        dup2(fds[0], STDIN_FILENO);
        close(fds[0]);

        execlp(argv[2], argv[2], NULL);

        // execlpが失敗した場合。
        perror("execlp child");
        exit(1);
    }
    else
    {
        // 親プロセス。

        // 読み込みのストリーム用の fd を閉じる。
        close(fds[0]);
        // 書き込みを標準出力のストリームに複製する。
        dup2(fds[1], STDOUT_FILENO);
        close(fds[1]);

        execlp(argv[1], argv[1], NULL);

        // execlpが失敗した場合。
        perror("execlp parent");
        exit(1);
    }

    wait(NULL);

    exit(0);
}
