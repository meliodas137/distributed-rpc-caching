'use strict';

const api = require('@opentelemetry/api');
const tracer = require('./tracer')('microservice-one');
const http = require('http');

/** A function which makes requests and handles response. */
function makeRequest(url = '') {
  // span corresponds to outgoing requests. Here, we have manually created
  // the span, which is created to track work that happens outside of the
  // request lifecycle entirely.
  tracer.startActiveSpan('makeRequest', (span) => {
    http.get({
      host: 'localhost',
      port: 8080,
      path: url,
    }, (response) => {
      const body = [];
      response.on('data', (chunk) => body.push(chunk));
      response.on('end', () => {
        span.setAttribute("service.output", decodeURIComponent(body.toString()));
        console.log(body.toString());
        span.end();
      });
    });
  });
}

makeRequest('/s1');
makeRequest('/s2');
makeRequest('/s3');
makeRequest();

console.log('Sleeping 5 seconds before shutdown to ensure all records are flushed.');
setTimeout(() => { console.log('Completed.'); }, 5000);