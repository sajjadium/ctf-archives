.PHONY: binaries handout.tgz

handout.tgz: binaries pcap
	TMPDIR=$$(mktemp -d) && \
		tar --exclude-from .tarignore -czf handout-tmp.tgz . && \
		mkdir -p "$$TMPDIR/amongst" && \
		tar -xzf handout-tmp.tgz -C "$$TMPDIR/amongst" && \
		echo 'The server has a different file here' > "$$TMPDIR/amongst/packages/game-server/assets/sus" && \
		tar -czf handout.tgz -C "$$TMPDIR" . && \
		rm -rf "$$TMPDIR" && \
		rm -f handout-tmp.tgz

binaries: misc/recalibrate-engine/engine misc/purchase-snack/vending

pcap: misc/file-transfer/out.pcap

misc/recalibrate-engine/engine: misc/recalibrate-engine/engine.c misc/recalibrate-engine/build.Dockerfile
	docker build misc/recalibrate-engine -f misc/recalibrate-engine/build.Dockerfile -t recalibrate-engine:build
	CONTAINER_ID=$$(docker create recalibrate-engine:build) ; \
		docker cp $$CONTAINER_ID:/chal/engine misc/recalibrate-engine/engine ; \
		docker rm $$CONTAINER_ID

misc/purchase-snack/vending: misc/purchase-snack/vending.c misc/purchase-snack/build.Dockerfile
	docker build misc/purchase-snack -f misc/purchase-snack/build.Dockerfile -t purchase-snack:build
	CONTAINER_ID=$$(docker create purchase-snack:build) ; \
		docker cp $$CONTAINER_ID:/chal/vending misc/purchase-snack/vending ; \
		docker rm $$CONTAINER_ID

misc/file-transfer/out.pcap: misc/file-transfer/build.Dockerfile misc/file-transfer/run.sh misc/file-transfer/sus.png
	docker build misc/file-transfer -f misc/file-transfer/build.Dockerfile -t file-transfer:build
	CONTAINER_ID=$$(docker run -d file-transfer:build) ; \
		sleep 20 ; \
		docker cp $$CONTAINER_ID:/out/tcpdump.pcap misc/file-transfer/out.pcap ; \
		docker stop $$CONTAINER_ID ; \
		docker rm $$CONTAINER_ID
	cp misc/file-transfer/out.pcap packages/game-server/assets/sus
