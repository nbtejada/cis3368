// load the things we need
var express = require('express');
var app = express();
const bodyParser  = require('body-parser');

const path = require('path');
app.set('views', path.join(__dirname, 'views','pages'))

// required module to make calls to a REST API
const axios = require('axios');

app.use(bodyParser.urlencoded());

// set the view engine to ejs
app.set('view engine', 'ejs');


app.get('/', async (req, res) => {
    const response = await fetch('https://jsonplaceholder.typicode.com/users');
    const users = await response.json();
  
    const randomUsers = [];
    const getRandomInt = (max) => Math.floor(Math.random() * Math.floor(max));
    for (let i = 0; i < 3; i++) {
      const randomIndex = getRandomInt(users.length);
      const randomUser = users[randomIndex];
      randomUsers.push({
        name: randomUser.name,
        city: randomUser.address.city,
        company: randomUser.company.name,
      });
    }
  
    res.render('index', { randomUsers });
  });
  

app.listen(8080);
console.log('8080 is the magic port');
