// load the things we need
var express = require('express');
var app = express();
const bodyParser  = require('body-parser');

// required module to make calls to a REST API
const axios = require('axios');

app.use(bodyParser.urlencoded());

// set the view engine to ejs
app.set('view engine', 'ejs');

// use res.render to load up an ejs view file

// index page 
app.get('/', function(req, res) {
    ;
    res.render('pages/index', {});
});

// choose API page
app.get('/choose', function(req, res) {
        
    res.render('pages/choose', {});
});

app.get('/space', function(req, res) {
        
    res.render('pages/space', {});
});

app.get('/viewspace', function(req, res) {
        
    res.render('pages/viewspace', {});
});

app.get('/viewcaptain', function(req, res) {
        
    res.render('pages/viewcaptain', {});
});

// about page
app.get('/about', function(req, res) {

    res.render('pages/about', {});
}); 
 

    
    
    

// examples page 
app.get('/examples', function(req, res) {
    var exampleVar = "Javascript";
    
    // this will render our new example spage 
    res.render("pages/examples.ejs", {exampleVar: exampleVar});
});




  app.post('/process_form', function(req, res){
    // create a variable to hold the username parsed from the request body
    let username = req.body.username
    // create a variable to hold ....
    let password = req.body.password

    let alert = require('alert');

  if (username === "space" && password === "galaxy"){
    res.render('pages/thanks.ejs', {body: req.body})
  }
  else {
    alert("Unsuccessful Login Attempt")
    res.redirect('back');
  }
});

app.get('/thanks', function(req, res){

    axios.get(`http://127.0.0.1:5000/api/cargo/all`)
    .then((response)=>{
        
        var cargo = response.data;
        var tagline = "Cargos in Transit:";
        console.log(cargo);
         // use res.render to load up an ejs view file
        res.render('pages/about.ejs', {
            cargo: cargo,
            tagline: tagline
        });
    });
}); 




app.listen(8080);
console.log('8080 is the magic port');
