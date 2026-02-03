from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import InternetGateway, ELB
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.management import Cloudwatch
from diagrams.onprem.client import Users

with Diagram("Arquitectura AWS - Aplicación Flask", 
             filename="docs/diagramas/arquitectura-aws",
             show=False,
             direction="TB",
             graph_attr={
                 "fontsize": "12",
                 "bgcolor": "white",
                 "pad": "1.0",
                 "nodesep": "1.5",
                 "ranksep": "1.5",
                 "splines": "ortho",
                 "concentrate": "false"
             }):
    
    # Capa externa: Usuarios
    users = Users("Usuarios")
    igw = InternetGateway("Internet Gateway")
    
    # VPC
    with Cluster("VPC Production"):
        
        # ALB (implícitamente en subnets públicas)
        alb = ELB("Application Load Balancer\nHTTPS:443 + SSL/TLS")
        
        # Availability Zones en paralelo
        with Cluster("AZ eu-west-1a"):
            ec2_1 = EC2("EC2-1\nFlask + Docker\nt2.micro\n(Private Subnet)")
        
        with Cluster("AZ eu-west-1b"):
            ec2_2 = EC2("EC2-2\nFlask + Docker\nt2.micro\n(Private Subnet)")
        
        # Base de datos
        db = RDS("RDS PostgreSQL 15\nMulti-AZ\ndb.t3.micro")
    
    # CloudWatch fuera
    cw = Cloudwatch("AWS CloudWatch\nLogs & Metrics")
    
    # Flujo principal (flechas sólidas azules/verdes)
    users >> Edge(label="HTTPS", color="darkblue", style="bold") >> igw
    igw >> Edge(color="darkblue") >> alb
    alb >> Edge(label="5000", color="darkgreen") >> ec2_1
    alb >> Edge(label="5000", color="darkgreen") >> ec2_2
    ec2_1 >> Edge(label="5432", color="green") >> db
    ec2_2 >> Edge(label="5432", color="green") >> db
    
    # Monitorización (flechas punteadas naranjas, DIRECTAS sin cruzar)
    ec2_1 >> Edge(style="dashed", color="orange") >> cw
    ec2_2 >> Edge(style="dashed", color="orange") >> cw
    db >> Edge(style="dashed", color="orange") >> cw

print("✅ Diagrama limpio creado")