import requests
import argparse
import json


def main(args):
    stack_id = ""
    env = {}
    git_reference_name = ""
    git_username = ""

    response = requests.get(args.url + "/api/stacks", headers={
        "X-API-Key": args.apiKey
    })

    stacks = json.loads(response.content)

    for stack in stacks:
        if stack["Name"] == args.stackName and stack["EndpointId"] == args.endpointId:
            stack_id = stack["Id"]
            env = stack["Env"]
            git_reference_name = stack["GitConfig"]["ReferenceName"]
            git_username = stack["GitConfig"]["Authentication"]["Username"]
            break

    if stack_id == "":
        raise SystemExit(f"Stack with name {args.stackName} not found.")

    data = {
        "env": env,
        "prune": False,
        "pullImage": True,
        "repositoryAuthentication": True,
        "repositoryReferenceName": git_reference_name,
        "repositoryUsername": git_username,
    }

    if args.prune:
        data["prune"] = True

    print("Running redeploy...")

    response = requests.put(
        args.url + "/api/stacks/" + str(stack_id) + "/git/redeploy?endpointId=" + str(args.endpointId),
        headers={
            "X-API-Key": args.apiKey
        },
        json=data
    )

    if response.status_code > 200:
        raise SystemExit(f"Redeploy was finished with error " + str(response.status_code) + ":\n" + str(response.content))

    print("Success")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Portainer stack redeploy tool",
        description="Redeploys stack from git"
    )
    parser.add_argument("--url", type=str, required=True, help="Base Portainer's service URL")
    parser.add_argument("--apiKey", type=str, required=True, help="Portainer API Key")
    parser.add_argument("--endpointId", type=int, required=True, help="Environment ID")
    parser.add_argument("--stackName", type=str, required=True, help="Stack name")
    parser.add_argument("--prune", type=bool, required=False, help="Prune unused services")

    main(parser.parse_args())
