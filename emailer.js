var nodemailer = require('nodemailer');
var transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: 'keshav.chinnakotla@gmail.com',
      pass: '' // generate application specific email, then this works
    }
  });
  
  var mailOptions = {
    from: 'keshav.chinnakotla@gmail.com',
    to: 'koolcidz174@gmail.com',
    subject: 'Sending Email using Node.js',
    text: 'That was easy!'
  };
  
  transporter.sendMail(mailOptions, function(error, info){
    if (error) {
      console.log(error);
    } else {
      console.log('Email sent: ' + info.response);
    }
  });