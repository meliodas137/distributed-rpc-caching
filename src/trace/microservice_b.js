'use strict';

const http = require('http');
const tracer = require('./tracer')('microservice_b');

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
      case '/s4':
        s4(request, response);
        break;
    default:
      defaultResponse(request, response);
  }
}

function s1(request, response){
  request.on('end', () => {
    setTimeout(() => {
      tracer.startActiveSpan('s1_request', (span) => {
        http.get({
          host: 'localhost',
          port: 8081,
          path: '/s5',
          headers: {'parent-id': span.spanContext().traceId}
        }, (res) => {
          const body = [];
          res.on('data', (chunk) => body.push(chunk));
          res.on('end', () => {
            const rand = Math.floor(Math.random()*10000);
            var result = 's1 random output ' + rand + ' ' + decodeURIComponent(body.toString())

            span.setAttribute("service.output", decodeURIComponent(result));
            span.setAttribute("service.parentId", request.headers['parent-id'])
            
            response.write(result);
            response.end();
            span.end();
          });  
        });
      });
    }, 200 );
  });
}

function s2(request, response){
  request.on('end', () => {
    setTimeout(() => {
      tracer.startActiveSpan('s2_service', (span) => {
        const config = 'fixed config'
        var result = 's2 ' + config;
        span.setAttribute("service.output", decodeURIComponent(result));
        span.setAttribute("service.parentId", request.headers['parent-id'])
        response.write(result);
        response.end();
        span.end();
      })
  });
}

function s3(request, response){
  request.on('end', () => {
    setTimeout(() => {
      tracer.startActiveSpan('s3_request', (span) => {
        http.get({
          host: 'localhost',
          port: 8081,
          path: '/s7',
          headers: {'parent-id': span.spanContext().traceId}
        }, (res) => {
          const body = [];
          res.on('data', (chunk) => body.push(chunk));
          res.on('end', () => {

            const rand = Math.floor(Math.random()*10000);
            var result = 's3 random output ' + rand + ' ' + decodeURIComponent(body.toString());

            span.setAttribute("service.output", decodeURIComponent(result));
            span.setAttribute("service.parentId", request.headers['parent-id'])
            
            response.write(result);
            response.end();
            span.end();
          });  
        });
      });
    }, 200 );
  });
}

function s4(request, response){
  request.on('end', () => {
    setTimeout(() => {
      tracer.startActiveSpan('s4_request', (span) => {
        http.get({
          host: 'localhost',
          port: 8081,
          path: '/s6',
          headers: {'parent-id': span.spanContext().traceId}
        }, (res) => {
          const body = [];
          res.on('data', (chunk) => body.push(chunk));
          res.on('end', () => {
            const config = 'fixed config'
            var result = 's4 ' + config + ' ' + decodeURIComponent(body.toString())

            span.setAttribute("service.output", decodeURIComponent(result));
            span.setAttribute("service.parentId", request.headers['parent-id'])
            
            response.write(result);
            response.end();
            span.end();
          });  
        });
      });
    }, 200 );
  });
}

function defaultResponse(request, response){
  request.on('end', () => {
    setTimeout(() => {
      tracer.startActiveSpan('default_service', (span) => {
        var result = 'No matching service!';
        span.setAttribute("service.output", decodeURIComponent(result));
        span.setAttribute("service.parentId", request.headers['parent-id'])
        response.write(result);
        response.end();
        span.end();
      });
  });
}

startServer(8080);
