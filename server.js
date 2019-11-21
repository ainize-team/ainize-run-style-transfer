var express = require('express');
var bodyParser = require('body-parser');
var app = express();
var { transfer } = require('/workspace/functions/index');
const cors = require('cors');

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json())

app.use(cors());
app.get('/transfer', transfer);

const server = app.listen(80, () => {
  const host = server.address().address;
  const port = server.address().port;
  console.log(`Example app listening at http://${host}:${port}`);
});