# TitanFabric API

Base URL: `http://127.0.0.1:8000`

## `GET /health`

Returns service status.

## `GET /fabrics`

Optional query parameters:

- `category`: `linen`, `cotton`, `denim`, `silk`, or `knit`
- `sustainable`: `true` or `false`
- `max_price`: numeric price ceiling per yard

## `GET /fabrics/{fabric_id}`

Returns one fabric or `404` when the fabric is unknown.

## `POST /quotes`

Example request:

```json
{
  "customer_name": "Maya Chen",
  "email": "maya@example.com",
  "destination": "domestic",
  "items": [
    { "fabric_id": "tf-linen-01", "yards": 35 }
  ],
  "notes": "Need swatches before full order."
}
```

The response includes normalized minimum yardage, shipping, service fee, and estimated total.
