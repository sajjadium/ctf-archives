#include <stdio.h>
#include <pcap.h>

void packet_handler(u_char *args, const struct pcap_pkthdr *header, const u_char *packet){
    printf("Packet captured: Length %d\n", header->len);
}

int main(){
    char *dev = "eth0";
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle;

    handle = pcap_open_live(dev, BUFSIZ, 1, 1000, errbuf);
    if(handle == NULL){
        fprintf(stderr, "Couldn't open device %s: %s\n", dev, errbuf);
        return 2;
    }

    pcap_loop(handle, 10, packet_handler, NULL);
    pcap_close(handle);
    return 0;
}
