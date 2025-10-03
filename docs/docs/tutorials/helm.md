# Helm chart deployment
[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/aapb)](https://artifacthub.io/packages/search?repo=aapb)

AAPB can be deployed as a simple Helm Chart to a Kubernetes cluster.

!!! kube "Setup"

    If you haven't set up a production environment, follow the steps in [Quickstart](quickstart.md) first.

### Install
Add the Helm repository:
```sh
helm repo add aapb https://wgbh-mla.github.io/aapb-deploy
```

Update the charts:
```sh
helm repo update
```

Customize the values in `values.yaml` to your needs. You can also use `--set` to override values on the command line.
```yaml
global:
  backend:
    image:
      tag: latest
```

Install the Helm chart:
```sh
helm install my-aapb aapb/aapb
```

### Upgrade
```sh
helm upgrade my-aapb aapb/aapb
```

### Values
See the [values.yaml](https://github.com/WGBH-MLA/aapb-deploy/blob/main/charts/aapb/values.yaml) file for the full list of configurable values and their defaults.

### Uninstall
```sh
helm uninstall [release-name]
```
... where `[release-name]` is the name you used when installing the chart (e.g. `my-aapb`).