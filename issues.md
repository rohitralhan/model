# LV Challenges and Issues

## Resolved Issues

### Unable to pull images

#### Summary

We are unable to pull images from the quay.io registry

#### Additional Details

The service account associated with the pull secret provisioned by LinkerVision to pull images into the T-Mobile environment from quay.io were not granted correct permissions to access all required images.

#### Actions Taken

LinkerVision updated permissions to the service account.

### Unable to connect to LinkerVision MQTT

#### Summary

Linkervision `edge-agent` needs to be able to connect to an MQTT server hosted in their AWS instance.  

#### Additional Details

The `edge-agent` needs to be able to connect to `mqtt-staging.visionai.linkervision.ai:1883`.

#### Actions Taken

Port 1883 was opened on the T-Mobile network to connect to `mqtt-staging.visionai.linkervision.ai` but the issue persisted.

LinkerVision had to configure additional updates on their side to allow the connection from T-Mobile.

### Edge Agent Unhandled Exception

#### Summary

The edge-agent has an unhandled exception that is causes the application to crash.

#### Additional Details

The edge agent is attempting to process details from the k8s nodes and throwing an error related to the node reporting `50M` of ephemeral-storage.

The edge agent is only expecting `Mi` while `M` is a valid k8s value.

```
Traceback (most recent call last):
  File "/app/manage.py", line 25, in <module>
    execute_from_command_line(sys.argv)
  File "/usr/local/lib/python3.10/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
    utility.execute()
  File "/usr/local/lib/python3.10/site-packages/django/core/management/__init__.py", line 436, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "/usr/local/lib/python3.10/site-packages/django/core/management/base.py", line 412, in run_from_argv
    self.execute(*args, **cmd_options)
  File "/usr/local/lib/python3.10/site-packages/django/core/management/base.py", line 458, in execute
    output = self.handle(*args, **options)
  File "/app/apps/agent/management/commands/run_edge_agent.py", line 82, in handle
    asyncio.run(
  File "/usr/local/lib/python3.10/asyncio/runners.py", line 44, in run
    return loop.run_until_complete(main)
  File "/usr/local/lib/python3.10/asyncio/base_events.py", line 649, in run_until_complete
    return future.result()
  File "/app/apps/agent/management/commands/run_edge_agent.py", line 56, in run_kube_agent
    await asyncio.gather(*agent.start(), *custom_agents)
  File "/app/apps/ai_model/agent.py", line 968, in report_node_list_loop
    await self.report_node_list()
  File "/app/apps/ai_model/agent.py", line 1002, in report_node_list
    parse_kubectl_describe_node(describe_node_list[index]),
  File "/app/apps/ai_model/agent.py", line 121, in parse_kubectl_describe_node
    ret["disk"] = parse_value_to_mb(parts[1])
  File "/app/apps/ai_model/agent.py", line 91, in parse_value_to_mb
    value = int(value)
ValueError: invalid literal for int() with base 10: '50M'
```

### Actions Taken

LinkerVision updated application code.

## Active Issues With Work Arounds

### Stream Agent UID

#### Summary

OpenShift expects all containers to run as a Random UID and stream-agent is attempting to run as root.

#### Additional Details

This is a common issue for applications new to OpenShift.  The Random UID is a security feature of OpenShift.

Additionally, the stream-agent pod is running as the default service account instead of a dedicated service account.

#### Work Around

We were able to manually create a serviceAccount and add it to the Deployment in the stream-agent-template configmap.

After the ServiceAccount was created, we were able to apply the `privileged` SCC to the service account and grant permissions to run the pod with root.

Running as root is generally considered a critical security concern.

#### Actions To Be Taken

LinkerVision to investigate running the container as the expected random UID.

https://www.redhat.com/en/blog/a-guide-to-openshift-and-uids

### Stream Agent using Host Storage

#### Summary

The stream agent application is attempting to utilize host storage.

#### Recommended Additional Details

Accessing host storage is a voliotion of Red Hat support policies and is considered a critical security concern.

#### Work Around

The `stream-agent-template` configmap was updated to deploy a StatefulSet instead of a standard deployment object with PVCs.

#### Recommended Actions To Be Taken

LinkerVision should invistage using a StatefulSet by default and storing data on a PVC.

### Stream Agent attempting to deploy on Control Plane Nodes

#### Summary

The edge agent creates a copy of the stream-agent for each node, including the control plane nodes.

#### Additional Details

Scheduling workloads on control plane nodes is a violation of the OpenShift support policy unless the nodes have been deployed as hyperconverged infrastructure (control plane nodes are also provisioned as worker nodes).

LinkerVision appears to be deploying on multiple nodes by creating a unique Deployment for each node.

#### Work Arounds

Multiple-replicas are not critical at this point in time.  We were able to get a single instance running successfully and allowed the additional replicas to remain pending.

#### Recommended Actions To Be Taken

LinkerVision should consider migrating to StatefulSets and leverage the multi-replica capabilities instead of creating a unique Deployment for every node.  If scheduling the replicas on different nodes are critical, LinkerVision should consider using NodeAntiAffinity.  If scheduling the replicas on every working node is critical, LinkerVision should consider DaemonSets.

### Prometheus Conflicts

#### Summary

OpenShift deploys a Prometheus instance by default.

Applications are allowed to deploy their own Prometheus instance that monitors additional resources outside of their namespaces.

#### Additional Details

OpenShift allows third party applications to deploy Prometheus instances onto the cluster as long as they are limited in scope to specific namespaces.

The Prometheus instance

#### Work Arounds

The edge-agent service account was granted the `cluster-monitor-view` role which grants permissions to query the OpenShift prometheus instance.  The helm chart was also updated to point to the OpenShift Prometheus endpoint.

Note: `cluster-monitor-view` access grants Prometheus access to all metrics data collected from all workloads running on the cluster.  LinkerVision also forwards this data to their cloud platform which could include non-LinkerVision tenants.

Additionally, LinkerVision updated the application code to ignore the TLS cert on the cluster prometheus service endpoint, and read the Service Account token that is automatically mounted in the container.

#### Recommended Actions To Be Taken

LinkerVision should explore limiting the scope of their Prometheus instance to only the namespaces they are responsible for managing and avoiding conflicting with the OpenShift Prometheus instance.

### Inference Deployment Config Issues

#### Summary

LinkerVision is responsible for pushing deployment objects from their cloud environment to the cluster to create model servers.

The deployments pushed from the cloud environment include several manual configurations that require additional changes after the configs have been pushed to the cluster.

#### Additional Details

Changes include:

* Updating the image registry to quay.io/hellosimon27
* Manually specifying `nvidia.com/gpu: 1` as a resource request/limit
* Remove `runtimeClassName: nvidia`

Additionally, Inference servers are created with multiple deployment objects to create unique replicas instead of using traditional "replicas" feature built into deployments. 

#### Work Arounds

Manually change the required options in the Deployment after it is applied to the cluster.

#### Recommended Actions To Be Taken

LinkerVision to enable additional options to configure specific features when deploying resources.

LinkerVision should investigate leveraging traditional Deployment replica sets to manage multiple replicas.

## Non-Blocking Issues For Later Consideration

### Cluster Admin Privledges for edge-agent

#### Summary

The edge-agent is currently being granted cluster admin privledges which will allow it to view and edit all resources on the cluster, including other tenants resources.

#### Additional Details

The `observ-edge` helm chart is creating multiple ClusterRoleBindings granting `cluster-admin` and a custom role granting broad `*` permissions.

The `ClusterRoleBinding` does includes a `namespace` definition which is not valid as a `ClusterRoleBinding` is a cluster scoped object.  The intention may have been to to grant admin permississions to the specific namespaces, but a broader, cluster wide access was provisioned.

#### Recommended Actions To Be Taken

LinkerVision should audit the specific permissions required for their application and create a custom role following the principal of least priveledge.
