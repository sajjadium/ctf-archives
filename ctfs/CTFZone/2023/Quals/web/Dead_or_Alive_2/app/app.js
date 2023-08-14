import express from 'express';
import nunjucks from 'nunjucks';
import neo4j from 'neo4j-driver';
import md5 from 'md5'
import moment from 'moment'

const SALT = 'healthgraph';
const DATABASE = Deno.env.get("DB") ?? 'localhost';
const HOST = '0.0.0.0';
const PORT = Deno.env.get("PORT") ?? '3000';

const app = express();

const driver = neo4j.driver(
    `neo4j://${DATABASE}/hospitalgraph`,
    neo4j.auth.basic('moderator', 'moderator')
)

nunjucks.configure('views', {
    autoescape: true,
    express: app
});

app.use(express.json());

app.use('/static', express.static('./static'))

app.get('/', async function(req, res) {
    const session = driver.session()
    const result = await session.run(
        'MATCH (s:Symptom) RETURN s.name, s.description'
        )
    session.close();
    res.render('index.html', {'items': result.records});
});

app.post('/api/setUser', async (req, res) => {
    // zero-padded 9-digit number
    const ssn = ('000000000'+req.body.ssn).slice(-9)
    if (!ssn) return res.status(400).send({
        status: 'error',
        message: 'Bad ssn'
    });

    // Data depersonalization
    const name = md5(`${SALT}|${req.body.fullname}|${SALT}`);

    // Need only year for statistics
    const yearOfBirth = moment(req.body.dateOfBirth, 'DD/MM/YYYY').year?.();
    if (!yearOfBirth) return res.status(400).send({
        status: 'error',
        message: 'Need date in format DD/MM/YYYY'
    });

    const weight = parseFloat(req.body.weight);
    if (!weight) return res.status(400).send({
        status: 'error',
        message: 'Need correct weight'
    });

    // register user if not exists
    setUser(ssn, name, yearOfBirth, weight)
    .then(() => res.status(200).send({
                    status: 'Ok',
                    message: 'User updated'
                }));
});

app.post('/api/setSymptoms', async (req, res) => {
    // zero-padded 9-digit number
    const ssn = ('000000000'+req.body.ssn).slice(-9)
    if (!ssn) return res.status(400).send({
        status: 'error',
        message: 'Bad ssn'
    });

    const symptoms = req.body.symptoms?.map?.(i => `'${i}'`).join(',');
    // saving symptoms
    setSymptoms(ssn, symptoms)
    .then(() => res.status(200).send({
                    status: 'Ok',
                    message: 'Symptoms updated'
                }));
});

app.post('/api/getDiagnosis', async (req, res) => {
    // zero-padded 9-digit number
    const ssn = ('000000000'+req.body.ssn).slice(-9)
    if (!ssn) return res.status(400).send({
        status: 'error',
        message: 'Bad ssn'
    });

    // establish diagnosis
    getDiagnosis(ssn)
    .then((result) => res.status(200).send({
                        status: (result.length) ? 'Diagnosis found' : 'Healthy',
                        message: (result.length) ? result : [{
                            'name': 'Diagnosis not established, most probably you are healthy and beautiful!',
                            'description':'We could not identify the disease by your symptoms, now you have to live with it ...'
                        }]
                    }));
});

async function setUser(ssn, name, yearOfBirth, weight){
    const session = driver.session();
    const q = `
        MERGE (p:Patient {
                    ssn: '${ssn}'
                })
        ON CREATE SET p.since = date()
        SET p.name = '${name}'
        SET p.yearOfBirth = ${yearOfBirth}
        SET p.weight = ${weight}
    `
    return session.run(q)
            .catch(() => {})
            .then(() => session.close());
}

async function setSymptoms(ssn, symptoms){
    const session = driver.session();
    let q = `
        MATCH (p:Patient {ssn: '${ssn}'})
        MATCH (s:Symptom) WHERE s.name in [${symptoms}]
        MERGE (p)-[r:HAS]->(s)
    `;
    return session.run(q)
            .catch(() => {})
            .then(() => session.close());
}

async function getDiagnosis(ssn){
    const session = driver.session();
    const q = `
        // get patient symptoms as array
        MATCH (p:Patient {ssn: '${ssn}'})-[:HAS]->(s:Symptom)-[:OF]->(d:Disease)
        WITH d, collect(s.name) AS p_symptoms
        
        // looking for a match of the patient's symptoms in the symptoms of diseases
        MATCH (d)<-[:OF]-(d_symptom:Symptom)
        WITH d, p_symptoms, collect(d_symptom.name) as d_symptoms
        WHERE size(p_symptoms) = size(d_symptoms)
        RETURN d.name, d.description
    `;
    const result = await session.run(q).catch(() => {});
    session.close();
    return result?.records.map((record) => ({
            name: record.get('d.name'),
            description: record.get('d.description')
    }));
}

app.listen(PORT, HOST, () => console.log(`Listening on ${HOST}:${PORT}`));