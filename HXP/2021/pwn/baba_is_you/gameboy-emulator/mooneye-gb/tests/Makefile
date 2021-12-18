# Copyright (C) 2014-2020 Joonas Javanainen <joonas.javanainen@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

WLA ?= wla-gb
WLALINK ?= wlalink

BUILD_PATH := build

SRC := $(filter-out ./common/%.s,$(shell find . -type f -name '*.s'))
OBJS := $(addprefix $(BUILD_PATH)/, $(TARGETS:.s=.o))

all: $(addprefix $(BUILD_PATH)/, $(patsubst %.s,%.gb, $(SRC)))

$(BUILD_PATH):
	@mkdir $(BUILD_PATH)

$(OBJS): | $(BUILD_PATH)

$(BUILD_PATH)/flags: force | $(BUILD_PATH)
	@echo '${WLAFLAGS}' | cmp -s - $@ || echo '${WLAFLAGS}' > $@

$(BUILD_PATH)/%.o: %.s common/**/*.s $(BUILD_PATH)/flags
	@mkdir -p $(dir $@)
	@$(WLA) -I $(abspath common) $(WLAFLAGS) -o $(abspath $@) $<

$(BUILD_PATH)/%.link: $(BUILD_PATH)/%.o
	@printf "[objects]\n%s\n" $< > $@

$(BUILD_PATH)/%.gb: $(BUILD_PATH)/%.link
	@$(WLALINK) -d -S $(WLALINKFLAGS) $< $(abspath $@)
	@echo --- $(notdir $(basename $@))

tags: common/**/*.s $(BUILD_PATH)/flags
	@ctags --recurse=yes --languages=asm --langmap=asm:.s ./common

clean:
	@rm -rf $(BUILD_PATH)

.PHONY: clean all force
