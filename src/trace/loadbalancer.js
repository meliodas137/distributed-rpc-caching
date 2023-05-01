'use strict';

const http = require('http');
const tracer = require('./tracer')('loadbalancer');
let cache = require('./cacheInfo.json')
let useRpcCaching = false

/** Starts a HTTP server that receives requests on sample server port. */
function startServer(port) {
  if(cache !== {}) useRpcCaching = true 
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
  request.on('end', () => {
    setTimeout(() => {
    tracer.startActiveSpan('loadbalancer', (span) => {
        var parent = request.headers['parent-id']
        var input = request.headers['input']
        request.headers['parent-id'] = span.spanContext().traceId
        if(requiresReq(request)) {
          http.get({
            host: 'localhost',
            port: request.headers['port'],
            path: request.headers['url'],
            headers: request.headers
            }, (res) => {
            const body = [];
            res.on('data', (chunk) => body.push(chunk));
            res.on('end', () => {

              const rand = Math.floor(Math.random()*10000);
              var result = 's3 random output ' + rand + ' ' + decodeURIComponent(body.toString());

              span.setAttribute("service.output", decodeURIComponent(result));
              span.setAttribute("service.parentId", parent)
              span.setAttribute("service.input", input)
              
              response.write(result);
              response.end();
              span.end();
            });  
          });
        }
        else {
          let constRes = getDeterministicRes(resquest)
          response.write(constRes);
          response.end();
          span.end();
        }
      });
    }, 100 );
  });
}

function requiresReq(request){
  return true
}

function getDeterministicRes(request){
  return ''
}

startServer(8082);
