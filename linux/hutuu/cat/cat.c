#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>

// 関数のプロトタイプ宣言
static int get_wc_opt(int argc, char *argv[]);
static void cat_standard_input();
static void do_cat(const char *path);
static void die(const char *s);
static void wc(const char *path);
static void wc_standard_input();

int main(int argc, char *argv[])
{
    int opt;
    opt = get_wc_opt(argc, argv);

    if (argc < 2 + opt)
    {
        fprintf(stderr, "%s: file name was not given\n", argv[0]);
        if (opt)
        {
            wc_standard_input();
        }
        else
        {
            cat_standard_input();
        }
        exit(0);
    }
    for (int i = 1 + opt; i < argc; i++)
    {
        if (opt)
        {
            wc(argv[i]);
        }
        else
        {
            do_cat(argv[i]);
        }
    }
    exit(0);
}

static int
get_wc_opt(int argc, char *argv[])
{
    for (int i = 1; i < argc; i++)
    {
        if (strcmp(argv[i], "-w") == 0)
        {
            return 1;
        }
    }
    return 0;
}

#define BUFFER_SIZE 2048

static void
cat_standard_input()
{
    unsigned char buf[BUFFER_SIZE];
    int n;

    for (;;)
    {
        n = read(STDIN_FILENO, buf, sizeof buf);
        if (n < 0)
        {
            return;
        }
        if (n == 0)
            break;
        if (write(STDOUT_FILENO, buf, n) < 0)
            return;
    }
}

static void
do_cat(const char *path)
{
    int fd;
    unsigned char buf[BUFFER_SIZE];
    int n;

    fd = open(path, O_RDONLY);
    if (fd < 0)
        die(path);
    for (;;)
    {
        n = read(fd, buf, sizeof buf);
        if (n < 0)
            die(path);
        if (n == 0)
            break;
        if (write(STDOUT_FILENO, buf, n) < 0)
            die(path);
    }
    if (close(fd) < 0)
        die(path);
}

static void
wc(const char *path)
{
    int fd;
    unsigned char buf[BUFFER_SIZE];
    int n;
    int count = 0;

    fd = open(path, O_RDONLY);
    if (fd < 0)
        die(path);
    for (;;)
    {
        n = read(fd, buf, sizeof buf);
        if (n < 0)
            die(path);
        if (n == 0)
            break;
        for (int i = 0; i < n; i++)
        {
            if (buf[i] == '\n')
            {
                count++;
            }
        }
    }
    printf("%d\n", count);
    if (close(fd) < 0)
        die(path);
}

static void
wc_standard_input()
{
    unsigned char buf[BUFFER_SIZE];
    int n;
    int count = 0;

    for (;;)
    {
        n = read(STDIN_FILENO, buf, sizeof buf);
        if (n < 0)
        {
            return;
        }
        if (n == 0)
            break;
        for (int i = 0; i < n; i++)
        {
            if (buf[i] == '\n')
            {
                count++;
            }
        }
    }
    printf("%d\n", count);
}

static void
die(const char *s)
{
    perror(s);
    exit(1);
}
