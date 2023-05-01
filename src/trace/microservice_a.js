'use strict';

const api = require('@opentelemetry/api');
const tracer = require('./tracer')('microservice_a');
const http = require('http');

/** A function which makes requests and handles response. */
function makeRequest(url = '', input = '') {
  // span corresponds to outgoing requests. Here, we have manually created
  // the span, which is created to track work that happens outside of the
  // request lifecycle entirely.
  tracer.startActiveSpan('a_request', (span) => {
    http.get({
      host: 'localhost',
      port: 8082, //sending it to loadbalancer
      headers: {'url': url, 'parent-id': span.spanContext().traceId, 'input': input, port: 8080, caller: 'a'}
    }, (response) => {
      const body = [];
      response.on('data', (chunk) => body.push(chunk));
      response.on('end', () => {
        const rand = Math.floor(Math.random()*10000);
        span.setAttribute("service.output", rand);
        span.setAttribute("service.input", url);
        console.log(body.toString());
        span.end();
      });
    });
  });
}

function doRequests(){
  console.log('Sleeping 1 seconds after every request');
  setTimeout(() => { makeRequest('/s1'); console.log('Completed.'); }, 100);
  setTimeout(() => { makeRequest('/s1', 'fallback'); console.log('Completed.'); }, 200);
  setTimeout(() => { makeRequest('/s2'); console.log('Completed.'); }, 300);
  setTimeout(() => { makeRequest('/s2', 'fetch'); console.log('Completed.'); }, 400);
  setTimeout(() => { makeRequest('/s3'); console.log('Completed.'); }, 500);
  setTimeout(() => { makeRequest('/s3', 'default'); console.log('Completed.'); }, 600);
  setTimeout(() => { makeRequest('/s4'); console.log('Completed.'); }, 700);
  setTimeout(() => { makeRequest('/s4', 'fallback'); console.log('Completed.'); }, 800);
  setTimeout(() => { makeRequest(); console.log('Completed.'); }, 1000);
}

doRequests();
