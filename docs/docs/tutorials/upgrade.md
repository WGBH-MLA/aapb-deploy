# Upgrading AAPB
This guide provides instructions for upgrading the AAPB application deployed via Helm.

## TLDR
After the automated build process is complete, update the image in the kubernetes deployment.

### Case 1: Using ArgoCD
1. Log in to the ArgoCD web interface
1. Navigate to the AAPB application
1. In the `aapb` deployment resource sub-menu, click the "Refresh" option

The deployment will pull the updated image and restart the pods automatically.