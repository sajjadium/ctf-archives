#pragma once

#include "settings.hpp"
#include "synths.hpp"

#include <juce_audio_formats/juce_audio_formats.h>
#include <juce_core/juce_core.h>

#include <exception>
#include <iostream>


#define assert_res(cond)                                        \
	do {                                                        \
		bool result = bool(cond);                               \
		if (!result) {                                          \
			return juce::Result::fail("assert failed: " #cond); \
		}                                                       \
	} while (0)

std::pair<juce::XmlElement*, juce::String> getRelayStaff(const std::unique_ptr<juce::XmlElement>& msRoot)
{
	if (auto score = msRoot->getChildByName("Score"); !score) {
		return {nullptr, ""};
	} else {
		for (auto* staff : score->getChildWithTagNameIterator("Staff")) {
			// Jankest of jank code in this file. Why doesn't C++ have a null-coalescing operator?
			// Heck, even PHP has `?->`. PHP!!! The world is upside down.
			if (auto measure = staff->getChildByName("Measure"); !measure) {
				continue;
			} else if (auto voice = measure->getChildByName("voice"); !voice) {
				continue;
			} else if (auto staffText = voice->getChildByName("StaffText"); !staffText) {
				continue;
			} else if (auto text = staffText->getChildByName("text"); !text) {
				continue;
			} else {
				if (auto s = text->getAllSubText(); s.startsWith("relay:")) {
					auto flag = s.substring(juce::String("relay:").length());
					return {staff, flag};
				}
			}
		}
	}
	return {nullptr, ""};
}

juce::Result getDuration(double& durationOut, const juce::String& durationType, juce::XmlElement* chord_or_rest)
{
	if (durationType == "quarter") {
		durationOut = 1.0;
	} else if (durationType == "whole") {
		durationOut = 4.0;
	} else if (durationType == "half") {
		durationOut = 2.0;
	} else if (durationType == "eighth") {
		durationOut = 0.5;
	} else if (durationType == "16th") {
		durationOut = 0.25;
	} else if (durationType == "32nd") {
		durationOut = 0.125;
	} else if (durationType == "64th") {
		durationOut = 0.0625;
	} else if (durationType == "measure") {
		assert_res(chord_or_rest->getTagName() == "Rest");
		auto dur = chord_or_rest->getChildElementAllSubText("duration", "4/4");
		auto idx = dur.indexOf("/");
		if (idx == -1) {
			return juce::Result::fail("unknown <duration>: " + dur);
		}
		auto num = dur.substring(0, idx).getIntValue();
		auto den = dur.substring(idx + 1).getIntValue();
		assert_res(num > 0 && num <= 16);
		assert_res(den > 0 && den <= 16);
		durationOut = 4.0 / den * num;
		assert_res(durationOut <= 4.0);
	} else {
		return juce::Result::fail("unknown duration: " + durationType);
	}
	return juce::Result::ok();
}

inline uint8_t hexdigit2nibble(char c)
{
	return isdigit(c) ? (c - '0') : islower(c) ? (c - 'a' + 10) : (c - 'A' + 10);
}

inline int getTempoFromStaff(juce::XmlElement* staff)
{
	if (auto mm = staff->getChildByName("Measure"); !mm)
		goto fail;
	else if (auto vc = mm->getChildByName("voice"); !vc)
		goto fail;
	else if (auto tempo = vc->getChildByName("Tempo"); !tempo)
		goto fail;
	else if (auto text = tempo->getChildByName("text"); !text)
		goto fail;
	else {
		auto content = text->getAllSubText();
		auto idx = content.indexOf(" = ");
		if (idx == -1)
			goto fail;

		auto bpm = content.substring(idx + 3).getIntValue();
		if (bpm >= 60 && bpm <= 240) {
			return bpm;
		}
	}

fail:
	return 0;
}

juce::Result loadMidiMessages(juce::MidiBuffer& midiBuffer, juce::XmlElement* staff, const juce::String& flag,
							  const std::string& key, double sampleRate)
{
	// Load bits into vector.
	// But first...
	// A lil' detour...
	std::vector<uint8_t> keybytes(key.length() / 2);
	for (size_t i = 0; i < keybytes.size(); i++) {
		uint8_t nibble1 = hexdigit2nibble(key[2 * i + 0])
						  << 4; // Bunch of implicit conv warnings here. But I've given up caring.
		uint8_t nibble2 = hexdigit2nibble(key[2 * i + 1]);
		keybytes[i] = nibble1 | nibble2;
	}

	std::vector<uint8_t> flagbits(static_cast<size_t>(flag.length() * 8));
	for (int i = 0; i < flag.length(); i++) {
		uint8_t byte = ~static_cast<uint8_t>(flag[i]) ^ keybytes[static_cast<size_t>(i) % keybytes.size()];
		uint8_t msb = (byte >> 7) & 1;
		for (int b = 7; b >= 0; b--) {
			flagbits[static_cast<size_t>(8 * i + (7 - b))] = ((byte >> b) & 1) ^ !msb;
		}
	}

	// Ask the staff for tissue. Good skill to have in restaurants.
	int bpm = getTempoFromStaff(staff);
	if (!bpm)
		bpm = JUCE_DEFAULT_BPM;
	double samplesPerBeat = sampleRate / (bpm / 60.0); // sample/s `div` beats/s

	double currSample = 0;	  // Accumulated sample.
	double alignedSample = 0; // Sample aligned to a 16th beat.
	int flagidx = 0;		  // Tracks which bit of the flag we're at.
	std::vector<int> pitches; // Pitches of the current chord.
	int measureCount = 0;

	for (auto mm : staff->getChildWithTagNameIterator("Measure")) {
		measureCount++;
		if (measureCount > JUCE_MAX_MEASURE_COUNT) {
			return juce::Result::fail("exceeded max measures");
		}
		if (auto vc = mm->getChildByName("voice")) {
			for (auto obj : vc->getChildIterator()) {
				auto tag = obj->getTagName();

				if (auto durationType = obj->getChildByName("durationType")) {
					double multiplier;
					auto res = getDuration(multiplier, durationType->getAllSubText(), obj);
					if (!res)
						return res;

					double nextSample = currSample + samplesPerBeat * multiplier;

					pitches.clear();

					if (obj->getTagName() == "Chord") {
						for (auto note : obj->getChildWithTagNameIterator("Note")) {
							auto pitch = note->getChildElementAllSubText("pitch", "?").getIntValue();
							assert_res(pitch > 0);

							// Add noteOn and noteOff msgs to the midi buffer.
							pitches.push_back(pitch);
						}

						float vel = JUCE_INITIAL_VELOCITY;

						// Aligned to 16th notes.
						for (; alignedSample < nextSample; alignedSample += samplesPerBeat * 0.25,
														   vel *= 0.94f, // Decay.
														   flagidx = (flagidx + 1) % (8 * flag.length()))
						{
							if (flagbits[static_cast<size_t>(flagidx)]) {
								// Trigger note on 1 bit.
								for (auto pitch : pitches) {
									midiBuffer.addEvent(juce::MidiMessage::noteOn(1, pitch, vel),
														static_cast<int>(alignedSample));
									midiBuffer.addEvent(
										juce::MidiMessage::noteOff(1, pitch, vel),
										static_cast<int>(alignedSample + samplesPerBeat * 0.25 * JUCE_NOTE_DURATION));
								}
							}
						}
					} else if (obj->getTagName() == "Rest") {
						// Pass. No rest for the ~~wicked~~ CTF player.
					}

					currSample = nextSample;
				} else {
					if (obj->getTagName() == "Dynamic") {
						// Pass. Baroque composers would approve.
					}
				}
				if (alignedSample < currSample) {
					// Jump to most recent sample aligned to a 16th beath.
					alignedSample = floor(currSample / (samplesPerBeat * 0.25)) * (samplesPerBeat * 0.25);
				}
			}
		}
	}
	return juce::Result::ok();
}

void makeSynth(juce::Synthesiser& synth, double sampleRate)
{
	synth.addSound(new SineWaveSound());
	synth.setCurrentPlaybackSampleRate(sampleRate);

	for (int i = 0; i < 4; i++)
		synth.addVoice(new WavetableVoice(JUCE_WAVETABLE, JUCE_WAVETABLE_SIZE));
}

juce::Result checkMuseScoreFile(const juce::ZipFile& mscz)
{
	assert_res(mscz.getNumEntries() > 0);
	for (int i = 0; i < mscz.getNumEntries(); i++) {
		// No slippies.
		auto filename = mscz.getEntry(i)->filename;
		assert_res(!filename.contains(".."));
	}
	return juce::Result::ok();
}

juce::Result generateRhythmicBleeps(const std::string& uniqueKey, const std::string& musicInputPath,
									const std::string& musescorePath, const std::string& outputPath)
{
	juce::File musicInputFile(musicInputPath);

	// MuseScore XML.
	juce::File msFile(musescorePath);
	assert_res(msFile.existsAsFile());

	juce::File unzipDirectory = msFile.getParentDirectory().getChildFile("tmp");
	unzipDirectory.createDirectory();

	juce::ZipFile mscz(msFile);
	if (auto res = checkMuseScoreFile(mscz); !res)
		return res;

	if (auto res = mscz.uncompressTo(unzipDirectory, false); !res)
		return res;

	// Find mscx file.
	juce::File mscx;
	for (int i = 0; i < mscz.getNumEntries(); i++) {
		juce::File file = unzipDirectory.getChildFile(mscz.getEntry(i)->filename);
		if (file.existsAsFile()) {
			// Sneak in a lil' anti-dirbust mechanism. (Not really needed now that we use an instancer... but we'll keep it here- cos why not!)
			auto newfilename = file.getFileNameWithoutExtension() + "_" + uniqueKey + file.getFileExtension();
			auto newfile = file.getSiblingFile(newfilename);
			file.moveFileTo(newfile);

			if (file.getFileExtension() == ".mscx") {
				mscx = newfile;
			}
		}
	}

	if (mscx == juce::File())
		return juce::Result::fail("no mscx found in mscz");

	assert_res(mscx.existsAsFile());

	juce::File musicOutputFile(outputPath);
	if (musicOutputFile.existsAsFile()) {
		// The Juce audio writer doesn't seem to overwrite existing files
		// properly. So we'll do it for them!
		musicOutputFile.deleteFile();
	}

	juce::AudioFormatManager formatManager;
	formatManager.registerBasicFormats();
	auto reader = std::unique_ptr<juce::AudioFormatReader>{formatManager.createReaderFor(musicInputFile)};
	if (!reader)
		return juce::Result::fail("failed to construct an audio reader");
	assert_res(reader->numChannels == 2);
	assert_res(reader->sampleRate <= JUCE_MAX_SAMPLE_RATE);

	auto layout = reader->getChannelLayout();

	juce::WavAudioFormat fmt;
	juce::AudioChannelSet channelSet;
	channelSet = juce::AudioChannelSet::quadraphonic();
	assert_res(fmt.isChannelLayoutSupported(channelSet));

	auto ofs = new juce::FileOutputStream(musicOutputFile);
	auto writer =
		std::unique_ptr<juce::AudioFormatWriter>{fmt.createWriterFor(ofs, reader->sampleRate, channelSet, 16, {}, 0)};
	if (!writer)
		return juce::Result::fail("failed to construct an audio writer");

	juce::MidiBuffer midiBuffer;

	auto xml = juce::parseXML(mscx);
	if (!xml)
		return juce::Result::fail("failed to parse xml. (Xcuse Me Laddie, please provide a proper MuseScore 4 file.)");

	auto [staff, flag] = getRelayStaff(xml);
	if (!staff)
		return juce::Result::fail("failed to locate a [Relay] staff. (Do you realyze the problem?)");

	if (flag.isEmpty())
		return juce::Result::fail("no flag. (Try harder.)");

	if (auto res = loadMidiMessages(midiBuffer, staff, flag, uniqueKey, reader->sampleRate); !res)
		return res;

	juce::AudioSampleBuffer buffer(static_cast<int>(reader->numChannels) + 2, JUCE_MAX_BUFFER_SIZE);
	int totalSamples = static_cast<int>(reader->lengthInSamples);
	if (totalSamples > JUCE_MAX_SECONDS * reader->sampleRate)
		return juce::Result::fail(
			"audio exceeded max duration. (What? You thought you could just upload Wagner's Ring Cycle and watch the "
			"server burn?)");

	int samplesProcessed = JUCE_MAX_BUFFER_SIZE;

	juce::Synthesiser synth;
	makeSynth(synth, reader->sampleRate);

	juce::AudioBuffer<float> synthBuffer(2, JUCE_MAX_BUFFER_SIZE);

	for (int readerStartSample = 0; readerStartSample < totalSamples; readerStartSample += samplesProcessed) {
		if (totalSamples - readerStartSample < samplesProcessed) {
			samplesProcessed = totalSamples - readerStartSample;
		}

		buffer.clear();
		synthBuffer.clear();

		reader->read(&buffer, 0, samplesProcessed, readerStartSample, true, true);

		juce::MidiBuffer localisedMidiBuffer;
		localisedMidiBuffer.addEvents(midiBuffer, readerStartSample, samplesProcessed, -readerStartSample);

		synth.renderNextBlock(synthBuffer, localisedMidiBuffer, 0, samplesProcessed);
		buffer.copyFrom(buffer.getNumChannels() - 2, 0, synthBuffer, 0, 0, synthBuffer.getNumSamples());
		buffer.copyFrom(buffer.getNumChannels() - 1, 0, synthBuffer, 1, 0, synthBuffer.getNumSamples());

		writer->writeFromAudioSampleBuffer(buffer, 0, samplesProcessed);
	}
	return juce::Result::ok();
}
