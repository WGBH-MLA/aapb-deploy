# AAPB: Deploy
[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/aapb)](https://artifacthub.io/packages/search?repo=aapb)

## About

Deployment documentation for the American Archive of Public Broadcasting (AAPB) website: [americanarchive.org](https://americanarchive.org/)

## Install
### Add the Helm repository:

```sh
helm repo add aapb https://wgbh-mla.github.io/aapb-deploy
helm repo update
```
### Install the AAPB Helm chart:

```sh
helm install my-aapb aapb/aapb
```

Optional: Change `my-aapb` to the name of your release

## Links

- Website: [americanarchive.org](https://americanarchive.org/)
- Demo: [aapb.dev.wgbh-mla.org](https://aapb.dev.wgbh-mla.org/)
- Code: [github.com/WGBH-MLA/dream-aapb](https://github.com/WGBH-MLA/dream-aapb)
- Artifact Hub: [artifacthub.io/packages/helm/aapb/aapb](https://artifacthub.io/packages/helm/aapb/aapb)
- Documentation: [wgbh-mla.github.io/aapb-deploy](https://wgbh-mla.github.io/aapb-deploy)

## Credits

Developed by the [Media Library and Archives](https://www.wgbh.org/foundation/what-we-do/media-library-and-archives) at [GBH Boston](https://wgbh.org)
