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
  // console.log(request.headers['parent-id'])
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
        var input = request.headers['input']
        var path = input === 'fallback' ? '/s7' : '/s5'
        http.get({
          host: 'localhost',
          port: 8082,
          headers: {'port': 8081, url: path, 'parent-id': span.spanContext().traceId}
        }, (res) => {
          const body = [];
          res.on('data', (chunk) => body.push(chunk));
          res.on('end', () => {
            const rand = Math.floor(Math.random()*10000);
            var result = 's1 random output ' + rand + ' ' + decodeURIComponent(body.toString())

            span.setAttribute("service.output", decodeURIComponent(result));
            span.setAttribute("service.parentId", request.headers['parent-id'])
            span.setAttribute("service.input", input)
            
            response.write(result);
            response.end();
            span.end();
          });  
        });
      });
    }, 100 );
  });
}

function s2(request, response){
  request.on('end', () => {
    setTimeout(() => {
      tracer.startActiveSpan('s2_service', (span) => {
        var input = request.headers['input']
        const config = 'fixed config'
        var result = 's2 ' + config;
        
        if(input === 'fetch') {
          http.get({
            host: 'localhost',
            port: 8082,
            headers: {'port': 8081, url: '/s7', 'parent-id': span.spanContext().traceId}
          }, (res) => {
            const body = [];
            res.on('data', (chunk) => body.push(chunk));
            res.on('end', () => {

              var result = result + decodeURIComponent(body.toString())

              span.setAttribute("service.output", decodeURIComponent(result));
              span.setAttribute("service.parentId", request.headers['parent-id'])
              span.setAttribute("service.input", input)

              response.write(result);
              response.end();
              span.end();
            });  
          })
        } else {
          span.setAttribute("service.output", decodeURIComponent(result));
          span.setAttribute("service.parentId", request.headers['parent-id'])
          span.setAttribute("service.input", input)
          response.write(result);
          response.end();
          span.end();
        }
      })
    }, 100);
  });
}

function s3(request, response){
  request.on('end', () => {
    setTimeout(() => {
      var input = request.headers['input']
      var path = input === 'default' ? '' : '/s7'
      tracer.startActiveSpan('s3_request', (span) => {
        http.get({
          host: 'localhost',
          port: 8082,
          headers: {'port': 8081, url: path, 'parent-id': span.spanContext().traceId}
        }, (res) => {
          const body = [];
          res.on('data', (chunk) => body.push(chunk));
          res.on('end', () => {

            const rand = Math.floor(Math.random()*10000);
            var result = 's3 random output ' + rand + ' ' + decodeURIComponent(body.toString());

            span.setAttribute("service.output", decodeURIComponent(result));
            span.setAttribute("service.parentId", request.headers['parent-id'])
            span.setAttribute("service.input", input)
            
            response.write(result);
            response.end();
            span.end();
          });  
        });
      });
    }, 100 );
  });
}

function s4(request, response){
  request.on('end', () => {
    setTimeout(() => {
      var input = request.headers['input']
      var path = input === 'fallback' ? 's5' : '/s6'
      tracer.startActiveSpan('s4_request', (span) => {
        http.get({
          host: 'localhost',
          port: 8082,
          headers: {'port': 8081, url: path, 'parent-id': span.spanContext().traceId}
        }, (res) => {
          const body = [];
          res.on('data', (chunk) => body.push(chunk));
          res.on('end', () => {
            const config = 'fixed config'
            var result = 's4 ' + config + ' ' + decodeURIComponent(body.toString())

            span.setAttribute("service.output", decodeURIComponent(result));
            span.setAttribute("service.parentId", request.headers['parent-id'])
            span.setAttribute("service.input", request.headers['input'])
            
            response.write(result);
            response.end();
            span.end();
          });  
        });
      });
    }, 100 );
  });
}

function defaultResponse(request, response){
  request.on('end', () => {
    setTimeout(() => {
      tracer.startActiveSpan('default_service', (span) => {
        var result = 'No matching service!';
        span.setAttribute("service.output", decodeURIComponent(result));
        span.setAttribute("service.parentId", request.headers['parent-id'])
        span.setAttribute("service.input", request.headers['input'])
        response.write(result);
        response.end();
        span.end();
      });
    }, 100);
  });
}

startServer(8080);
