#include <speex/speex_resampler.h>
#include <stdio.h>
int main(void) {
    int err;
    SpeexResamplerState *state = speex_resampler_init(1, 16000, 48000, 5, &err);
    if (!state || err != RESAMPLER_ERR_SUCCESS) return 1;
    spx_int16_t input[320] = {0}, output[960] = {0};
    spx_uint32_t in_count = 320, out_count = 960;
    err = speex_resampler_process_int(state, 0, input, &in_count, output, &out_count);
    speex_resampler_destroy(state);
    if (err != RESAMPLER_ERR_SUCCESS || in_count != 320 || out_count == 0) return 1;
    printf("consumed=%u produced=%u\n", in_count, out_count);
    return 0;
}
