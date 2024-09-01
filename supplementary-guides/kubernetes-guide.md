# Kubernetes Guide for Docker Users

This guide is designed to help developers familiar with Docker and Docker Compose transition to Kubernetes. It provides tips on creating Kubernetes YAML files, outlines the standard structure of these files, and highlights important considerations when working with Kubernetes.

## Getting Started with Kubernetes YAML Files

### What Files Are Needed?

When transitioning from Docker Compose to Kubernetes, you'll typically need to create several YAML files to define your application's resources. Based on the structure in the `k8s-artifacts` directory, here are the common file types you might need:

1. Deployment YAML (e.g., `postgres-deployment.yaml`, `flask-app-deployment.yaml`)
2. Service YAML (e.g., `postgres-service.yaml`, `flask-app-service.yaml`)
3. Job or CronJob YAML (e.g., `data-pipeline-job.yaml`)

You may also need additional files depending on your application's requirements, such as:

4. ConfigMap YAML (for configuration data)
5. Secret YAML (for sensitive data)
6. PersistentVolume and PersistentVolumeClaim YAML (for persistent storage)

### Standard Structure of Kubernetes YAML Files

Most Kubernetes YAML files follow a similar structure:

```yaml
apiVersion: <API version>
kind: <Resource type>
metadata:
  name: <Resource name>
  labels:
    <key>: <value>
spec:
  <Resource-specific configuration>
```

Key components:
- `apiVersion`: Specifies the Kubernetes API version being used
- `kind`: Defines the type of resource (e.g., Deployment, Service, Job)
- `metadata`: Contains information about the resource, including its name and labels
- `spec`: Describes the desired state of the resource

## Tips for Creating Kubernetes YAML Files

1. **Use a Consistent Naming Convention**: Name your resources consistently. For example, use the same prefix for related resources (e.g., `postgres-deployment`, `postgres-service`).

2. **Leverage Labels and Selectors**: Use labels to organize your resources and selectors to create relationships between them. This is crucial for services to find the correct pods.

3. **Define Resource Requests and Limits**: Always specify CPU and memory requests and limits for your containers to ensure efficient resource allocation.

4. **Use Environment Variables**: Store configuration in environment variables, either directly in the YAML or by referencing ConfigMaps and Secrets.

5. **Create Separate Files for Different Resources**: Unlike Docker Compose, it's common in Kubernetes to have separate YAML files for different resources. This improves readability and maintainability.

6. **Use Multi-Document YAML Files**: You can define multiple resources in a single file by separating them with `---`. This can be useful for closely related resources.

7. **Utilize Kubernetes Secrets**: For sensitive information like database credentials, use Kubernetes Secrets instead of hardcoding values in your YAML files.

## Considerations When Working with Kubernetes

1. **Stateful vs. Stateless Applications**: Kubernetes handles stateless applications differently from stateful ones. For stateful applications like databases, consider using StatefulSets instead of Deployments.

2. **Networking**: Understand how Kubernetes networking works, especially the differences between ClusterIP, NodePort, and LoadBalancer service types.

3. **Persistent Storage**: If your application needs persistent storage, learn about PersistentVolumes and PersistentVolumeClaims.

4. **Health Checks**: Implement readiness and liveness probes to help Kubernetes manage your application's lifecycle effectively.

5. **Rolling Updates**: Leverage Kubernetes' rolling update feature for zero-downtime deployments.

6. **Resource Management**: Be mindful of resource requests and limits to ensure efficient use of cluster resources.

7. **Monitoring and Logging**: Set up proper monitoring and logging for your Kubernetes cluster and applications.

## Differences from Docker Compose

When transitioning from Docker Compose to Kubernetes, keep in mind:

1. **Service Discovery**: Kubernetes uses its own DNS for service discovery, replacing Docker Compose's links.

2. **Volume Management**: Kubernetes has a more complex but powerful system for managing persistent storage.

3. **Environment Variables**: While you can still use environment variables, Kubernetes offers ConfigMaps and Secrets for more flexible configuration management.

4. **Scaling**: Kubernetes allows for more granular and dynamic scaling compared to Docker Compose's simple `scale` directive.

5. **Networking**: Kubernetes networking is more complex but also more powerful, allowing for advanced features like network policies.

For more detailed information on the specific Kubernetes resources used in this project, refer to the [Kubernetes Deployment README](link-to-previous-readme).

## Conclusion

Transitioning from Docker and Docker Compose to Kubernetes involves a learning curve, but it offers powerful features for deploying, scaling, and managing containerized applications. By understanding the structure of Kubernetes YAML files and following best practices, you can effectively leverage Kubernetes for your applications.

Remember to consult the official Kubernetes documentation and use tools like `kubectl explain` to learn more about specific resource types and their configurations.
