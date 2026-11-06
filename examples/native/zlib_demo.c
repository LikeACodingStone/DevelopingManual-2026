/*
 * zlib C API: one-shot compress2/uncompress, a streaming deflate/inflate loop with a
 * hard output limit, and corrupt-input handling.
 *
 * Build: cc -std=c11 -Wall -Wextra -Werror examples/native/zlib_demo.c -lz -o /tmp/zlib-demo
 * Run:   /tmp/zlib-demo
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <zlib.h>

static int fail(const char *what, int code)
{
    fprintf(stderr, "FAIL: %s (zlib code %d)\n", what, code);
    return 1;
}

/* Streaming deflate of an in-memory buffer through a small output chunk. */
static int deflate_stream(const unsigned char *in, size_t in_len, unsigned char **out, size_t *out_len)
{
    unsigned char chunk[64];
    size_t cap = 256, used = 0;
    unsigned char *buf = malloc(cap);
    if (!buf)
        return Z_MEM_ERROR;

    z_stream s;
    memset(&s, 0, sizeof s);
    int rc = deflateInit(&s, Z_DEFAULT_COMPRESSION);
    if (rc != Z_OK) {
        free(buf);
        return rc;
    }
    s.next_in = (Bytef *)in;
    s.avail_in = (uInt)in_len;
    do {
        s.next_out = chunk;
        s.avail_out = sizeof chunk;
        rc = deflate(&s, Z_FINISH);          /* Z_FINISH: all input supplied */
        if (rc == Z_STREAM_ERROR)
            break;
        size_t have = sizeof chunk - s.avail_out;
        if (used + have > cap) {
            while (used + have > cap)
                cap *= 2;
            unsigned char *bigger = realloc(buf, cap);
            if (!bigger) {
                rc = Z_MEM_ERROR;
                break;
            }
            buf = bigger;
        }
        memcpy(buf + used, chunk, have);
        used += have;
    } while (rc != Z_STREAM_END);            /* Z_OK / Z_BUF_ERROR mean "call again" */
    deflateEnd(&s);
    if (rc != Z_STREAM_END) {
        free(buf);
        return rc == Z_OK ? Z_BUF_ERROR : rc;
    }
    *out = buf;
    *out_len = used;
    return Z_OK;
}

/* Inflate into a caller-sized buffer; exceeding the limit is an error, not a realloc. */
static int inflate_limited(const unsigned char *in, size_t in_len, unsigned char *out, size_t limit, size_t *out_len)
{
    z_stream s;
    memset(&s, 0, sizeof s);
    int rc = inflateInit(&s);
    if (rc != Z_OK)
        return rc;
    s.next_in = (Bytef *)in;
    s.avail_in = (uInt)in_len;
    s.next_out = out;
    s.avail_out = (uInt)limit;
    rc = inflate(&s, Z_FINISH);
    *out_len = limit - s.avail_out;
    inflateEnd(&s);
    if (rc == Z_STREAM_END)
        return Z_OK;
    return rc == Z_OK || rc == Z_BUF_ERROR ? Z_BUF_ERROR : rc; /* output full or input truncated */
}

int main(void)
{
    unsigned char text[2000];
    for (size_t i = 0; i < sizeof text; i++)
        text[i] = (unsigned char)("STATUS=OK;"[i % 10]);

    /* 1. One-shot API: size the destination with compressBound(). */
    uLongf packed_len = compressBound(sizeof text);
    unsigned char *packed = malloc(packed_len);
    if (!packed)
        return fail("malloc", 0);
    int rc = compress2(packed, &packed_len, text, sizeof text, Z_BEST_COMPRESSION);
    if (rc != Z_OK)
        return fail("compress2", rc);
    unsigned char restored[sizeof text];
    uLongf restored_len = sizeof restored;
    rc = uncompress(restored, &restored_len, packed, packed_len);
    if (rc != Z_OK || restored_len != sizeof text || memcmp(restored, text, sizeof text) != 0)
        return fail("uncompress round trip", rc);

    /* 2. Streaming deflate with a 64-byte output chunk, then limited inflate. */
    unsigned char *streamed = NULL;
    size_t streamed_len = 0;
    rc = deflate_stream(text, sizeof text, &streamed, &streamed_len);
    if (rc != Z_OK)
        return fail("deflate_stream", rc);
    size_t got = 0;
    rc = inflate_limited(streamed, streamed_len, restored, sizeof restored, &got);
    if (rc != Z_OK || got != sizeof text || memcmp(restored, text, sizeof text) != 0)
        return fail("stream round trip", rc);

    /* 3. A limit smaller than the real size must fail, not truncate silently. */
    rc = inflate_limited(streamed, streamed_len, restored, 100, &got);
    if (rc == Z_OK)
        return fail("limit not enforced", rc);

    /* 4. Truncated and corrupted input must be reported. */
    rc = inflate_limited(streamed, streamed_len / 2, restored, sizeof restored, &got);
    if (rc == Z_OK)
        return fail("truncated input accepted", rc);
    streamed[streamed_len / 2] ^= 0xFF;
    rc = inflate_limited(streamed, streamed_len, restored, sizeof restored, &got);
    if (rc == Z_OK)
        return fail("corrupted input accepted", rc);

    free(streamed);
    free(packed);
    puts("zlib C round trip OK");
    return 0;
}
