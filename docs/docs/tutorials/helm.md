# Helm chart deployment

!!! kube "Setup"

    If you haven't set up a production environment, follow the steps in [Quickstart](quickstart.md) first.

## Helm
The recommended way to deploy AAPB is using the Helm Chart.

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
