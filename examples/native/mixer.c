#include <errno.h>
#include <alloca.h>
#include <alsa/asoundlib.h>
#include <stdio.h>
/* Read only: the example does not change the user's audio volume. */
int main(int argc, char **argv) {
    if (argc != 3) { fprintf(stderr, "usage: mixer CARD ELEMENT\n"); return 2; }
    snd_mixer_t *mixer = NULL;
    int rc = snd_mixer_open(&mixer, 0);
    if (rc < 0) return 1;
    if ((rc = snd_mixer_attach(mixer, argv[1])) < 0 ||
        (rc = snd_mixer_selem_register(mixer, NULL, NULL)) < 0 ||
        (rc = snd_mixer_load(mixer)) < 0) goto finish;
    snd_mixer_selem_id_t *id;
    snd_mixer_selem_id_alloca(&id);
    snd_mixer_selem_id_set_index(id, 0);
    snd_mixer_selem_id_set_name(id, argv[2]);
    snd_mixer_elem_t *elem = snd_mixer_find_selem(mixer, id);
    if (!elem || !snd_mixer_selem_has_playback_volume(elem)) { rc = -ENOENT; goto finish; }
    long low, high, value;
    if ((rc = snd_mixer_selem_get_playback_volume_range(elem, &low, &high)) < 0) goto finish;
    if ((rc = snd_mixer_selem_get_playback_volume(elem, SND_MIXER_SCHN_FRONT_LEFT, &value)) < 0) goto finish;
    printf("min=%ld max=%ld current=%ld\n", low, high, value);
finish:
    if (rc < 0) fprintf(stderr, "%s\n", snd_strerror(rc));
    snd_mixer_close(mixer);
    return rc < 0;
}
