var restify = require('restify')
var logger = require('morgan')

var VERIFY_TOKEN = process.env.SLACK_VERIFY_TOKEN
if (!VERIFY_TOKEN) {
  console.error('SLACK_VERIFY_TOKEN is required')
  process.exit(1)
}
// Use Beep Boop provided PORT - default to 8080 for dev
var PORT = process.env.PORT || 8080

var server = restify.createServer()
server.use(logger('tiny'))

// Add a `/beepboop` route handler for `/beepboop` slash command
server.post('/beepboop', restify.bodyParser(), function (req, res) {
  if (req.params.token !== VERIFY_TOKEN) {
    return res.send(401, 'Unauthorized')
  }

  var message = 'boopbeep'

  // Handle any help requests
  if (req.params.text === 'help') {
    message = "Sorry, I can't offer much help, just here to beep and boop"
  }

  res.send({
    response_type: 'ephemeral',
    text: message
  })
})
// Add a GET handler for `/beepboop` route that Slack expects to be present
server.get('/beepboop', function (req, res) {
  res.send(200, 'Ok')
})

// 🔥 it up
server.listen(PORT, function (err) {
  if (err) {
    return console.error('Error starting server: ', err)
  }

  console.log('Server successfully started on port %s', PORT)
})
