'use strict';
const express = require('express');
const request = require('request');
const HOSTNAME = process.env.HOSTNAME || 'NO_NAME';
const PORT = process.env.PORT || 8080;
const HOST = '0.0.0.0';
const app = express();
app.get('/', (request, response) => {
  response.send(`<html><body>Container ${HOSTNAME}:${PORT}</body></html>`);
});
app.listen(PORT, HOST);

console.log(`Running on http://${HOSTNAME}:${PORT}`);
console.log('Environment:');
Object.keys(process.env).forEach(function(key, index) {
  console.log(`${index}- ENV[${key}]=${process.env[key]}`);
});
const options = {json: true}
request(`${process.env.ECS_CONTAINER_METADATA_URI}`, options, (error, response, body) => {
  console.log("Container Metadata: %j", body);
});
request(`${process.env.ECS_CONTAINER_METADATA_URI}/task`, options, (error, response, body) => {
  console.log("Task Metadata: %j", body);
});
request(`${process.env.ECS_CONTAINER_METADATA_URI}/stats`, options, (error, response, body) => {
  console.log("Container Stats: %j", body);
});
request(`${process.env.ECS_CONTAINER_METADATA_URI}/task/stats`, options, (error, response, body) => {
  console.log("Task Stats: %j", body);
});
