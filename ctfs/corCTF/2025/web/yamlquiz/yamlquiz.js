const express = require('express');
const YAML = require('yaml');

const PORT = process.env.PORT || 4455;
const FLAG = process.env.FLAG || 'corctf{fake_flag_for_testing}';

const app = express();

app.use(express.urlencoded({extended: false}));
app.use(express.static('static'));

app.post('/submit', (req, res) => {
  let result = req.body.result;
  let score = 0;
  if (result) {
    const result_parsed_1 = YAML.parse(result, null, {version: '1.1'});
    const result_parsed_2 = YAML.parse(result, null, {version: '1.2'});
    const score_1 = result_parsed_1?.result?.[0]?.score ?? 0;
    const score_2 = result_parsed_2?.result?.[0]?.score ?? 0;
    if (score_1 !== score_2) {
        score = score_1;
    }
  } else {
    score = 0;
  }

  if (score === 5000) {
    res.json({pass: true, flag: FLAG});
  } else {
    res.json({pass: false});
  }
});

app.listen(PORT, () => console.log(`web/yamlquiz listening on port ${PORT}`));
