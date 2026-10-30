# 24. Deployment, APIs and operational ownership

![Production deployment with independent ingestion and query planes](../diagrams/24-deployment.png)

## Components and responsibilities
FastAPI or an equivalent API layer authenticates requests, validates input and binds tenant scope. Ingestion workers process files asynchronously. SQS/Kafka or another durable queue handles retries and backpressure. Object storage keeps originals and parse artifacts. PostgreSQL owns metadata/job/publication state. OpenSearch and a vector store provide search; using pgvector can consolidate one store. Neo4j is optional for relationship workloads. Redis is optional for scoped caches. A model gateway centralizes provider timeouts, quotas and safe telemetry.

Do not deploy every listed tool just because it appears in a textbook stack. Each extra distributed component adds consistency, backup, security and recovery responsibilities. Managed services reduce some operations but introduce limits, cost and residency considerations.

## API contracts
`POST /documents`: authorized upload/source reference -> accepted job ID. `GET /jobs/{id}`: permitted job state, errors and published version. `POST /query`: question/history/business filters -> answer, citations, unresolved gaps, trace ID and applicable version. Derive identity and access server-side; never trust a body field claiming another tenant. Validate upload ownership and source-connector permissions too.

## Deployment and index lifecycle
Build immutable application images with pinned dependencies. Run migrations compatibly with old/new versions during rollout. Workers and APIs scale independently. Keep service processes stateless where possible, with durable job/state stores. Health checks should distinguish live process, dependency readiness and model availability. Test representative functional requests, not only open ports.

Publish index manifests after validation. Blue/green aliases or application manifests allow rollback. Model, chunker, analyzer, schema and index versions belong in deployment metadata. A rollback must preserve source/ACL semantics; revoking a permission must not be undone by rolling back the application.

## Scaling and recovery
Shard based on measured index size, tenant distribution and query pattern. Too many shards add coordination overhead. Tenant-per-index gives stronger operational separation but may create many tiny indexes; shared indexes require rigorously enforced scope. Heavy tenants may need dedicated resources. Autoscale on queue age, active work and resource utilization rather than one metric alone.

Use infrastructure as code for reviewable resources and policies. Back up source and metadata stores, and know which indexes can be rebuilt. Test restore time against recovery objectives. Kubernetes, Docker and Terraform are implementation options, not proof of availability. Live processes and connections do not survive a snapshot by assumption.

**Interview answer:** “I separate ingestion throughput from interactive latency, make versions publishable/rollbackable, and test both normal readiness and recovery.” **Follow-up:** “What is highly available?” **Response:** “The complete required path, including metadata, search, authentication and model dependency—not just two API replicas.”
