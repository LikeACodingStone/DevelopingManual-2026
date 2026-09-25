.PHONY: all test clean core audio business
all: core audio business
core:
	$(MAKE) -C S001_OperatingSystem/linux/core_engineering
audio:
	$(MAKE) -C S007_Library/audio_speech_processing
business:
	$(MAKE) -C S007_Library/business_interaction
test:
	$(MAKE) -C S001_OperatingSystem/linux/core_engineering run
	$(MAKE) -C S007_Library/audio_speech_processing run
	$(MAKE) -C S007_Library/business_interaction run
clean:
	$(MAKE) -C S001_OperatingSystem/linux/core_engineering clean
	$(MAKE) -C S007_Library/audio_speech_processing clean
	$(MAKE) -C S007_Library/business_interaction clean
