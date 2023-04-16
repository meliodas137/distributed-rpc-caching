'use strict';

const http = require('http');

/** Starts a HTTP server that receives requests on sample server port. */
function startServer(port) {
  // Creates a server
  const server = http.createServer(handleRequest);
  // Starts the server
  server.listen(port, (err) => {
    if (err) {
      throw err;
    }
    console.log(`Node HTTP listening on ${port}`);
  });
}

/** A function which handles requests and send response. */
function handleRequest(request, response) {
  console.log("Request", request.url);
  const body = [];
  request.on('error', (err) => console.log(err));
  request.on('data', (chunk) => body.push(chunk));
  switch(request.url){
    case '/s1':
      s1(request, response);
      break;
    case '/s2':
      s2(request, response);
      break;
    case '/s3':
      s3(request, response);
      break;
    default:
      defaultResponse(request, response);
  }
}

function s1(request, response){
  request.on('end', () => {
    setTimeout(() => {
      response.write('s1');
      response.end();
    }, 500 );
  });
}

function s2(request, response){
  request.on('end', () => {
    setTimeout(() => {
      response.write('s2');
      response.end();
    }, 300);
  });
}

function s3(request, response){
  request.on('end', () => {
    setTimeout(() => {
      response.write('s3');
      response.end();
    }, 200);
  });
}

function defaultResponse(request, response){
  request.on('end', () => {
    setTimeout(() => {
      response.write('No matching service!');
      response.end();
    }, 200);
  });
}

startServer(8080);
