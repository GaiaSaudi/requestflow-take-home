.PHONY: dev test reset logs

dev:
	docker compose up --build

test:
	docker compose run --rm backend uv run pytest
	docker compose run --rm frontend npm run test -- --run

reset:
	docker compose down --volumes --remove-orphans

logs:
	docker compose logs --follow
