# Troubleshooting Docker Compose Deployments

When a Docker Compose deployment doesn't work as expected, there are several commands and strategies you can use to diagnose and resolve issues. This guide provides common troubleshooting steps and explains what each command does and when to use it.

## Viewing Logs

### View logs for all services
To see the logs for all services defined in your `docker-compose.yml` file:

```sh
docker-compose logs
```

Use this command to get an overview of what's happening across all your services. It's particularly useful for identifying which service might be causing issues.

### View logs for a specific service
To see the logs for a particular service:

```sh
docker-compose logs <service-name>
```

Use this when you've identified a problematic service and need to investigate its logs in detail.

### Follow logs in real-time
To continuously stream the logs:

```sh
docker-compose logs -f
```

This is useful when you're actively debugging and want to see log entries as they occur.

## Checking Service Status

### List services and their status
To see the current status of all services:

```sh
docker-compose ps
```

Use this to quickly check which services are running, which have exited, and their current state.

## Rebuilding and Restarting Services

### Rebuild images and restart services
If you've made changes to your Dockerfile or service configuration:

```sh
docker-compose up --build
```

This command rebuilds the images and starts the containers. Use it when you've made changes to your application code or Dockerfile.

### Force recreation of containers
To force Docker Compose to stop and recreate all containers:

```sh
docker-compose up --force-recreate
```

This is useful when you suspect there might be issues with the existing containers that a simple restart won't fix.

## Cleaning Up

### Stop and remove containers, networks, and volumes
To clean up your Docker Compose deployment:

```sh
docker-compose down -v
```

The `-v` flag also removes named volumes. Use this when you want to start fresh or when troubleshooting issues related to persistent data.

### Remove all unused Docker data
For a more thorough cleanup:

```sh
docker system prune -a --volumes
```

This removes all unused containers, networks, images, and volumes. Use it cautiously, as it affects all Docker resources on your system, not just those related to your current project.

## Checking Resource Usage

### View resource usage of containers
To see CPU, memory, and network usage of your containers:

```sh
docker stats
```

Use this to identify if any containers are using excessive resources, which might indicate performance issues.

## Inspecting Containers

### Get detailed information about a container
To see detailed information about a specific container:

```sh
docker inspect <container-id>
```

This provides a wealth of information about the container's configuration, network settings, and more. It's useful for diagnosing networking or configuration issues.

## Accessing Containers

### Start an interactive shell in a running container
To get a shell inside a running container:

```sh
docker-compose exec <service-name> /bin/bash
```

This allows you to explore the container's filesystem, check configurations, and run commands directly inside the container. It's invaluable for hands-on troubleshooting.

## Conclusion

When troubleshooting Docker Compose deployments, start with viewing logs and checking service status. If issues persist, try rebuilding and restarting services. For more complex problems, inspect containers and their resource usage. Remember to clean up your Docker environment regularly to prevent issues caused by stale or conflicting resources.

Always refer to the official Docker and Docker Compose documentation for the most up-to-date and comprehensive information on troubleshooting and managing your deployments.
