workers = 8
worker_class = "uvicorn.workers.UvicornWorker"
bind = "0.0.0.0:8000"
accesslog = "-"
proxy_allow_ips = "*"
raw_env = ['prometheus_multiproc_dir={{ env "PROMETHEUS_DIR" | default "/var/run/prometheus"}}']
