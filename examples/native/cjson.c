#include <cjson/cJSON.h>
#include <stdio.h>
int main(void) {
    cJSON *root = cJSON_Parse("{\"text\":\"PCM\\nexample\",\"rate\":16000}");
    if (!root) return 1;
    const cJSON *text = cJSON_GetObjectItemCaseSensitive(root, "text");
    const cJSON *rate = cJSON_GetObjectItemCaseSensitive(root, "rate");
    int ok = cJSON_IsString(text) && text->valuestring && cJSON_IsNumber(rate);
    if (ok) printf("text=%s rate=%.0f\n", text->valuestring, rate->valuedouble);
    cJSON_Delete(root);
    return !ok;
}
