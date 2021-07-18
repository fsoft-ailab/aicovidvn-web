const path = require('path');
const express = require('express');
const app = express();

// // Serve static files
// app.use(express.static(__dirname + '/dist'));

// // Send all requests to index.html
// app.get('/test*', function (req, res) {
//   res.sendFile(path.join(__dirname + '/dist/index.html'));
// });

// // app.listen(process.env.HOST || 'localhost')
// app.listen(process.env.PORT || 8080)

// const path = require('path');
// const express = require('express');
// const app = express();

//  Serve static files
app.use(express.static(__dirname + '/dist'));

// Send all requests to index.html
app.get('/*', function(req, res) {
  res.sendFile(path.join(__dirname + '/dist/index.html'));
});

// default Heroku port
app.listen(process.env.PORT || 8080)