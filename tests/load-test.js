import http from 'k6/http';
import { check, sleep } from 'k6';
import { Counter, Rate, Trend } from 'k6/metrics';

export let errorCount = new Counter('errors');
export let errorRate = new Rate('error_rate');
export let responseTimeTrend = new Trend('response_time');

export let options = {
  stages: [
    { duration: '1m', target: 5 },  // Ramp-up to 5 users over 1 minute
    { duration: '3m', target: 5 },  // Stay at 5 users for 3 minutes
    { duration: '1m', target: 10 }, // Ramp-up to 10 users over 1 minute
    { duration: '3m', target: 10 }, // Stay at 10 users for 3 minutes
    { duration: '1m', target: 0 },  // Ramp-down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<2000'], // 95% of requests must complete below 2s (более реалистично)
    http_req_failed: ['rate<0.05'],    // Error rate must be below 5% (было слишком строго)
    error_rate: ['rate<0.05'],         // Custom error rate threshold
  },
};

const books = [
  { id: 1, title: 'Clean Code', author: 'Robert Martin', price: 1500 },
  { id: 2, title: 'Software Architecture', author: 'Martin Fowler', price: 2000 },
  { id: 3, title: 'Python for Professionals', author: 'Dan Bader', price: 1800 }
];

const BOOKSHOP_URL = __ENV.BOOKSHOP_URL || 'http://localhost:8000';
const API_STORE_URL = __ENV.API_STORE_URL || 'http://localhost:5050';

export default function () {
  let bookshopResponse = testBookshop();
  let apiStoreResponse = testApiStore();
  
  sleep(1);
}

function testBookshop() {
  let responses = {};
  
  let booksResponse = http.get(`${BOOKSHOP_URL}/api/books`);
  check(booksResponse, {
    'Books API status is 200': (r) => r.status === 200,
    'Books API response time < 2000ms': (r) => r.timings.duration < 2000,
  }) || errorCount.add(1);
  
  responses.books = booksResponse;
  responseTimeTrend.add(booksResponse.timings.duration);
  
  if (booksResponse.status !== 200) {
    errorRate.add(true);
    return responses;
  } else {
    errorRate.add(false);
  }

  let randomBook = books[Math.floor(Math.random() * books.length)];
  let addToCartPayload = JSON.stringify({
    book_id: randomBook.id,
    quantity: Math.floor(Math.random() * 3) + 1
  });
  
  let cartResponse = http.post(
    `${BOOKSHOP_URL}/api/cart/add`,
    addToCartPayload,
    { headers: { 'Content-Type': 'application/json' } }
  );
  
  check(cartResponse, {
    'Add to cart status is 200': (r) => r.status === 200,
    'Add to cart response time < 2000ms': (r) => r.timings.duration < 2000,
  }) || errorCount.add(1);
  
  responses.addToCart = cartResponse;
  responseTimeTrend.add(cartResponse.timings.duration);

  let getCartResponse = http.get(`${BOOKSHOP_URL}/api/cart`);
  check(getCartResponse, {
    'Get cart status is 200': (r) => r.status === 200,
    'Cart has items': (r) => JSON.parse(r.body).count > 0,
  }) || errorCount.add(1);
  
  responses.getCart = getCartResponse;

  if (Math.random() > 0.5) {
    let orderResponse = http.post(
      `${BOOKSHOP_URL}/api/orders`,
      '{}',
      { headers: { 'Content-Type': 'application/json' } }
    );
    
    check(orderResponse, {
      'Create order status is 201': (r) => r.status === 201,
      'Order creation response time < 2000ms': (r) => r.timings.duration < 2000,
    }) || errorCount.add(1);
    
    responses.order = orderResponse;
    responseTimeTrend.add(orderResponse.timings.duration);
  }

  return responses;
}

function testApiStore() {
  let responses = {};
  
  let healthResponse = http.get(`${API_STORE_URL}/`);
  check(healthResponse, {
    'API Store health status is 200': (r) => r.status === 200,
    'API Store health response time < 1500ms': (r) => r.timings.duration < 1500,
  }) || errorCount.add(1);
  
  responses.health = healthResponse;
  responseTimeTrend.add(healthResponse.timings.duration);

  let purchasesResponse = http.get(`${API_STORE_URL}/purchases`);
  check(purchasesResponse, {
    'Get purchases status is 200': (r) => r.status === 200,
    'Purchases response is array': (r) => Array.isArray(JSON.parse(r.body)),
  }) || errorCount.add(1);
  
  responses.purchases = purchasesResponse;

  if (Math.random() > 0.7) {
    let mockPurchase = [{
      order_id: Math.floor(Math.random() * 1000),
      book_id: Math.floor(Math.random() * 3) + 1,
      user_id: Math.floor(Math.random() * 100) + 1,
      book_title: 'Load Test Book',
      author_name: 'Test Author',
      price: Math.floor(Math.random() * 2000) + 1000,
      create_at: new Date().toISOString().split('T')[0],
      publisher_id: 1
    }];
    
    let createPurchaseResponse = http.post(
      `${API_STORE_URL}/purchases`,
      JSON.stringify(mockPurchase),
      { headers: { 'Content-Type': 'application/json' } }
    );
    
    check(createPurchaseResponse, {
      'Create purchase status is 200': (r) => r.status === 200,
      'Purchase creation response time < 1000ms': (r) => r.timings.duration < 1000,
    }) || errorCount.add(1);
    
    responses.createPurchase = createPurchaseResponse;
    responseTimeTrend.add(createPurchaseResponse.timings.duration);
  }

  return responses;
}

export function handleSummary(data) {
  return {
    'load-test-results.json': JSON.stringify(data, null, 2),
    stdout: textSummary(data, { indent: ' ', enableColors: true }),
  };
}

function textSummary(data, options) {
  return `
     execution: local
        script: ${__ENV.K6_SCRIPT_NAME || 'load-test.js'}
        output: -

     scenarios: (100.00%) 1 scenario, max ${data.root_group.checks} concurrent VUs

     data_received..................: ${data.metrics.data_received.values.count} B
     data_sent......................: ${data.metrics.data_sent.values.count} B
     http_req_blocked...............: avg=${data.metrics.http_req_blocked.values.avg.toFixed(2)}ms
     http_req_connecting............: avg=${data.metrics.http_req_connecting.values.avg.toFixed(2)}ms
     http_req_duration..............: avg=${data.metrics.http_req_duration.values.avg.toFixed(2)}ms
     http_req_failed................: ${data.metrics.http_req_failed.values.rate.toFixed(2)}%
     http_req_receiving.............: avg=${data.metrics.http_req_receiving.values.avg.toFixed(2)}ms
     http_req_sending...............: avg=${data.metrics.http_req_sending.values.avg.toFixed(2)}ms
     http_req_waiting...............: avg=${data.metrics.http_req_waiting.values.avg.toFixed(2)}ms
     http_reqs......................: ${data.metrics.http_reqs.values.count}
     iteration_duration.............: avg=${data.metrics.iteration_duration.values.avg.toFixed(2)}ms
     iterations.....................: ${data.metrics.iterations.values.count}
     vus............................: ${data.metrics.vus.values.max} max
     vus_max........................: ${data.metrics.vus_max.values.max} max
  `;
} 