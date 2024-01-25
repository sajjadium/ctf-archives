#pragma once

#include <juce_audio_devices/juce_audio_devices.h>
#include <juce_core/juce_core.h>


struct SineWaveSound : public juce::SynthesiserSound
{
	SineWaveSound() {}

	bool appliesToNote(int) override
	{
		return true;
	}
	bool appliesToChannel(int) override
	{
		return true;
	}
};

class SineWaveVoice final : public juce::SynthesiserVoice
{
public:
	SineWaveVoice() {}

	bool canPlaySound(juce::SynthesiserSound* sound) override
	{
		return dynamic_cast<SineWaveSound*>(sound) != nullptr;
	}

	void startNote(int midiNoteNumber, float velocity, juce::SynthesiserSound* /*sound*/,
				   int /*currentPitchWheelPosition*/) override
	{
		currentAngle = 0.0;
		level = velocity * 0.15;
		tailOff = 0.0;

		auto cyclesPerSecond = juce::MidiMessage::getMidiNoteInHertz(midiNoteNumber);
		auto cyclesPerSample = cyclesPerSecond / getSampleRate();

		angleDelta = cyclesPerSample * juce::MathConstants<double>::twoPi;
	}

	void stopNote(float /*velocity*/, bool allowTailOff) override
	{
		if (allowTailOff) {
			// start a tail-off by setting this flag. The render callback will pick up on
			// this and do a fade out, calling clearCurrentNote() when it's finished.

			if (juce::approximatelyEqual(tailOff, 0.0)) // we only need to begin a tail-off if it's not already doing so
														// - the stopNote method could be called more than once.
				tailOff = 1.0;
		} else {
			// we're being told to stop playing immediately, so reset everything..

			clearCurrentNote();
			angleDelta = 0.0;
		}
	}

	void pitchWheelMoved(int /*newValue*/) override
	{
		// not implemented for the purposes of this demo!
	}

	void controllerMoved(int /*controllerNumber*/, int /*newValue*/) override
	{
		// not implemented for the purposes of this demo!
	}

	void renderNextBlock(juce::AudioBuffer<float>& outputBuffer, int startSample, int numSamples) override
	{
		if (!juce::approximatelyEqual(angleDelta, 0.0)) {
			if (tailOff > 0.0) {
				while (--numSamples >= 0) {
					auto currentSample = (float)(sin(currentAngle) * level * tailOff);

					for (auto i = outputBuffer.getNumChannels(); --i >= 0;)
						outputBuffer.addSample(i, startSample, currentSample);

					currentAngle += angleDelta;
					++startSample;

					tailOff *= 0.99;

					if (tailOff <= 0.005) {
						// tells the synth that this voice has stopped
						clearCurrentNote();

						angleDelta = 0.0;
						break;
					}
				}
			} else {
				while (--numSamples >= 0) {
					auto currentSample = (float)(sin(currentAngle) * level);

					for (auto i = outputBuffer.getNumChannels(); --i >= 0;)
						outputBuffer.addSample(i, startSample, currentSample);

					currentAngle += angleDelta;
					++startSample;
				}
			}
		}
	}

	using SynthesiserVoice::renderNextBlock;

private:
	double currentAngle = 0.0;
	double angleDelta = 0.0;
	double level = 0.0;
	double tailOff = 0.0;
};

class WavetableVoice final : public juce::SynthesiserVoice
{
public:
	WavetableVoice(const float* wavetable_, int wavetableLength_)
		: wavetable{wavetable_}, wavetableLength{wavetableLength_}
	{
		adsr.setParameters(juce::ADSR::Parameters(0.02f, 0.08f, 0.9f, 0.04f));
	}

	bool canPlaySound(juce::SynthesiserSound* sound) override
	{
		return dynamic_cast<SineWaveSound*>(sound) != nullptr;
	}

	void startNote(int midiNoteNumber, float velocity, juce::SynthesiserSound* /*sound*/,
				   int /*currentPitchWheelPosition*/) override
	{
		currentPhase = 0.0;
		level = velocity;

		auto cyclesPerSecond = juce::MidiMessage::getMidiNoteInHertz(midiNoteNumber);
		auto cyclesPerSample = cyclesPerSecond / getSampleRate();

		phaseDelta = cyclesPerSample * wavetableLength;

		adsr.setSampleRate(getSampleRate());
		adsr.reset();
		adsr.noteOn();
	}

	void stopNote(float /*velocity*/, bool allowTailOff) override
	{
		if (allowTailOff) {
			// start a tail-off by setting this flag. The render callback will pick up on
			// this and do a fade out, calling clearCurrentNote() when it's finished.
			adsr.noteOff();
		} else {
			// we're being told to stop playing immediately, so reset everything..
			clearCurrentNote();
			phaseDelta = 0.0;
		}
	}

	void pitchWheelMoved(int /*newValue*/) override
	{
		// not implemented for the purposes of this demo!
	}

	void controllerMoved(int /*controllerNumber*/, int /*newValue*/) override
	{
		// not implemented for the purposes of this demo!
	}

	void renderNextBlock(juce::AudioBuffer<float>& outputBuffer, int startSample, int numSamples) override
	{
		while (--numSamples >= 0) {
			int idx = int(currentPhase);	  // Integer part.
			double frac = currentPhase - idx; // Decimal part.

			// Get the pre-generated sample to the LEFT of the current sample.
			float samp0 = wavetable[idx];

			// Get the pre-generated sample to the RIGHT of the current sample.
			idx = (idx + 1) % wavetableLength;
			float samp1 = wavetable[idx];

			// Interpolate between the left and right samples to get the current sample.
			float currentSample = (samp0 + static_cast<float>((samp1 - samp0) * frac));
			currentSample *= level * adsr.getNextSample();

			for (auto i = outputBuffer.getNumChannels(); --i >= 0;)
				outputBuffer.addSample(i, startSample, currentSample);

			currentPhase += phaseDelta;
			if (currentPhase >= wavetableLength) {
				currentPhase -= wavetableLength;
			}
			++startSample;
		}
	}

	using SynthesiserVoice::renderNextBlock;

private:
	const float* wavetable = nullptr;
	int wavetableLength = 0;
	double currentPhase = 0.0;
	double phaseDelta = 0.0;
	float level = 0.0;
	juce::ADSR adsr;
};
