#include <opus/opus.h>
#include <stdio.h>
int main(void) {
    int error;
    OpusEncoder *enc = opus_encoder_create(16000, 1, OPUS_APPLICATION_VOIP, &error);
    if (!enc || error != OPUS_OK) return 1;
    OpusDecoder *dec = opus_decoder_create(16000, 1, &error);
    if (!dec || error != OPUS_OK) { opus_encoder_destroy(enc); return 1; }
    opus_int16 input[320] = {0}, output[320];
    unsigned char packet[1276];
    int size = opus_encode(enc, input, 320, packet, sizeof(packet));
    int count = size > 0 ? opus_decode(dec, packet, size, output, 320, 0) : -1;
    opus_decoder_destroy(dec); opus_encoder_destroy(enc);
    if (count != 320) return 1;
    printf("decoded_frames=%d\n", count);
    return 0;
}
