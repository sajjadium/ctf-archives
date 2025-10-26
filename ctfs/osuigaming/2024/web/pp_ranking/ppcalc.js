import { StandardRuleset } from 'osu-standard-stable';
import { BeatmapDecoder, ScoreDecoder } from "osu-parsers";
import crypto from "crypto";

const calculate = async (osu, osr) => {
    const md5 = crypto.createHash('md5').update(osu).digest("hex");
    const scoreDecoder = new ScoreDecoder();
    const score = await scoreDecoder.decodeFromBuffer(osr);

    if (md5 !== score.info.beatmapHashMD5) {
        throw new Error("The beatmap and replay do not match! Did you submit the wrong beatmap?");
    }
    if (score.info._rulesetId !== 0) {
        throw new Error("Sorry, only standard is supported :(");
    }

    const beatmapDecoder = new BeatmapDecoder();
    const beatmap = await beatmapDecoder.decodeFromBuffer(osu);

    const ruleset = new StandardRuleset();
    const mods = ruleset.createModCombination(score.info.rawMods);
    const standardBeatmap = ruleset.applyToBeatmapWithMods(beatmap, mods);
    const difficultyCalculator = ruleset.createDifficultyCalculator(standardBeatmap);
    const difficultyAttributes = difficultyCalculator.calculate();

    const performanceCalculator = ruleset.createPerformanceCalculator(difficultyAttributes, score.info);
    const totalPerformance = performanceCalculator.calculate();

    return [totalPerformance, md5];
};

export default calculate;