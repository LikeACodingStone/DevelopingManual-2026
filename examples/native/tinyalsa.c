#include <tinyalsa/asoundlib.h>
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char **argv) {
    if (argc != 3) { fprintf(stderr, "usage: tinyalsa CARD DEVICE\n"); return 2; }
    char *end;
    unsigned long card = strtoul(argv[1], &end, 10);
    if (*end || card > 255 || !*argv[1]) return 2;
    unsigned long device = strtoul(argv[2], &end, 10);
    if (*end || device > 255 || !*argv[2]) return 2;
    struct pcm_config cfg = { .channels = 1, .rate = 16000, .period_size = 320,
        .period_count = 4, .format = PCM_FORMAT_S16_LE };
    struct pcm *pcm = pcm_open((unsigned)card, (unsigned)device, PCM_OUT, &cfg);
    if (!pcm || !pcm_is_ready(pcm)) {
        if (pcm) { fprintf(stderr, "%s\n", pcm_get_error(pcm)); pcm_close(pcm); }
        return 1;
    }
    short samples[320] = {0};
    int rc = pcm_write(pcm, samples, sizeof(samples));
    if (rc) fprintf(stderr, "%s\n", pcm_get_error(pcm));
    pcm_close(pcm);
    return rc ? 1 : 0;
}
