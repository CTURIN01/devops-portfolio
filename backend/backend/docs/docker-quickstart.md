# Docker Quickstart

## Start the full stack
Run: docker-compose up --build

## Stop the stack
Run: docker-compose down

## Check running containers
Run: docker ps

## View logs
Run: docker-compose logs -f

## Common issues

### Port already in use
- Stop the conflicting process or change the port in docker-compose.yml

### Database connection refused
- Wait 5-10 seconds after startup for MySQL to initialize
- Check DB_HOST matches the service name in docker-compose.yml

### Changes not reflecting
- Rebuild the image with: docker-compose up --build
