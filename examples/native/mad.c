#include <mad.h>
#include <stdio.h>
#include <stdlib.h>
struct context { unsigned char *data; unsigned long size; unsigned long frames; int fed; };
static enum mad_flow input(void *arg, struct mad_stream *stream) {
    struct context *c = arg;
    if (c->fed) return MAD_FLOW_STOP;
    mad_stream_buffer(stream, c->data, c->size);
    c->fed = 1;
    return MAD_FLOW_CONTINUE;
}
static enum mad_flow output(void *arg, const struct mad_header *header, struct mad_pcm *pcm) {
    (void)header;
    struct context *c = arg;
    c->frames += pcm->length;
    /* pcm->samples[ch][i] are fixed-point; count decoded frames, not byte output. */
    return MAD_FLOW_CONTINUE;
}
static enum mad_flow error(void *arg, struct mad_stream *stream, struct mad_frame *frame) {
    (void)arg; (void)frame;
    return MAD_RECOVERABLE(stream->error) ? MAD_FLOW_CONTINUE : MAD_FLOW_BREAK;
}
int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: mad FILE.mp3\n"); return 2; }
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 1;
    if (fseek(file, 0, SEEK_END)) { fclose(file); return 1; }
    long length = ftell(file);
    if (length <= 0 || length > 16 * 1024 * 1024 || fseek(file, 0, SEEK_SET)) { fclose(file); return 1; }
    struct context c = {0};
    c.data = calloc((size_t)length + MAD_BUFFER_GUARD, 1);
    if (!c.data) { fclose(file); return 1; }
    if (fread(c.data, 1, (size_t)length, file) != (size_t)length) { free(c.data); fclose(file); return 1; }
    fclose(file);
    c.size = (unsigned long)length + MAD_BUFFER_GUARD;
    struct mad_decoder decoder;
    mad_decoder_init(&decoder, &c, input, NULL, NULL, output, error, NULL);
    int rc = mad_decoder_run(&decoder, MAD_DECODER_MODE_SYNC);
    mad_decoder_finish(&decoder);
    free(c.data);
    printf("decoded_frames=%lu\n", c.frames);
    return rc != 0 || c.frames == 0;
}
