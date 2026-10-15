# Architecture

This section provides a high-level overview of the architecture of the AAPB application, including its components and how they interact with each other.

## Deployment

The AAPB application is deployed on a Kubernetes cluster using Helm charts for package management and Argo CD for continuous deployment.

The following diagram illustrates the kubernetes architecture of a single AAPB instance:

![AAPB Instance Deployment Architecture](aapb-instance-deployment.svg)

For installation instructions, see the [Quickstart Guide](../tutorials/quickstart.md).

## GitOps
Deployments are managed using a GitOps strategy, with Argo CD Applications.

The following diagram illustrates the GitOps architecture of the [aapb-deploy repository](https://github.com/WGBH-MLA/aapb-deploy/):

![GitOps Architecture](gitops-architecture.svg)

## Production Ingress

Production traffic for `americanarchive.org` enters through a Traefik `IngressRoute` ([production/ingressroute.yaml](https://github.com/WGBH-MLA/aapb-deploy/blob/main/production/ingressroute.yaml)). The router with the highest `priority` that matches a request wins, and each router runs its own middleware chain before forwarding to the `aapb` Service, an `ExternalName` for `aapb-prod.wgbh-mla.org:443`.

### Route selection

```mermaid
flowchart TD
    client(["Host: americanarchive.org"]) --> m100{"<strong>Priority 100</strong><br/>GBH IP Address?"}

    m100 -->|"yes"| c100["<strong>aapb-cache</strong>"] --> l100["<strong>private-ratelimit</strong><br/>50/s, burst 100"] --> svc
    m100 -->|"no"| m20{"<strong>Priority 20</strong><br/>/turnstile_challenge or /turnstile_verify?"}

    m20 -->|"yes"| l20["<strong>public-ratelimit</strong><br/>10/s, burst 20"] --> svc
    m20 -->|"no"| m10{"<strong>Priority 10</strong><br/>/catalog*?"}

    m10 -->|"yes"| r10["<strong>catalog chain</strong><br/>(detailed below)"] --> svc
    m10 -->|"no"| r1["<strong>Priority 1</strong><br/>everything else"] --> c1["<strong>aapb-cache</strong>"] --> l20

    svc["service: <strong>aapb</strong>"]
```

The priority 20 route has no `human-id` middleware. The Turnstile challenge and its static assets must stay reachable without a verified cookie, or visitors would be redirected in a loop.

### `/catalog` middleware chain

Middlewares run top to bottom. `human-id` runs before `aapb-cache` so that the challenge redirect is never cached.

```mermaid
flowchart TD
    in(["<strong>/catalog*</strong>"]) --> rlp["<strong>rate-limited-page</strong><br/>replaces any 429 body with the /429 page"]
    rlp --> hid["<strong>human-id</strong><br/>forwardAuth"]

    hid -->|"no valid cookie"| redirect(["302 to /turnstile_challenge"])
    hid <-.->|"<strong>GET /turnstile_check</strong><br/>sends Cookie, returns X-Aapb-Human-Id"| check[("aapb-prod.wgbh-mla.org")]
    hid -->|"200 with X-Aapb-Human-Id"| human

    subgraph human["<strong>Human Ratelimits</strong><br/>keyed on X-Aapb-Human-Id"]
        direction TB
        h1["3/3s, burst 5"] --> h2["10/1m, burst 15"] --> h3["20/5m, burst 30"] --> h4["60/1h, burst 80"] --> h5["180/24h, burst 120"]
    end

    human --> ip

    subgraph ip["<strong>Global ratelimits</strong><br/>Combined /catalog traffic"]
        direction TB
        g1["4/1s, burst 16"] --> g2["8/3s, burst 32"] --> g3["16/10s, burst 48"] --> g4["30/30s, burst 120"] --> g5["100/2m, burst 300"] --> g6["150/5m, burst 400"]
    end

    ip --> cache["aapb-cache"] --> svc["Service aapb"]

    human -.->|"limit exceeded"| tooMany(["429 Too Many Requests"])
    ip -.->|"limit exceeded"| tooMany
    tooMany -.->|"body replaced via rate-limited-page"| rlp
```

### Where things are defined

| Resource | File |
|---|---|
| `IngressRoute` | [production/ingressroute.yaml](https://github.com/WGBH-MLA/aapb-deploy/blob/main/production/ingressroute.yaml) |
| `rate-limited-page`, `human-id`, `human-id-ratelimit-*` | [production/human-ratelimits.yaml](https://github.com/WGBH-MLA/aapb-deploy/blob/main/production/human-ratelimits.yaml) |
| `private-ratelimit`, `public-ratelimit`, `global-ratelimit-*` | [production/site-ratelimits.yaml](https://github.com/WGBH-MLA/aapb-deploy/blob/main/production/site-ratelimits.yaml) |
| `aapb-cache` | Defined in the cluster only, not in this repository |
