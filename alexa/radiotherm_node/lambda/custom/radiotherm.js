const config = require('./config.js').config;
const tunnel = require('tunnel-ssh');
const request = require('request');

module.exports = {getTemp, setTemp};

async function getTemp() {
  return new Promise( (resolve, reject) => {
    tunnel(config, function (tnl_error, server) {
      if (tnl_error) {
        console.log("Tunnel error:", tnl_error);
        reject();
      } else {
        // run request
        var options = {
          url: 'http://127.0.0.1:27000/tstat/temp',
          json: true
        }
        request.get(options, function (req_error, response, body) {
          // console.log('error:', error); // Print the error if one occurred
          // console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
          // console.log('body:', body);
          // console.log(typeof body);
          // console.log(body.temp);
          //callback(body['temp']);
          if (req_error) {
            console.log("request error:", req_error);
            reject();
          } else {
            resolve(body['temp']);
          }
        }); // closes request.get
      } // end tnl_error else
    }); // closes tunnel
  }); // promise
}

function setTemp(temp) {

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
          //console.log("error", err);
          tnl.close();
        });
      } else if ('t_cool' in body) {
        options['body'] = {t_cool: temp};
        request.post(options, (err, res, body) => {
          //console.log("error", err);
          tnl.close();
        });
      }
    });

  });
}
