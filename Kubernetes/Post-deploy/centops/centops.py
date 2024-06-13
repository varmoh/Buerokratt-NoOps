import os
import subprocess
import re

# Function to check if a deployment exists in the given namespace
def check_deployment(namespace, deployment):
    cmd = f"kubectl get deployment {deployment} -n {namespace}"
    try:
        subprocess.check_output(cmd, shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Function to apply a YAML file in the given namespace
def install_helm_chart(namespace, tgz_file):
    cmd = f"helm install byk-test {tgz_file} -n {namespace}"
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Installation failed for {tgz_file}. Attempting upgrade...")
        upgrade_helm_chart(namespace, tgz_file)

# Function to upgrade a Helm chart in the given namespace
def upgrade_helm_chart(namespace, tgz_file):
    cmd = f"helm upgrade byk-test {tgz_file} -n {namespace}"
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Upgrade failed for {tgz_file}. Error: {e}")

# Function to get the version number from a tgz filename
def get_version_from_filename(filename):
    match = re.search(r"(\d+\.\d+\.\d+)", filename)
    if match:
        return match.group(1)
    return None

# Main function
def main():
    # Set the repository URL, branch, and charts directory
    repo_url = "https://github.com/buerokratt/buerokratt-helm.git"
    branch = "dev"
    charts_dir = "charts/"

    if repo_url is None or branch is None or charts_dir is None:
        print("Error: Missing environment variables. Please ensure REPO_URL, BRANCH, and CHARTS_DIR are set.")
        return

    # Clone the repository and switch to the specified branch
    try:
        subprocess.run(["git", "clone", "--branch", branch, repo_url], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        return

    # Navigate to the charts directory
    os.chdir(os.path.join(repo_url.split("/")[-1].split(".")[0], charts_dir))

    # Get a list of all .tgz files in the charts directory
    tgz_files = [file for file in os.listdir(".") if file.endswith(".tgz")]

    # Check if there are any .tgz files
    if tgz_files:
        # Check if the deployment exists in the namespace
        namespace = "byk-test"
        deployment = "byk-test"
        if namespace is None or deployment is None:
            print("Error: Missing NAMESPACE or DEPLOYMENT environment variables.")
            return

        for tgz_file in tgz_files:
            # Get the version from the tgz filename
            tgz_version = get_version_from_filename(tgz_file)
            if not tgz_version:
                print(f"Warning: Could not extract version from {tgz_file}. Skipping...")
                continue

            # Check if the deployment exists and get its version
            deployment_exists = check_deployment(namespace, deployment)
            if deployment_exists:
                cmd = f"kubectl get deployment {deployment} -n {namespace} -o=jsonpath='{{.metadata.labels.version}}'"
                try:
                    current_version = subprocess.check_output(cmd, shell=True, text=True).strip()
                except subprocess.CalledProcessError:
                    current_version = None

                if current_version == tgz_version:
                    print(f"Skipping {tgz_file}. It is already deployed with the same version.")
                    continue
                elif current_version is not None and current_version > tgz_version:
                    print(f"Skipping {tgz_file}. The deployed version is newer.")
                    continue

            # Apply the YAML file
            install_helm_chart(namespace, tgz_file)

    else:
        print("No new version found.")

if __name__ == "__main__":
    main()
