#!/bin/bash

NAMESPACE=""
RELEASE_NAME=""
CHART=""

usage() {
  echo "Usage: $0 -n <namespace> -r <release_name> -c <chart>" >&2
  exit 1
}

while getopts ":n:r:c:" option; do
  case $option in
    n)
      NAMESPACE=$OPTARG
      ;;
    r)
      RELEASE_NAME=$OPTARG
      ;;
    c)
      CHART=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      usage
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      usage
      ;;
  esac
done

if [ -z "$NAMESPACE" ] || [ -z "$CHART" ]; then
  echo "Namespace and chart are required."
  usage
fi

case $CHART in
  pipeline)
    helm install "$RELEASE_NAME" ../../Kubernetes/Post-deploy/pipeline -n "$NAMESPACE"
    ;;
  first-login)
    helm install "$RELEASE_NAME" ../../Kubernetes/Post-deploy/first-login -n "$NAMESPACE"
    ;;
  dmapperv1)
    helm install "$RELEASE_NAME" ../../Kubernetes/Post-deploy/dmapperv1 -n "$NAMESPACE"
    ;;
  byk-bot)
    releaseName=$(yq eval '.releaseName' ../../Kubernetes/Components/Bot/values.yaml)
    if [ -z "$releaseName" ]; then
      echo "Enter release name for byk-bot:"
      read -r releaseName
    fi
    helm install "$releaseName" ../../Kubernetes/Components/Bot -n "$NAMESPACE"
    ;;
  *)
    echo "Invalid chart specified: $CHART" >&2
    usage
    ;;
esac
