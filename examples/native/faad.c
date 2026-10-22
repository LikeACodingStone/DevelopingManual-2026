#include <neaacdec.h>
#include <stdio.h>
#include <stdlib.h>
/* Bounded whole-file ADTS example. Output is counted, not saved. */
int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: faad FILE.aac\n"); return 2; }
    FILE *f = fopen(argv[1], "rb");
    if (!f) return 1;
    if (fseek(f, 0, SEEK_END)) { fclose(f); return 1; }
    long length = ftell(f);
    if (length <= 0 || length > 16 * 1024 * 1024 || fseek(f, 0, SEEK_SET)) { fclose(f); return 1; }
    unsigned char *data = malloc((size_t)length);
    if (!data) { fclose(f); return 1; }
    size_t size = fread(data, 1, (size_t)length, f);
    fclose(f);
    if (size != (size_t)length) { free(data); return 1; }
    NeAACDecHandle dec = NeAACDecOpen();
    if (!dec) { free(data); return 1; }
    NeAACDecConfigurationPtr cfg = NeAACDecGetCurrentConfiguration(dec);
    cfg->outputFormat = FAAD_FMT_16BIT;
    int ok = NeAACDecSetConfiguration(dec, cfg);
    unsigned long rate = 0; unsigned char channels = 0;
    long used = ok ? NeAACDecInit(dec, data, (unsigned long)size, &rate, &channels) : -1;
    unsigned long samples = 0;
    if (used < 0 || (size_t)used > size) ok = 0;
    size_t offset = used >= 0 ? (size_t)used : 0;
    while (ok && offset < size) {
        NeAACDecFrameInfo info;
        void *pcm = NeAACDecDecode(dec, &info, data + offset, (unsigned long)(size - offset));
        if (info.error || !info.bytesconsumed || info.bytesconsumed > size - offset || (!pcm && info.samples)) {
            ok = 0; break;
        }
        samples += info.samples;
        offset += info.bytesconsumed;
    }
    NeAACDecClose(dec); free(data);
    printf("rate=%lu channels=%u decoded_samples=%lu\n", rate, channels, samples);
    return !ok || samples == 0;
}
