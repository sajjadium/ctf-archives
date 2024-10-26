const express = require('express');
const mysql = require('mysql');
const app = express();

const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'Sup3rStr0ngP@ssw0rd!',
    database: 'syringe_hospital'
});

app.get('/get-patients', (req, res) => {
    const patient_name = req.query.patient_name;

    const query = `SELECT * FROM patients WHERE patient_name = '${patient_name}'`;

    connection.query(query, (error, results) => {
        if (error) throw error;
        res.send(results);
    });
});

app.listen(3000, () => {
    console.log('Server running on http://localhost:3000');
});