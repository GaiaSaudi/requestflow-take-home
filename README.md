# RequestFlow Take-Home Starter

RequestFlow is the starter repository for Gaia's senior full-stack engineer production-change exercise.

The repository is intentionally incomplete. It contains realistic defects in the request-decision path for candidates to diagnose and improve. It is **not production software** and must not be used as an authorization or approval system.

Read [ASSIGNMENT.md](./ASSIGNMENT.md) before making changes.

## Start The Application

Requirements:

- Docker with Docker Compose
- GNU Make, or run the equivalent `docker compose` commands directly

Start from a clean checkout:

```bash
cp .env.example .env
make dev
```

Open:

- frontend: <http://localhost:3000>
- backend API docs: <http://localhost:8000/docs>
- health check: <http://localhost:8000/health>

The first backend start applies the database migration and loads deterministic seed data.

## Run Public Tests

```bash
make test
```

The supplied tests prove only the starter baseline. They are intentionally not a complete specification of the assignment's correctness requirements.

## Reset Local Data

```bash
make reset
```

Run `make dev` again to recreate and reseed the database.

## Simulated Sessions

The UI includes a session selector. The corresponding development-only session tokens are:

| User | Token | Team |
| --- | --- | --- |
| Alice Requester | `session-alice` | Platform |
| Bob Reviewer | `session-bob` | Platform |
| Carol Reviewer | `session-carol` | Platform |
| Dana Outsider | `session-dana` | Operations |
| Erin Dual Role | `session-erin` | Platform |

These are deterministic test identities, not credentials or an authentication design.

## Submission Safety

Do not open a solution pull request against this public starter repository. Create a separate repository or archive using the submission instructions provided by the hiring team.
