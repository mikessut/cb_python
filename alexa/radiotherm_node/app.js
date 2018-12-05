const request = require('request');
const config = require('./config.js').config;
const tunnel = require('tunnel-ssh');
const express = require('express');
const port = 3000;

function getTemp(callback) {

  tunnel(config, function (error, server) {
    //....
    console.log(error)

    var options = {
      url: 'http://127.0.0.1:27000/tstat/temp',
      json: true
    }
    request.get(options, function (error, response, body) {
      console.log('error:', error); // Print the error if one occurred
      // console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
      console.log('body:', body);
      console.log(typeof body);
      console.log(body.temp);
      callback(body['temp']);
    });
  });
}

function setTemp(temp, callback) {

  var c = Object.assign({}, config);
  c['keepAlive'] = true;
  var tnl = tunnel(c, function (error, server) {

    options = {
      url: 'http://127.0.0.1:27000/tstat',
      //body: {t_heat: temp},
      json:true,
    };

    getOptions = {
      url: 'http://127.0.0.1:27000/tstat',
      json:true
    };

    request.get(getOptions, function (error, response, body) {
      //console.log('error:', error); // Print the error if one occurred
      // console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
      //console.log('body:', body);
      //console.log(typeof body);
      //console.log(body.temp);
      if ('t_heat' in body) {
        options['body'] = {t_heat: temp};
        request.post(options, (err, res, body) => {
          console.log("error", err);
          tnl.close();
        });
      } else if ('t_cool' in body) {
        options['body'] = {t_cool: temp};
        request.post(options, (err, res, body) => {
          console.log("error", err);
          tnl.close();
        });
      }
      //tnl.close();
      //callback();
    });

  });
}

// getTemp( (temp2) => {
//   console.log('callback', temp2)
// });

// setTemp(63, () => {
//   console.log('complete');
//
// });

const app = express();

app.use(express.json());

app.post('/', (req, res) => {
  //console.log("body:", req.body);
  //console.log(req.body)

  var alexa_request = req.body.request;
  if (!alexa_request) {
    //console.log("returning...");
    res.json({});
    return;
  }
  var intent = {};
  if ('intent' in alexa_request) {
    intent = alexa_request.intent;
  }
  console.log('intent', intent);
  res.json({thiswas: "success"});
});

app.listen(port, () => console.log(`Example app listening on port ${port}!`));
