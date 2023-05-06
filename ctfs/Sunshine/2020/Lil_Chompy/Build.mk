# Used by deploy/Build.mk
CHOMPY_DIR := $(DIR)
CHOMPY_BUILD := $(BUILD_DIR)

# List of targets to build
TARGETS := lilchompys lilchompys.debug libcageheap.so

# Build settings applied to all targets in this directory
CFLAGS := -Wall -Wextra
BITS := 64
ASLR := 1
NX := 1
CANARY := 1
RELRO := 1
DEBUG := 1

# Build libcageheap.so in debug mode
libcageheap.so_SRCS := heap.c compat.c heap_debug.c
libcageheap.so := 1

# Build a release version of the lilchompys binary
lilchompys_SRCS := lilchompys.c
lilchompys_LIBS := $(CHOMPY_BUILD)/libcageheap.so

# Build a debug version of the lilchompys binary
lilchompys.debug_SRCS := lilchompys.c
lilchompys.debug_LIBS := $(CHOMPY_BUILD)/libcageheap.so
lilchompys.debug_CFLAGS := -DCHOMPY_DEBUG=1


# Build a Docker image w/o the real flag, so it can be distributed to players
CHOMPY_DOCKER_IMAGE := kjcolley7/lilchompys-redacted
DOCKER_IMAGE := $(CHOMPY_DOCKER_IMAGE)
DOCKER_IMAGE_TAG := release
FLAG_FILE :=
FLAG := fake{this is not the real flag. the real one is only on the server}

# This is the port that the fake challenge will run on if you do `make docker-start`
# from the PwnableHarness directory
DOCKER_PORTS := 20003

# Only allow connections to last for a maximum of 30 seconds
DOCKER_TIMELIMIT := 30

# Tell the Dockerfile where the build dir (that contains libcageheap.so) is
DOCKER_BUILD_ARGS := --build-arg "BUILD_DIR=$(BUILD_DIR)"


# List of files to publish
PUBLISH_BUILD := lilchompys.tar.gz docker-image-redacted.tar.gz
PUBLISH_LIBC := lilchompys-libc.so

# Makefile rules for rendering Graphviz files into PDFs when using `make graph`
# from the PwnableHarness directory. You might need to `apt-get install graphviz`
_GRAPHVIZ_FILES := $(wildcard $(CHOMPY_DIR)/*.dot)

$(CHOMPY_DIR)/%.pdf: $(CHOMPY_DIR)/%.dot
	$(_V)echo "Rendering $@ using Graphviz"
	$(_v)dot -Tpdf -o$@ $<

$(CHOMPY_DIR)/%.svg: $(CHOMPY_DIR)/%.dot
	$(_V)echo "Rendering $@ using Graphviz"
	$(_v)dot -Tsvg -o$@ $<

graph-pdf: $(_GRAPHVIZ_FILES:.dot=.pdf)

graph-svg: $(_GRAPHVIZ_FILES:.dot=.svg)

graph: graph-svg

.PHONY: graph graph-pdf graph-svg


# Share all sources and the real challenge binaries, as well as the build settings
_HEADERS := compat.h heap.h heap_internal.h heap_debug.h
_ARCHIVE_FILES_BUILD := $(sort $(addprefix $(CHOMPY_BUILD)/,$(TARGETS)))
_ARCHIVE_FILES_SRC := $(sort \
	$(addprefix $(CHOMPY_DIR)/, \
		$(foreach target,$(TARGETS),$($(target)_SRCS)) \
		$(_HEADERS) \
		Build.mk \
		Dockerfile \
		BUILDING.md \
	) \
)
_ARCHIVE_DIR := $(CHOMPY_BUILD)/archive
_ARCHIVE_DST_BUILD := $(addprefix $(_ARCHIVE_DIR)/,$(notdir $(_ARCHIVE_FILES_BUILD)))
_ARCHIVE_DST_SRC := $(addprefix $(_ARCHIVE_DIR)/,$(notdir $(_ARCHIVE_FILES_SRC)))
_ARCHIVE_FILES := $(sort $(_ARCHIVE_FILES_BUILD) $(_ARCHIVE_FILES_SRC))
_ARCHIVE_DST := $(sort $(_ARCHIVE_DST_BUILD) $(_ARCHIVE_DST_SRC))

$(_ARCHIVE_DST_BUILD): $(_ARCHIVE_DIR)/%: $(CHOMPY_BUILD)/% $(_ARCHIVE_DIR)/.dir
	$(_v)cp $< $@

$(_ARCHIVE_DST_SRC): $(_ARCHIVE_DIR)/%: $(CHOMPY_DIR)/% $(_ARCHIVE_DIR)/.dir
	$(_v)cp $< $@

_CHOMPY_DOCKERIGNORE := $(CHOMPY_BUILD)/.dockerignore
$(_CHOMPY_DOCKERIGNORE): $(CHOMPY_BUILD)/.dir
	$(_v){ \
		echo '*.tar.gz'; \
		echo 'archive/'; \
	} > $@

$(CHOMPY_BUILD)/lilchompys.tar.gz: $(_ARCHIVE_DST) | $(_CHOMPY_DOCKERIGNORE)
	$(_V)echo "Creating archive $@"
	$(_v)tar czf $@ -C $(_ARCHIVE_DIR) $(notdir $^)


$(CHOMPY_BUILD)/docker-image-redacted.tar.gz: docker-build[$(CHOMPY_DOCKER_IMAGE).release] | $(_CHOMPY_DOCKERIGNORE)
	$(_V)echo "Exporting docker image $(@F)"
	$(_v)docker save $(CHOMPY_DOCKER_IMAGE) | gzip > $@

# For the real server only, define DOCKER_BUILD_ONLY to prevent the fake container from
# running as part of `make docker-start`
-include $(CHOMPY_DIR)/Override.mk
