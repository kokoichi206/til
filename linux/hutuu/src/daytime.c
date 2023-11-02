#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>

static int open_connection(char *host, char *service);

int main(int argc, char *argv[])
{
    int sock;
    FILE *f;
    char buf[1024];

    sock = open_connection((argc > 1 ? argv[1] : "localhost"), "daytime");
    f = fdopen(sock, "r");
    if (!f)
    {
        perror("fdopen(3)");
        exit(1);
    }
    fgets(buf, sizeof buf, f);
    fclose(f);
    fputs(buf, stdout);
    exit(0);
}

// TCP 接続を担当する。
static int
open_connection(char *host, char *service)
{
    int sock;
    struct addrinfo hints, *res, *ai;
    int err;

    memset(&hints, 0, sizeof(struct addrinfo));
    // hint で候補を絞り込むためのヒントを与える。
    // アドレスファミリーはなんでもいい（IPv4, IPv6）。
    hints.ai_family = AF_UNSPEC;
    // パケットではなくストリーム形式の接続を使う（= TCP）。
    hints.ai_socktype = SOCK_STREAM;

    if ((err = getaddrinfo(host, service, &hints, &res)) != 0)
    {
        fprintf(stderr, "getaddrinfo(3): %s\n", gai_strerror(err));
        exit(1);
    }

    // getaddrinfo が返してくるのがリンクリストだから for 文を使っている。
    for (ai = res; ai; ai = ai->ai_next)
    {
        // ソケット接続しちゃう。
        sock = socket(ai->ai_family, ai->ai_socktype, ai->ai_protocol);
        if (sock < 0)
        {
            continue;
        }
        if (connect(sock, ai->ai_addr, ai->ai_addrlen) < 0)
        {
            close(sock);
            continue;
        }
        /* success */
        freeaddrinfo(res);
        return sock;
    }

    fprintf(stderr, "socket(2)/connect(2) failed");
    freeaddrinfo(res);
    exit(1);
}
