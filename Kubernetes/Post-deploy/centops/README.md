## CentOps cronjob for K8s

This is to be deployed into a k8s environment,   
where the cronjob checks Buerokratt-Helm repo charts/ for versions of charts.tgz and if new one is available,  
pulls it and either deploys new install or upgrades existing one.

Currently image to use inside `cronjob.yaml` can be found here `insert dockerhb url`  

##### Changes to make before deploying this  

Inside cronjob.yaml change:  
    - `image: repo/centops-cron-image:tag` change it to the latest image fro dockerhub  
    - `name: NAMESPACE` change it to the namespace that you use in k8s  
    - `value: "your-deployment"` change it to reflect your deployment  



##### Local test (without k8s)  #####
- In this test build image locally (or use dockerhub image)
    
    `docker build -t centops . `

- Run following command (no need to change anything)   

    ```
    docker run --rm -it \
    -e REPO_URL="https://github.com/buerokratt/buerokratt-helm" \
    -e BRANCH="dev" \
    -e CHARTS_DIR="charts/" \
    -e NAMESPACE="your-namespace" \
    -e DEPLOYMENT="your-deployment" \
    your/repo-checker-image:tag
    
    ```  

- Local test outcome (unless you have a local k8s running) should look like this  

    ```
    Cloning into 'buerokratt-helm'...
    remote: Enumerating objects: 1717, done.
    remote: Counting objects: 100% (703/703), done.
    remote: Compressing objects: 100% (314/314), done.
    remote: Total 1717 (delta 369), reused 546 (delta 306), pack-reused 1014
    Receiving objects: 100% (1717/1717), 4.41 MiB | 8.49 MiB/s, done.
    Resolving deltas: 100% (962/962), done.
    /bin/sh: 1: kubectl: not found
    /bin/sh: 1: kubectl: not found
    Traceback (most recent call last):
    File "/app/centops.py", line 89, in <module>
        main()
    File "/app/centops.py", line 83, in main
        apply_yaml(namespace, tgz_file)
    File "/app/centops.py", line 17, in apply_yaml
        subprocess.run(cmd, shell=True, check=True)
    File "/usr/local/lib/python3.9/subprocess.py", line 528, in run
        raise CalledProcessError(retcode, process.args,
    subprocess.CalledProcessError: Command 'kubectl apply -f chat_backoffice-0.1.0.tgz -n your-namespace' returned non-zero exit status 127.```
