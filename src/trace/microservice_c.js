'use strict';

const http = require('http');
const tracer = require('./tracer')('microservice_c');

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
    case '/s5':
      s5(request, response);
      break;
    case '/s6':
      s6(request, response);
      break;
    case '/s7':
      s7(request, response);
      break;
    default:
      defaultResponse(request, response);
  }
}

function s5(request, response){
  request.on('end', () => {
    setTimeout(() => {
      tracer.startActiveSpan('s5_service', (span) => {
        var res = 's5 ';
        span.setAttribute("service.output", decodeURIComponent(res));
        span.setAttribute("service.parentId", request.headers['parent-id'])
        response.write(res);
        response.end();
        span.end();
      })
    }, 50 );
  });
}

function s6(request, response){
  request.on('end', () => {
    setTimeout(() => {
      tracer.startActiveSpan('s6_service', (span) => {
        var res = 's6 ';
        span.setAttribute("service.output", decodeURIComponent(res));
        span.setAttribute("service.parentId", request.headers['parent-id'])
        response.write(res);
        response.end();
        span.end();
      })
    }, 50);
  });
}

function s7(request, response){
  request.on('end', () => {
    setTimeout(() => {
      tracer.startActiveSpan('s7_service', (span) => {
        const rand = Math.floor(Math.random()*20000);
        var res = 's7 ' + rand;
        span.setAttribute("service.output", decodeURIComponent(res));
        span.setAttribute("service.parentId", request.headers['parent-id'])
        response.write(res);
        response.end();
        span.end();
      })
    }, 50);
  });
}

function defaultResponse(request, response){
  request.on('end', () => {
    setTimeout(() => {
      tracer.startActiveSpan('s7_service', (span) => {
        var res = 'No matching service!';
        span.setAttribute("service.output", decodeURIComponent(res));
        span.setAttribute("service.parentId", request.headers['parent-id'])
        response.write(res);
        response.end();
        span.end();
      })
    }, 50);
  });
}

startServer(8081);
