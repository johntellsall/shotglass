# chatgpt: "sample code for diagrams.mingrammer.com for  Nginx in K8s"and

from diagrams import Diagram, Cluster
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Service
from diagrams.k8s.infra import Node

with Diagram("Nginx in Kubernetes", show=False):
    with Cluster("Kubernetes Cluster"):
        ingress_controller = Pod("Nginx Ingress Controller")
        web_app = Pod("Web App")
        service = Service("Nginx Service")

        ingress_controller - [web_app, service]

    with Cluster("External Network"):
        internet = Node("Internet")

        ingress_controller - internet
