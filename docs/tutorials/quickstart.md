# Quickstart

## Prerequisites
These instructions assume you have the following:

- A working Kubernetes cluster
- `kubectl`, configured to connect to your cluster
- `helm` installed and configured


## Helm Repository
Add the Helm repository for the AAPB application:
```bash
helm repo add aapb https://wgbh-mla.github.io/aapb-deploy/
helm repo update
```

??? kube "Namespaces"

    ### Create a namespace
    Create a new namespace, in this case: `aapb`:

    ```bash
    kubectl create namespace aapb
    ```

    Set the current context to the new namespace:
    ```bash
    kubectl config set-context --current --namespace=aapb

    # Verify the current context
    kubectl config view --minify | grep namespace:
    ```


## Install the Application
Install the AAPB application using Helm:
```bash
helm install aapb aapb/aapb -n aapb
```
