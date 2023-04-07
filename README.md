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

### Run Docker container

```bash
docker run --rm portainer-redeploy \
  --url=(Url) \
  --apiKey=(String) \
  --endpointId=(Int) \
  --stackName=(String) \
  --prune=1 # optional
```

### Drone CI example

```yaml
  - name: deploy
    image: organization/portainer-redeploy:latest
    entrypoint: []
    commands:
      - >
        if [ "$DRONE_COMMIT_BRANCH" = "develop" ]; then
          STACK_NAME=project-dev
        elif [ "$DRONE_COMMIT_BRANCH" = "release" ]; then
          STACK_NAME=project-stage
        elif [ "$DRONE_COMMIT_BRANCH" = "main" ]; then
          STACK_NAME=project-prod
        else
          echo "Stack name not found"
          exit 1
        fi

        python /app/main.py --url=$PORTAINER_URL \
          --apiKey=$PORTAINER_API_KEY --endpointId=1 --stackName=$STACK_NAME
    environment:
      PORTAINER_URL:
        from_secret: portainer_url
      PORTAINER_API_KEY:
        from_secret: portainer_api_key
    when:
      branch:
        - main
        - develop
        - release
      event:
        - push
    depends_on:
      - push-to-registry
```