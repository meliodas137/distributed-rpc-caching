'use strict';

const api = require('@opentelemetry/api');
const tracer = require('./tracer')('microservice_a');
const http = require('http');

/** A function which makes requests and handles response. */
function makeRequest(url = '') {
  // span corresponds to outgoing requests. Here, we have manually created
  // the span, which is created to track work that happens outside of the
  // request lifecycle entirely.
  tracer.startActiveSpan('a_request', (span) => {
    http.get({
      host: 'localhost',
      port: 8080,
      path: url,
      headers: {'parent-id': span.spanContext().traceId}
    }, (response) => {
      const body = [];
      response.on('data', (chunk) => body.push(chunk));
      response.on('end', () => {
        const rand = Math.floor(Math.random()*10000);
        span.setAttribute("service.output", rand);
        console.log(body.toString());
        span.end();
      });
    });
  });
}

function doRequests(){
  console.log('Sleeping 1 seconds after every request');
  setTimeout(() => { makeRequest('/s1'); console.log('Completed.'); }, 500);
  setTimeout(() => { makeRequest('/s2'); console.log('Completed.'); }, 1500);
  setTimeout(() => { makeRequest('/s3'); console.log('Completed.'); }, 2000);
  setTimeout(() => { makeRequest('/s4'); console.log('Completed.'); }, 2500);
  setTimeout(() => { makeRequest(); console.log('Completed.'); }, 3000);
}

doRequests();
