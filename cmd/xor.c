#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void usage(char * name)
{
    printf("Usage: %s [-k key]\n", name);
}

int main(int argc, char **argv)
{
    char key = 1;
    char ch;
    while ((ch = getopt(argc, argv, "hk:")) != -1) {
        switch (ch) {
            case 'h':
                usage(argv[0]);
                return 0;
            case 'k':
                key = atoi(optarg) & 0xFF;
                break;
            default:
                usage(argv[0]);
                return 1;
        }
    }

    char buf[1024];
    int cnt = 0;
    while ((cnt = fread(buf, 1, 1024, stdin)) > 0) {
        for (int i = 0; i < cnt; ++i) {
            buf[i] ^= key;
        }
        fwrite(buf, 1, cnt, stdout);
    }
    return 0;
}
