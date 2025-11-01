A cloud-native, containerized, strongly consistent SAML web application, but maybe something is wrong?

Due to differences between local and remote environments, you need to be aware of the following:

1. In a local environment (started using `docker-compose`), the healthcheck, sp, proxy, and kvstore containers have different IP addresses in the Docker network. Therefore, within the `run.sh` scripts of these containers, the container names will be used as domain names for requests (e.g., proxy:2379, sp:9000).

2. In a remote environment (deployed based on Kubernetes), the healthcheck, sp, proxy, and kvstore containers belong to the same pod, therefore they share a single IP address, which is obtained using the `hostname -i` command.
