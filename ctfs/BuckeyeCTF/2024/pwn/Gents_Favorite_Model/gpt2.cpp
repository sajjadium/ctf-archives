/* Based on: https://github.com/karpathy/llm.c/tree/48fee049cbf571eb44acdf7b174df71b6d7bfcb1 */

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdint.h>
#include <assert.h>
#include <math.h>
#include <time.h>
#include <string.h>
#include <unistd.h>

void print_flag()
{
    char *flag = getenv("FLAG");
    printf("woah, how did you get here?\n");
    if (flag == nullptr) {
        printf("bctf{fake_flag}\n");
    } else {
        printf("%s\n", flag);
    }
}

// ----------------------------------------------------------------------------
// fread convenience utils, with nice handling of error checking using macros
// simple replace fopen, fread, fclose, fseek
// with fopenCheck, freadCheck, fcloseCheck, fseekCheck

extern inline FILE *fopen_check(const char *path, const char *mode, const char *file, int line)
{
    FILE *fp = fopen(path, mode);
    if (fp == NULL)
    {
        fprintf(stderr, "Error: Failed to open file '%s' at %s:%d\n", path, file, line);
        exit(EXIT_FAILURE);
    }
    return fp;
}

#define fopenCheck(path, mode) fopen_check(path, mode, __FILE__, __LINE__)

extern inline void fread_check(void *ptr, size_t size, size_t nmemb, FILE *stream, const char *file, int line)
{
    size_t result = fread(ptr, size, nmemb, stream);
    if (result != nmemb)
    {
        if (feof(stream))
        {
            fprintf(stderr, "Error: Unexpected end of file at %s:%d\n", file, line);
        }
        else if (ferror(stream))
        {
            fprintf(stderr, "Error: File read error at %s:%d\n", file, line);
        }
        else
        {
            fprintf(stderr, "Error: Partial read at %s:%d. Expected %zu elements, read %zu\n",
                    file, line, nmemb, result);
        }
        exit(EXIT_FAILURE);
    }
}

#define freadCheck(ptr, size, nmemb, stream) fread_check(ptr, size, nmemb, stream, __FILE__, __LINE__)

extern inline void fclose_check(FILE *fp, const char *file, int line)
{
    if (fclose(fp) != 0)
    {
        fprintf(stderr, "Error: Failed to close file at %s:%d\n", file, line);
        exit(EXIT_FAILURE);
    }
}

#define fcloseCheck(fp) fclose_check(fp, __FILE__, __LINE__)

extern inline void fseek_check(FILE *fp, long off, int whence, const char *file, int line)
{
    if (fseek(fp, off, whence) != 0)
    {
        fprintf(stderr, "Error: Failed to seek in file at %s:%d\n", file, line);
        exit(EXIT_FAILURE);
    }
}

#define fseekCheck(fp, off, whence) fseek_check(fp, off, whence, __FILE__, __LINE__)

extern inline void fwrite_check(void *ptr, size_t size, size_t nmemb, FILE *stream, const char *file, int line)
{
    size_t result = fwrite(ptr, size, nmemb, stream);
    if (result != nmemb)
    {
        if (feof(stream))
        {
            fprintf(stderr, "Error: Unexpected end of file at %s:%d\n", file, line);
        }
        else if (ferror(stream))
        {
            fprintf(stderr, "Error: File write error at %s:%d\n", file, line);
        }
        else
        {
            fprintf(stderr, "Error: Partial write at %s:%d. Expected %zu elements, wrote %zu\n",
                    file, line, nmemb, result);
        }
        fprintf(stderr, "Error details:\n");
        exit(EXIT_FAILURE);
    }
}

#define fwriteCheck(ptr, size, nmemb, stream) fwrite_check(ptr, size, nmemb, stream, __FILE__, __LINE__)

// ----------------------------------------------------------------------------
// malloc error-handling wrapper util

extern inline void *malloc_check(size_t size, const char *file, int line)
{
    void *ptr = malloc(size);
    if (ptr == NULL)
    {
        fprintf(stderr, "Error: Memory allocation failed at %s:%d\n", file, line);
        exit(EXIT_FAILURE);
    }
    return ptr;
}

#define mallocCheck(size) malloc_check(size, __FILE__, __LINE__)

// ----------------------------------------------------------------------------
// check that all tokens are within range
extern inline void token_check(const int *tokens, int token_count, int vocab_size, const char *file, int line)
{
    for (int i = 0; i < token_count; i++)
    {
        if (!(0 <= tokens[i] && tokens[i] < vocab_size))
        {
            fprintf(stderr, "Error: Token out of vocabulary at %s:%d\n", file, line);
            exit(EXIT_FAILURE);
        }
    }
}
#define tokenCheck(tokens, count, vocab) token_check(tokens, count, vocab, __FILE__, __LINE__)

class Tokenizer
{
private:
    uint32_t vocab_size;
    char **token_table;

public:
    int init_ok;
    int eot_token;
    void safe_printf(const char *piece);
    Tokenizer(const char *filename);
    const char *decode_token(uint32_t token_id);
    uint32_t *encode_string(const char *text);
    ~Tokenizer();
};

void Tokenizer::safe_printf(const char *piece)
{
    if (piece == NULL)
    {
        return;
    }
    if (piece[0] == '\0')
    {
        return;
    }
    if (piece[1] == '\0')
    {
        unsigned char byte_val = piece[0];
        if (!(isprint(byte_val) || isspace(byte_val)))
        {
            return;
        }
    }
    printf("%s", piece);
}

Tokenizer::Tokenizer(const char *filename)
{
    FILE *file = fopen(filename, "rb");
    if (file == NULL)
    {
        printf("WARNING: Failed to open the tokenizer file %s\n", filename);
        this->init_ok = 0;
        return;
    }
    uint32_t header[256];
    freadCheck(header, sizeof(uint32_t), 256, file);
    assert(header[0] == 20240328);
    int version = header[1];
    this->vocab_size = header[2];
    if (version == 1)
    {
        assert(this->vocab_size == 50257);
        this->eot_token = 50256;
    }
    else if (version == 2)
    {
        this->eot_token = header[3];
    }
    else
    {
        fprintf(stderr, "Tokenizer model file %s has bad version: %d\n", filename, version);
        exit(EXIT_FAILURE);
    }
    unsigned char length;
    this->token_table = (char **)mallocCheck(this->vocab_size * sizeof(char *));
    for (uint32_t i = 0; i < this->vocab_size; i++)
    {
        freadCheck(&length, sizeof(unsigned char), 1, file);
        assert(length > 0);
        char *token_bytes = (char *)mallocCheck(length + 1);
        freadCheck(token_bytes, sizeof(char), length, file);
        token_bytes[length] = '\0';
        this->token_table[i] = token_bytes;
    }
    fcloseCheck(file);
    this->init_ok = 1;
}

const char *Tokenizer::decode_token(uint32_t token_id)
{
    if (this->init_ok == 0)
    {
        return NULL;
    }
    if (token_id < this->vocab_size)
    {
        return this->token_table[token_id];
    }
    else
    {
        printf("invalid token id %u!\n", token_id);
        return NULL;
    }
}

uint32_t *Tokenizer::encode_string(const char *text)
{
    if (this->init_ok == 0)
    {
        return NULL;
    }

    size_t text_len = strlen(text);
    uint32_t *tokens = (uint32_t *)mallocCheck((text_len + 1) * sizeof(uint32_t));
    size_t token_count = 0;

    for (size_t i = 0; i < text_len;)
    {
        size_t longest_match = 0;
        uint32_t best_token = this->eot_token;

        for (uint32_t j = 0; j < this->vocab_size; j++)
        {
            size_t token_len = strlen(this->token_table[j]);
            if (token_len > 0 && token_len <= text_len - i && strncmp(text + i, this->token_table[j], token_len) == 0)
            {
                if (token_len > longest_match)
                {
                    longest_match = token_len;
                    best_token = j;
                }
            }
        }

        if (longest_match == 0)
        {
            fprintf(stderr, "Error: No matching token found for text starting at position %zu\n", i);
            free(tokens);
            return NULL;
        }

        tokens[token_count++] = best_token;
        i += longest_match;
    }

    tokens[token_count++] = this->eot_token;
    return tokens;
}

Tokenizer::~Tokenizer()
{
    if (this->init_ok)
    {
        for (uint32_t i = 0; i < this->vocab_size; i++)
        {
            free(this->token_table[i]);
        }
        free(this->token_table);
    }
}

// ----------------------------------------------------------------------------
// all the individual layers' forward passes
// B = batch_size, T = sequence_length, C = channels, V = vocab_size

void encoder_forward(float *out,
                     int *inp, float *wte, float *wpe,
                     int B, int T, int C)
{
    for (int b = 0; b < B; b++)
    {
        for (int t = 0; t < T; t++)
        {
            float *out_bt = out + b * T * C + t * C;
            int ix = inp[b * T + t];
            float *wte_ix = wte + ix * C;
            float *wpe_t = wpe + t * C;
            for (int i = 0; i < C; i++)
            {
                out_bt[i] = wte_ix[i] + wpe_t[i];
            }
        }
    }
}

void layernorm_forward(float *out, float *mean, float *rstd,
                       float *inp, float *weight, float *bias,
                       int B, int T, int C)
{
    float eps = 1e-5f;
    for (int b = 0; b < B; b++)
    {
        for (int t = 0; t < T; t++)
        {
            float *x = inp + b * T * C + t * C;
            float m = 0.0f;
            for (int i = 0; i < C; i++)
            {
                m += x[i];
            }
            m = m / C;
            float v = 0.0f;
            for (int i = 0; i < C; i++)
            {
                float xshift = x[i] - m;
                v += xshift * xshift;
            }
            v = v / C;
            float s = 1.0f / sqrtf(v + eps);
            float *out_bt = out + b * T * C + t * C;
            for (int i = 0; i < C; i++)
            {
                float n = (s * (x[i] - m));
                float o = n * weight[i] + bias[i];
                out_bt[i] = o;
            }
            mean[b * T + t] = m;
            rstd[b * T + t] = s;
        }
    }
}

void matmul_forward_naive(float *out,
                          const float *inp, const float *weight, const float *bias,
                          int B, int T, int C, int OC)
{
    for (int b = 0; b < B; b++)
    {
        for (int t = 0; t < T; t++)
        {
            int bt = b * T + t;
            for (int o = 0; o < OC; o++)
            {
                float val = (bias != NULL) ? bias[o] : 0.0f;
                for (int i = 0; i < C; i++)
                {
                    val += inp[bt * C + i] * weight[o * C + i];
                }
                out[bt * OC + o] = val;
            }
        }
    }
}

void matmul_forward(float *out,
                    const float *inp, const float *weight, const float *bias,
                    int B, int T, int C, int OC)
{
    const int LOOP_UNROLL = 8;
    if (B * T % LOOP_UNROLL != 0)
    {
        matmul_forward_naive(out, inp, weight, bias, B, T, C, OC);
        return;
    }
    for (int obt = 0; obt < B * T; obt += LOOP_UNROLL)
    {
        for (int o = 0; o < OC; o++)
        {
            float result[LOOP_UNROLL];
            for (int ibt = 0; ibt < LOOP_UNROLL; ibt++)
            {
                result[ibt] = (bias != NULL) ? bias[o] : 0.0f;
            }
            for (int i = 0; i < C; i++)
            {
                float w = weight[i + o * C];
                for (int ibt = 0; ibt < LOOP_UNROLL; ibt++)
                {
                    int bt = obt + ibt;
                    result[ibt] += inp[bt * C + i] * w;
                }
            }
            for (int ibt = 0; ibt < LOOP_UNROLL; ibt++)
            {
                int bt = obt + ibt;
                out[bt * OC + o] = result[ibt];
            }
        }
    }
}

void attention_forward(float *out, float *preatt, float *att,
                       float *inp,
                       int B, int T, int C, int NH)
{
    int C3 = C * 3;
    int hs = C / NH;
    float scale = 1.0 / sqrtf(hs);

    for (int b = 0; b < B; b++)
    {
        for (int t = 0; t < T; t++)
        {
            for (int h = 0; h < NH; h++)
            {
                float *query_t = inp + b * T * C3 + t * C3 + h * hs;
                float *preatt_bth = preatt + b * NH * T * T + h * T * T + t * T;
                float *att_bth = att + b * NH * T * T + h * T * T + t * T;

                float maxval = -10000.0f;
                for (int t2 = 0; t2 <= t; t2++)
                {
                    float *key_t2 = inp + b * T * C3 + t2 * C3 + h * hs + C;
                    float val = 0.0f;
                    for (int i = 0; i < hs; i++)
                    {
                        val += query_t[i] * key_t2[i];
                    }
                    val *= scale;
                    if (val > maxval)
                    {
                        maxval = val;
                    }

                    preatt_bth[t2] = val;
                }

                float expsum = 0.0f;
                for (int t2 = 0; t2 <= t; t2++)
                {
                    float expv = expf(preatt_bth[t2] - maxval);
                    expsum += expv;
                    att_bth[t2] = expv;
                }
                float expsum_inv = expsum == 0.0f ? 0.0f : 1.0f / expsum;

                for (int t2 = 0; t2 < T; t2++)
                {
                    if (t2 <= t)
                    {
                        att_bth[t2] *= expsum_inv;
                    }
                    else
                    {
                        att_bth[t2] = 0.0f;
                    }
                }

                float *out_bth = out + b * T * C + t * C + h * hs;
                for (int i = 0; i < hs; i++)
                {
                    out_bth[i] = 0.0f;
                }
                for (int t2 = 0; t2 <= t; t2++)
                {
                    float *value_t2 = inp + b * T * C3 + t2 * C3 + h * hs + C * 2;
                    float att_btht2 = att_bth[t2];
                    for (int i = 0; i < hs; i++)
                    {
                        out_bth[i] += att_btht2 * value_t2[i];
                    }
                }
            }
        }
    }
}

#define GELU_SCALING_FACTOR sqrtf(2.0f / M_PI)
void gelu_forward(float *out, float *inp, int N)
{
    for (int i = 0; i < N; i++)
    {
        float x = inp[i];
        float cube = 0.044715f * x * x * x;
        out[i] = 0.5f * x * (1.0f + tanhf(GELU_SCALING_FACTOR * (x + cube)));
    }
}

void residual_forward(float *out, float *inp1, float *inp2, int N)
{
    for (int i = 0; i < N; i++)
    {
        out[i] = inp1[i] + inp2[i];
    }
}

void softmax_forward(float *probs, float *logits, int B, int T, int V, int Vp)
{
    for (int b = 0; b < B; b++)
    {
        for (int t = 0; t < T; t++)
        {
            float *logits_bt = logits + b * T * Vp + t * Vp;
            float *probs_bt = probs + b * T * Vp + t * Vp;

            float maxval = -10000.0f;
            for (int i = 0; i < V; i++)
            {
                if (logits_bt[i] > maxval)
                {
                    maxval = logits_bt[i];
                }
            }
            float sum = 0.0f;
            for (int i = 0; i < V; i++)
            {
                probs_bt[i] = expf(logits_bt[i] - maxval);
                sum += probs_bt[i];
            }
            for (int i = 0; i < V; i++)
            {
                probs_bt[i] /= sum;
            }
            for (int i = V; i < Vp; i++)
            {
                probs_bt[i] = 0.0f;
            }
        }
    }
}

// ----------------------------------------------------------------------------
// sampler

unsigned int random_u32(uint64_t *state)
{
    *state ^= *state >> 12;
    *state ^= *state << 25;
    *state ^= *state >> 27;
    return (*state * 0x2545F4914F6CDD1Dull) >> 32;
}
float random_f32(uint64_t *state)
{
    return (random_u32(state) >> 8) / 16777216.0f;
}

int sample_mult(float *probabilities, int n, float coin)
{
    float cdf = 0.0f;
    for (int i = 0; i < n; i++)
    {
        cdf += probabilities[i];
        if (coin < cdf)
        {
            return i;
        }
    }
    return n - 1;
}

// ----------------------------------------------------------------------------
// GPT-2 model definition

typedef struct
{
    int max_seq_len;
    int vocab_size;
    int padded_vocab_size;
    int num_layers;
    int num_heads;
    int channels;
} GPT2Config;

#define NUM_PARAMETER_TENSORS 16
typedef struct
{
    float *wte;
    float *wpe;
    float *ln1w;
    float *ln1b;
    float *qkvw;
    float *qkvb;
    float *attprojw;
    float *attprojb;
    float *ln2w;
    float *ln2b;
    float *fcw;
    float *fcb;
    float *fcprojw;
    float *fcprojb;
    float *lnfw;
    float *lnfb;
} ParameterTensors;

void fill_in_parameter_sizes(size_t *param_sizes, GPT2Config config)
{
    size_t Vp = config.padded_vocab_size;
    size_t C = config.channels;
    size_t maxT = config.max_seq_len;
    size_t L = config.num_layers;
    param_sizes[0] = Vp * C;
    param_sizes[1] = maxT * C;
    param_sizes[2] = L * C;
    param_sizes[3] = L * C;
    param_sizes[4] = L * (3 * C) * C;
    param_sizes[5] = L * (3 * C);
    param_sizes[6] = L * C * C;
    param_sizes[7] = L * C;
    param_sizes[8] = L * C;
    param_sizes[9] = L * C;
    param_sizes[10] = L * (4 * C) * C;
    param_sizes[11] = L * (4 * C);
    param_sizes[12] = L * C * (4 * C);
    param_sizes[13] = L * C;
    param_sizes[14] = C;
    param_sizes[15] = C;
}

// allocate memory for the parameters and point the individual tensors to the right places
float *malloc_and_point_parameters(ParameterTensors *params, size_t *param_sizes)
{
    size_t num_parameters = 0;
    for (size_t i = 0; i < NUM_PARAMETER_TENSORS; i++)
    {
        num_parameters += param_sizes[i];
    }
    float *params_memory = (float *)mallocCheck(num_parameters * sizeof(float));
    float **ptrs[] = {
        &params->wte, &params->wpe, &params->ln1w, &params->ln1b, &params->qkvw, &params->qkvb,
        &params->attprojw, &params->attprojb, &params->ln2w, &params->ln2b, &params->fcw, &params->fcb,
        &params->fcprojw, &params->fcprojb, &params->lnfw, &params->lnfb};
    float *params_memory_iterator = params_memory;
    for (size_t i = 0; i < NUM_PARAMETER_TENSORS; i++)
    {
        *(ptrs[i]) = params_memory_iterator;
        params_memory_iterator += param_sizes[i];
    }
    return params_memory;
}

#define NUM_ACTIVATION_TENSORS 23
typedef struct
{
    float *encoded;
    float *ln1;
    float *ln1_mean;
    float *ln1_rstd;
    float *qkv;
    float *atty;
    float *preatt;
    float *att;
    float *attproj;
    float *residual2;
    float *ln2;
    float *ln2_mean;
    float *ln2_rstd;
    float *fch;
    float *fch_gelu;
    float *fcproj;
    float *residual3;
    float *lnf;
    float *lnf_mean;
    float *lnf_rstd;
    float *logits;
    float *probs;
    float *losses;
} ActivationTensors;

float *malloc_and_point_activations(ActivationTensors *acts, size_t *act_sizes)
{
    size_t num_activations = 0;
    for (size_t i = 0; i < NUM_ACTIVATION_TENSORS; i++)
    {
        num_activations += act_sizes[i];
    }
    float *acts_memory = (float *)mallocCheck(num_activations * sizeof(float));
    float **ptrs[] = {
        &acts->encoded, &acts->ln1, &acts->ln1_mean, &acts->ln1_rstd, &acts->qkv, &acts->atty,
        &acts->preatt, &acts->att, &acts->attproj, &acts->residual2, &acts->ln2, &acts->ln2_mean,
        &acts->ln2_rstd, &acts->fch, &acts->fch_gelu, &acts->fcproj, &acts->residual3, &acts->lnf,
        &acts->lnf_mean, &acts->lnf_rstd, &acts->logits, &acts->probs, &acts->losses};
    float *acts_memory_iterator = acts_memory;
    for (size_t i = 0; i < NUM_ACTIVATION_TENSORS; i++)
    {
        *(ptrs[i]) = acts_memory_iterator;
        acts_memory_iterator += act_sizes[i];
    }
    return acts_memory;
}

const int B = 1;  // batch size 1
const int T = 64; // sequence length <= 1024

void special_copy(uint16_t *src, int *dst, size_t n) {
    for (size_t i = 0; i < n; i++) {
        dst[i] = (uint32_t)src[i];
    }
}

class GPT2
{
private:
    GPT2Config config;
    ParameterTensors params;
    size_t param_sizes[NUM_PARAMETER_TENSORS];
    float *params_memory;
    size_t num_parameters;
    ParameterTensors grads;
    float *grads_memory;
    float *m_memory;
    float *v_memory;
    ActivationTensors acts;
    size_t act_sizes[NUM_ACTIVATION_TENSORS];
    float *acts_memory;
    size_t num_activations;
    ActivationTensors grads_acts;
    float *grads_acts_memory;
    int batch_size;
    int seq_len;
    int *inputs;
    float mean_loss;
    Tokenizer tokenizer;
    uint16_t gen_tokens[B * T];
    uint64_t rng_state;
    const uint16_t genT;
    void forward(size_t B, size_t T);

public:
    GPT2(const char *checkpoint_path, const char *filename);
    ~GPT2();
    void chat();
};

GPT2::GPT2(const char *checkpoint_path, const char *filename)
    : tokenizer(filename), genT(T)
{
    FILE *model_file = fopenCheck(checkpoint_path, "rb");
    if (model_file == NULL)
    {
        printf("Error opening model file\n");
        exit(1);
    }
    int model_header[256];
    freadCheck(model_header, sizeof(int), 256, model_file);
    if (model_header[0] != 20240326)
    {
        printf("Bad magic model file\n");
        exit(1);
    }
    if (model_header[1] != 3)
    {
        printf("Bad version in model file\n");
        printf("---> HINT: try to re-run `python train_gpt2.py`\n");
        exit(1);
    }

    size_t maxT, V, Vp, L, NH, C;
    this->config.max_seq_len = maxT = model_header[2];
    this->config.vocab_size = V = model_header[3];
    this->config.num_layers = L = model_header[4];
    this->config.num_heads = NH = model_header[5];
    this->config.channels = C = model_header[6];
    this->config.padded_vocab_size = Vp = model_header[7];

    fill_in_parameter_sizes(this->param_sizes, this->config);

    size_t num_parameters = 0;
    for (size_t i = 0; i < NUM_PARAMETER_TENSORS; i++)
    {
        num_parameters += this->param_sizes[i];
    }
    this->num_parameters = num_parameters;

    this->params_memory = malloc_and_point_parameters(&this->params, this->param_sizes);
    freadCheck(this->params_memory, sizeof(float), num_parameters, model_file);
    fcloseCheck(model_file);

    this->acts_memory = NULL;
    this->grads_memory = NULL;
    this->m_memory = NULL;
    this->v_memory = NULL;
    this->grads_acts_memory = NULL;
    this->inputs = NULL;
    this->batch_size = 0;
    this->seq_len = 0;
    this->mean_loss = -1.0f;
}

void GPT2::forward(size_t B, size_t T)
{
    if (this->params_memory == NULL)
    {
        printf("Error: model was not initialized properly.\n");
        exit(1);
    }

    size_t V = this->config.vocab_size;
    size_t Vp = this->config.padded_vocab_size;
    size_t L = this->config.num_layers;
    size_t NH = this->config.num_heads;
    size_t C = this->config.channels;

    for (int i = 0; i < B * T; i++)
    {
        assert(0 <= gen_tokens[i] && gen_tokens[i] < V);
    }

    if (this->acts_memory == NULL)
    {
        this->batch_size = B;
        this->seq_len = T;
        this->act_sizes[0] = B * T * C;
        this->act_sizes[1] = L * B * T * C;
        this->act_sizes[2] = L * B * T;
        this->act_sizes[3] = L * B * T;
        this->act_sizes[4] = L * B * T * 3 * C;
        this->act_sizes[5] = L * B * T * C;
        this->act_sizes[6] = L * B * NH * T * T;
        this->act_sizes[7] = L * B * NH * T * T;
        this->act_sizes[8] = L * B * T * C;
        this->act_sizes[9] = L * B * T * C;
        this->act_sizes[10] = L * B * T * C;
        this->act_sizes[11] = L * B * T;
        this->act_sizes[12] = L * B * T;
        this->act_sizes[13] = L * B * T * 4 * C;
        this->act_sizes[14] = L * B * T * 4 * C;
        this->act_sizes[15] = L * B * T * C;
        this->act_sizes[16] = L * B * T * C;
        this->act_sizes[17] = B * T * C;
        this->act_sizes[18] = B * T;
        this->act_sizes[19] = B * T;
        this->act_sizes[20] = B * T * Vp;
        this->act_sizes[21] = B * T * Vp;
        this->act_sizes[22] = B * T;
        size_t num_activations = 0;
        for (size_t i = 0; i < NUM_ACTIVATION_TENSORS; i++)
        {
            num_activations += this->act_sizes[i];
        }
        this->num_activations = num_activations;
        this->acts_memory = malloc_and_point_activations(&this->acts, this->act_sizes);
        this->inputs = (int *)mallocCheck(B * T * sizeof(int));
    }
    else
    {
        if (B != this->batch_size || T != this->seq_len)
        {
            printf("Model: B=%d T=%d, Desired: B=%d T=%d\n", this->batch_size, this->seq_len, (int)B, (int)T);
            exit(EXIT_FAILURE);
        }
    }

    special_copy(gen_tokens, this->inputs, B * T * sizeof(int));

    ParameterTensors params = this->params;
    ActivationTensors acts = this->acts;
    float *residual;
    encoder_forward(acts.encoded, this->inputs, params.wte, params.wpe, B, T, C);
    for (int l = 0; l < L; l++)
    {

        residual = l == 0 ? acts.encoded : acts.residual3 + (l - 1) * B * T * C;

        float *l_ln1w = params.ln1w + l * C;
        float *l_ln1b = params.ln1b + l * C;
        float *l_qkvw = params.qkvw + l * 3 * C * C;
        float *l_qkvb = params.qkvb + l * 3 * C;
        float *l_attprojw = params.attprojw + l * C * C;
        float *l_attprojb = params.attprojb + l * C;
        float *l_ln2w = params.ln2w + l * C;
        float *l_ln2b = params.ln2b + l * C;
        float *l_fcw = params.fcw + l * 4 * C * C;
        float *l_fcb = params.fcb + l * 4 * C;
        float *l_fcprojw = params.fcprojw + l * C * 4 * C;
        float *l_fcprojb = params.fcprojb + l * C;

        float *l_ln1 = acts.ln1 + l * B * T * C;
        float *l_ln1_mean = acts.ln1_mean + l * B * T;
        float *l_ln1_rstd = acts.ln1_rstd + l * B * T;
        float *l_qkv = acts.qkv + l * B * T * 3 * C;
        float *l_atty = acts.atty + l * B * T * C;
        float *l_preatt = acts.preatt + l * B * NH * T * T;
        float *l_att = acts.att + l * B * NH * T * T;
        float *l_attproj = acts.attproj + l * B * T * C;
        float *l_residual2 = acts.residual2 + l * B * T * C;
        float *l_ln2 = acts.ln2 + l * B * T * C;
        float *l_ln2_mean = acts.ln2_mean + l * B * T;
        float *l_ln2_rstd = acts.ln2_rstd + l * B * T;
        float *l_fch = acts.fch + l * B * T * 4 * C;
        float *l_fch_gelu = acts.fch_gelu + l * B * T * 4 * C;
        float *l_fcproj = acts.fcproj + l * B * T * C;
        float *l_residual3 = acts.residual3 + l * B * T * C;

        layernorm_forward(l_ln1, l_ln1_mean, l_ln1_rstd, residual, l_ln1w, l_ln1b, B, T, C);
        matmul_forward(l_qkv, l_ln1, l_qkvw, l_qkvb, B, T, C, 3 * C);
        attention_forward(l_atty, l_preatt, l_att, l_qkv, B, T, C, NH);
        matmul_forward(l_attproj, l_atty, l_attprojw, l_attprojb, B, T, C, C);
        residual_forward(l_residual2, residual, l_attproj, B * T * C);
        layernorm_forward(l_ln2, l_ln2_mean, l_ln2_rstd, l_residual2, l_ln2w, l_ln2b, B, T, C);
        matmul_forward(l_fch, l_ln2, l_fcw, l_fcb, B, T, C, 4 * C);
        gelu_forward(l_fch_gelu, l_fch, B * T * 4 * C);
        matmul_forward(l_fcproj, l_fch_gelu, l_fcprojw, l_fcprojb, B, T, 4 * C, C);
        residual_forward(l_residual3, l_residual2, l_fcproj, B * T * C);
    }
    residual = acts.residual3 + (L - 1) * B * T * C;
    layernorm_forward(acts.lnf, acts.lnf_mean, acts.lnf_rstd, residual, params.lnfw, params.lnfb, B, T, C);
    matmul_forward(acts.logits, acts.lnf, params.wte, NULL, B, T, C, Vp);
    softmax_forward(acts.probs, acts.logits, B, T, V, Vp);
}

void GPT2::chat()
{
    char user_input[256];
    printf("Inspire me: ");
    fgets(user_input, sizeof(user_input), stdin);
    user_input[strcspn(user_input, "\n")] = 0;
    const char *user_input_ptr = user_input;
    uint32_t *tokens = tokenizer.encode_string(user_input_ptr);

    for (int i = 0; i < B * T; ++i)
    {
        gen_tokens[i] = (uint16_t)tokenizer.eot_token;
    }

    int start_pos = 0;
    for (int i = 0; tokens[i] != tokenizer.eot_token; i++)
    {
        gen_tokens[i] = (uint16_t)tokens[i];
        start_pos = i;
        if (tokenizer.init_ok)
        {
            const char *token_str = tokenizer.decode_token(tokens[i]);
            tokenizer.safe_printf(token_str);
        }
    }
    start_pos++;

    for (int t = start_pos; t < genT; t++)
    {
        forward(B, T);
        float *probs = acts.probs + (t - 1) * config.padded_vocab_size;
        float coin = random_f32(&rng_state);
        int next_token = sample_mult(probs, config.vocab_size, coin);
        gen_tokens[t] = next_token;
        if (tokenizer.init_ok)
        {
            const char *token_str = tokenizer.decode_token(next_token);
            tokenizer.safe_printf(token_str);
        }
        else
        {
            printf("%d ", next_token);
        }
    }
}

GPT2::~GPT2()
{
    free(this->params_memory);
    free(this->grads_memory);
    free(this->m_memory);
    free(this->v_memory);
    free(this->acts_memory);
    free(this->grads_acts_memory);
    free(this->inputs);
}

__attribute__((noinline))
void chall()
{
    GPT2 model = GPT2("gpt2_124M.bin", "gpt2_tokenizer.bin");
    model.chat();
}

// ----------------------------------------------------------------------------
// main
int main()
{
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);

    chall();
    return 0;
}
