# Architecture

The platform uses an API gateway for routing and cross-cutting concerns (request IDs, rate limiting, cache), and four domain AI microservices.

Shared package includes config, OpenAI client, logging, DB models, and schemas.
