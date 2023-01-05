upgrade_db:
	@echo "Database initialization is started"
	@docker-compose exec -ti api alembic upgrade head
	@echo "Database initialization is finished"
