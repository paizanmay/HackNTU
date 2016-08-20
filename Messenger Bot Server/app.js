var express = require('express');
var app = express();

app.use(express.static('public'));

app.get('/', function(req, res) {
  res.sendfile(__dirname + '/index.html');
});

app.post('/test_post', function(req, res) {
  console.log("get post");
  var sender_id = req.param('sender_id');  
  console.log(sender_id);
  res.status(201);
  res.send('get post');
});

app.listen(5000, function() {
console.log("app listening on port 5000")
});