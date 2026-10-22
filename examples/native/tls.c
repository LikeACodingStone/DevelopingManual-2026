#include <openssl/ssl.h>
#include <openssl/err.h>
#include <signal.h>
#include <stdio.h>
#include <string.h>
/* OpenSSL >= 1.1.1. HOST is a DNS name, not a URL. */
int main(int argc, char **argv) {
    if (argc != 2 || !*argv[1] || strpbrk(argv[1], "\r\n/: ")) {
        fprintf(stderr, "usage: tls DNS_HOST\n"); return 2;
    }
    signal(SIGPIPE, SIG_IGN);
    SSL_CTX *ctx = SSL_CTX_new(TLS_client_method());
    if (!ctx) return 1;
    SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER, NULL);
    int ok = SSL_CTX_set_min_proto_version(ctx, TLS1_2_VERSION) &&
             SSL_CTX_set_default_verify_paths(ctx);
    BIO *bio = ok ? BIO_new_ssl_connect(ctx) : NULL;
    SSL *ssl = NULL;
    if (bio) BIO_get_ssl(bio, &ssl);
    ok = ssl && SSL_set_tlsext_host_name(ssl, argv[1]) && SSL_set1_host(ssl, argv[1]);
    if (ok) {
        BIO_set_conn_hostname(bio, argv[1]);
        BIO_set_conn_port(bio, "443");
        ok = BIO_do_connect(bio) > 0 && BIO_do_handshake(bio) > 0 &&
             SSL_get_verify_result(ssl) == X509_V_OK;
    }
    if (ok) printf("TLS verified: %s\n", SSL_get_version(ssl));
    else ERR_print_errors_fp(stderr);
    BIO_free_all(bio); SSL_CTX_free(ctx);
    return !ok;
}
