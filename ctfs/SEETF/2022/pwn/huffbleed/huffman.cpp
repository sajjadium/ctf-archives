#include <algorithm>
#include <cstring>
#include <map>
#include <memory>
#include <queue>
using namespace std;

struct headerSize {
    uint8_t size : 6;
    bool isTwoByte : 1, isHuffman : 1;
};

union smallNode {
    uint8_t code;
    struct {
        uint8_t skip : 6;
        bool isLeftLeaf : 1, isRightLeaf : 1;
        bool isLeaf(int dir) { return dir == 0 ? isLeftLeaf : isRightLeaf; }
    } branch;
};

struct node {
    uint8_t code;
    int freq;
    shared_ptr<node> left, right;

    node(uint8_t code, int freq) :
        code(code), freq(freq) {}
    node(shared_ptr<node> left, shared_ptr<node> right) :
        code(), freq(left->freq + right->freq), left(left), right(right) {}
    bool isLeaf() { return !left; }
};

/**
 * Compresses an array of bytes using huffman coding (or raw as a fallback, if that is smaller)
 *
 * @param p_inbuf A pointer to the input buffer
 * @param inlen The length of the input (should be no larger than 16447)
 * @param p_outbuf A pointer to the output buffer
 * @return The length of the output (compressed) buffer, which will be no larger than inlen + 2
 */
size_t encode(const void* p_inbuf, size_t inlen, void* p_outbuf) {
    // write the size into the header, except isHuffman which will be set later
    auto inbuf = (const uint8_t*)p_inbuf;
    auto outbuf = (uint8_t*)p_outbuf, outptr = outbuf;
    auto isTwoByte = inlen >= 64;
    *(headerSize*)outptr++ = { (uint8_t)inlen, isTwoByte, false };
    if (isTwoByte) *outptr++ = (inlen >> 6) - 1;
    
    // special case: the empty input
    if (inlen == 0) return 1;

    // keep a frequency table of the bytes (and some space to store the huffman code)
    map<uint8_t, pair<int, string>> map;
    for_each(inbuf, inbuf + inlen, [&map](uint8_t c) { map[c].first++; });

    // construct huffman tree
    deque<shared_ptr<node>> dq;
    for (auto& pair : map)
        dq.emplace_back(make_shared<node>(pair.first, pair.second.first));
    while (dq.size() > 1) {
        stable_sort(dq.begin(), dq.end(), [](auto p, auto q) { return p->freq < q->freq; });
        dq.emplace_back(make_shared<node>(dq[1], dq[0]));
        dq.erase(dq.begin(), dq.begin() + 2);
    }

    // build huffman codes recursively
    auto build = [&map](auto _build, auto child, string acc = "") -> void {
        if (child->isLeaf())
            map[child->code].second = acc;
        else {
            _build(_build, child->left, acc + "0");
            _build(_build, child->right, acc + "1");
        }
    };
    build(build, dq[0]);

    // calculate length of huffman-encoded bitstream
    int bitLength = 0;
    for (auto& pair : map)
        bitLength += pair.second.first * pair.second.second.length();
    int byteLength = (bitLength + 7) / 8;
    
    // if it can't be compressed, then we just keep the raw data
    if (byteLength + map.size() * 2 >= inlen) {
        memcpy(outptr, inbuf, inlen);
        return (outptr - outbuf) + inlen;
    }
    
    // if we reach here, that means it's compressible, so mark it as huffman
    ((headerSize*)outbuf)->isHuffman = true;
    *outptr++ = (uint8_t)map.size() - 1;

    // reorder the nodes in a logical way for the header
    vector<shared_ptr<node>> headerNodes { dq[0] };
    if (dq[0]->isLeaf()) dq.clear();
    while (dq.size()) {
        // find the best node to place next in the header
        auto bestIndex = 0u;
        for (auto i = 1u; i < dq.size(); i++)
            if (dq[i]->code - i < dq[bestIndex]->code - bestIndex)
                bestIndex = i;

        // calculate distance to parent
        auto bestNode{ dq[bestIndex] };
        dq.erase(dq.begin() + bestIndex);
        uint8_t skip = headerNodes.size() / 2 - bestNode->code;
        smallNode sn{ .branch = { skip, bestNode->left->isLeaf(), bestNode->right->isLeaf() } };
        bestNode->code = sn.code;

        // add children to the queue
        for (auto& child : { bestNode->left, bestNode->right }) {
            headerNodes.push_back(child);
            if (!child->isLeaf()) {
                child->code = headerNodes.size() / 2;
                dq.push_back(child);
            }
        }
    }

    // write out headerNodes into the buffer
    for (auto i = 0u; i < headerNodes.size(); i++)
        *outptr++ = headerNodes[i]->code;

    // write out all bits
    fill(outptr, outptr + byteLength, 0);
    for (auto i = 0u, bitIndex = 0u; i < inlen; i++)
        for (auto c : map[inbuf[i]].second) {
            if (c == '1')
                outptr[bitIndex / 8] |= 1 << bitIndex % 8;
            bitIndex++;
        }

    return (outptr - outbuf) + byteLength;
}

/**
 * Decompresses an array of bytes that was compressed with encode()
 *
 * @param p_inbuf A pointer to the input buffer
 * @param p_outbuf A pointer to the output buffer
 * @return The length of the output (decompressed) buffer
 */
size_t decode(const void* p_inbuf, void* p_outbuf) {
    // read header metadata
    auto inbuf = (const uint8_t*)p_inbuf;
    auto headerByte = (headerSize*)inbuf++;
    size_t len = headerByte->size;
    if (headerByte->isTwoByte) len |= (*inbuf++ + 1) << 6;
    const smallNode* sn = (smallNode*)inbuf;
    
    if (!headerByte->isHuffman)
        memcpy(p_outbuf, inbuf, len); // data was not compressible, copy the raw data
    else if (!sn->code)
        memset(p_outbuf, sn[1].code, len); // special case: single element repeated throughout
    else {
        int bitIndex = (1 + sn->code) * 16, nextPos = 1;
        for (auto outptr = (uint8_t*)p_outbuf, end = outptr + len; outptr < end; ) {
            auto curr = sn[nextPos].branch;
            nextPos = 2 * (nextPos / 2 + curr.skip + 1) | (inbuf[bitIndex / 8] >> (bitIndex % 8) & 1);
            bitIndex++;
            if (curr.isLeaf(nextPos & 1)) {
                *outptr++ = sn[nextPos].code;
                nextPos = 1;
            }
        }
    }
    return len;
}
