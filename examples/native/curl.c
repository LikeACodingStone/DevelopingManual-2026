#include <curl/curl.h>
#include <stdio.h>
static size_t output(char *data, size_t size, size_t count, void *unused) {
    (void)unused;
    return fwrite(data, size, count, stdout) * size;
}
int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: curl-demo URL\n"); return 2; }
    if (curl_global_init(CURL_GLOBAL_DEFAULT) != CURLE_OK) return 1;
    CURL *curl = curl_easy_init();
    if (!curl) { curl_global_cleanup(); return 1; }
    CURLcode rc = CURLE_OK;
#define SET(option, value) do { rc = curl_easy_setopt(curl, option, value); if (rc != CURLE_OK) goto done; } while (0)
    SET(CURLOPT_URL, argv[1]);
    SET(CURLOPT_CONNECTTIMEOUT, 5L);
    SET(CURLOPT_TIMEOUT, 10L);
    SET(CURLOPT_SSL_VERIFYPEER, 1L);
    SET(CURLOPT_SSL_VERIFYHOST, 2L);
    SET(CURLOPT_FAILONERROR, 1L);
    SET(CURLOPT_WRITEFUNCTION, output);
    rc = curl_easy_perform(curl);
done:
    if (rc != CURLE_OK) fprintf(stderr, "%s\n", curl_easy_strerror(rc));
    curl_easy_cleanup(curl); curl_global_cleanup();
    return rc != CURLE_OK;
}
