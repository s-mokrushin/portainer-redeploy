# Portainer stack redeploy tool

Works only with stacks, configured by git repository.

What the script do:

* Loads exist stack
* Copies envs and auth params
* Sends PUT request to api/stacks/[StackId]/git/redeploy

## Build

```bash
docker build --tag=portainer-redeploy:latest .
```

## Usage

```bash
docker run --rm portainer-redeploy \
  --url=(Url) \
  --apiKey=(String) \
  --endpointId=(Int) \
  --stackName=(String) \
  --prune=1 # optional
```
