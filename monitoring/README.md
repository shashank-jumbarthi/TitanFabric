# Monitoring

Suggested production checks:

- `GET /health` every 60 seconds.
- API error-rate alert above 2% over 10 minutes.
- Quote-submission latency p95 below 750 ms.
