#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <regex.h>
#define _GNU_SOURCE
#include <getopt.h>
#include <stdarg.h>

static void do_grep(regex_t *pat, FILE *f);
static void debug_print(const char *fmt, ...);

static int opt_ignorecase = 0;
static int opt_invertmatch = 0;
static int debug = 0;

static struct option longopts[] = {
    {"ignore-case", no_argument, NULL, 'i'},
    {"invert-match", no_argument, NULL, 'v'},
    {NULL, 0, NULL, 0},
};

int main(int argc, char *argv[])
{
    regex_t pat;
    int err;
    int i;

    int opt;

    while ((opt = getopt_long(argc, argv, "ivd", longopts, NULL)) != -1)
    {
        switch (opt)
        {
        case 'i':
            opt_ignorecase = 1;
            break;
        case 'v':
            opt_invertmatch = 1;
            break;
        case 'd':
            debug = 1;
            break;
        case '?':
            exit(1);
        }
    }

    argc -= optind;
    argv += optind;

    debug_print("optind %d\n", optind);
    debug_print("argc %d\n", argc);

    if (argc < 1)
    {
        fputs("no pattern\n", stderr);
        exit(1);
    }

    int re_mode = REG_EXTENDED | REG_NOSUB | REG_NEWLINE;
    if (opt_ignorecase)
        re_mode |= REG_ICASE;

    debug_print("argv[0] %s\n", argv[0]);
    debug_print("argv[1] %s\n", argv[1]);

    err = regcomp(&pat, argv[0], re_mode);
    if (err != 0)
    {
        char buf[1024];

        regerror(err, &pat, buf, sizeof buf);
        puts(buf);
        exit(1);
    }

    if (argc == 1)
    {
        do_grep(&pat, stdin);
    }
    else
    {
        for (i = 1; i < argc; i++)
        {
            FILE *f;

            f = fopen(argv[i], "r");
            if (!f)
            {
                perror(argv[i]);
                exit(1);
            }

            do_grep(&pat, f);
            fclose(f);
        }
    }

    regfree(&pat);
    exit(0);
}

static void
debug_print(const char *fmt, ...)
{
    if (debug)
    {
        va_list args;
        va_start(args, fmt);
        vprintf(fmt, args);
        va_end(args);
    }
}

static void
do_grep(regex_t *pat, FILE *src)
{
    debug_print("%s", "do_grep");

    int matched;

    char buf[4096];

    while (fgets(buf, sizeof buf, src))
    {
        matched = regexec(pat, buf, 0, NULL, 0) == 0;

        if (opt_invertmatch)
        {
            matched = !matched;
        }

        if (matched)
        {
            fputs(buf, stdout);
        }
    }
}
