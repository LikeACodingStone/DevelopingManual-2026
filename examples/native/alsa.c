#include <errno.h>
#include <alloca.h>
#include <alsa/asoundlib.h>
#include <stdio.h>
int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: alsa DEVICE (e.g. null)\n"); return 2; }
    snd_pcm_t *pcm = NULL;
    int rc = snd_pcm_open(&pcm, argv[1], SND_PCM_STREAM_PLAYBACK, 0);
    if (rc < 0) { fprintf(stderr, "%s\n", snd_strerror(rc)); return 1; }
    rc = snd_pcm_set_params(pcm, SND_PCM_FORMAT_S16_LE, SND_PCM_ACCESS_RW_INTERLEAVED,
                            1, 16000, 1, 100000);
    short silence[320] = {0};
    snd_pcm_uframes_t offset = 0;
    int recoveries = 0;
    while (rc >= 0 && offset < 320) {
        snd_pcm_sframes_t written = snd_pcm_writei(pcm, silence + offset, 320 - offset);
        if (written < 0) {
            if (++recoveries > 3) { rc = (int)written; break; }
            rc = snd_pcm_recover(pcm, (int)written, 1);
        } else if (written == 0) { rc = -EIO; }
        else offset += (snd_pcm_uframes_t)written;
    }
    if (rc >= 0) rc = snd_pcm_drain(pcm);
    if (rc < 0) fprintf(stderr, "%s\n", snd_strerror(rc));
    snd_pcm_close(pcm);
    if (rc < 0) return 1;
    puts("written_frames=320");
    return 0;
}
