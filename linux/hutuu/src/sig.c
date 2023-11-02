#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

// シグナルハンドラ。シグナル番号を受け取る。
void showsig(int sig)
{
    printf("signal=%d\n", sig);
}

int main(int argc, char *argv[])
{
    // https://linuxjm.osdn.jp/html/LDP_man-pages/man2/signal.2.html
    // SIGINT (Ctrl+C)のシグナルハンドラとして showsig を設定。
    //
    // Signal numbering:
    // https://linuxjm.osdn.jp/html/LDP_man-pages/man7/signal.7.html
    signal(SIGINT, showsig);

    // シグナルを受け取るまでプログラムを一時停止。
    pause();
    // シグナルを受け取ったらプログラムを終了。
    exit(0);
}
