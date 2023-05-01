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
        let parent = request.headers['parent-id']
        let input = request.headers['input']
        request.headers['parent-id'] = span.spanContext().traceId
        let {fwdReq, output} = requiresReq(request)
        if(fwdReq) {
          http.get({
            host: 'localhost',
            port: request.headers['port'],
            path: request.headers['url'],
            headers: request.headers
            }, (res) => {
            const body = [];
            res.on('data', (chunk) => body.push(chunk));
            res.on('end', () => {
              span.setAttribute("service.output", decodeURIComponent(body.toString()));
              span.setAttribute("service.parentId", parent)
              span.setAttribute("service.input", input)
              
              response.write(decodeURIComponent(body.toString()));
              response.end();
              span.end();
            });  
          });
        }
        else {
          span.setAttribute("service.output", decodeURIComponent(output));
          span.setAttribute("service.parentId", parent)
          span.setAttribute("service.input", input)
          response.write(output);
          response.end();
          span.end();
        }
      });
    }, 100 );
  });
}

function requiresReq(request){
  let reqService = request.headers['caller']
  let nextService = request.headers['url'] || ''

  nextService = nextService.replace('/', '')
  let input = request.headers['input'] || ''
  let forwardingTable = cache.services.find(ser => ser.serviceName === reqService).forwardingTable || {}

  if(forwardingTable !== {} && forwardingTable[nextService] !== undefined) {
    let logs = forwardingTable[nextService].responses
    let resp = logs.find(lg => lg.input === input)
    return {fwdReq: !resp.deterministic, output: resp.output === undefined ? "" : resp.output}
  }
  return {fwdReq: true, output: ""}
}

startServer(8082);
