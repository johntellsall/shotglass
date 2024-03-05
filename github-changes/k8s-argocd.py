from diagrams import Diagram, Cluster
from diagrams.k8s.compute import Pod
from diagrams.k8s.others import CRD as CustomResourceDefinition
from diagrams.k8s.ecosystem import Helm
from diagrams.k8s.infra import Node

with Diagram("ArgoCD in Kubernetes", show=False):
    with Cluster("Kubernetes Cluster"):
        argocd_server = Pod("ArgoCD Server")
        argocd_repo = CustomResourceDefinition("ArgoCD Repository")
        argocd_apps = Helm("ArgoCD Applications")

        argocd_server - argocd_repo
        argocd_server - argocd_apps

    with Cluster("External Network"):
        internet = Node("Internet")

        argocd_server - internet

