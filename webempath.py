# -*- coding: utf-8 -*-

import execjs
ctx = execjs.compile(""" 
var fs = require('fs');
var request = require('request');

function analyzeWav(apiKey, wavFilename) {
  var url = 'https://hogehoge_server/v2/analyzeWav';
  var formData = {
    apikey: apiKey,
    wav: fs.createReadStream(wavFilename)
  };

  request.post({ url: url, formData: formData }, function(err, response) {
    if (err) {
      console.trace(err);
      return;
    } else if (!response.body) {
      console.trace("no response body");
      return;
    }

    var result = JSON.parse(response.body);
    console.log("result: " + JSON.stringify(result));
  });
}
""")
