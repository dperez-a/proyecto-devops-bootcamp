from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import VPC, InternetGateway, ELB, Route53
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.general import Users

# Configuración del diagrama
with Diagram("Arquitectura AWS - Aplicación Flask", 
             filename="docs/diagramas/arquitectura-aws",
             show=False,
             direction="TB",
             graph_attr={
                 "fontsize": "14",
                 "bgcolor": "white",
                 "pad": "0.5"
             }):
    
    users = Users("Usuarios")
    igw = InternetGateway("Internet Gateway")
    
    with Cluster("VPC - Production"):
        alb = ELB("Application\nLoad Balancer\n(HTTPS/SSL)")
        
        with Cluster("Availability Zone eu-west-1a"):
            with Cluster("Private Subnet 1a"):
                ec2_1 = EC2("EC2-1\nFlask + Docker\nt2.micro")
        
        with Cluster("Availability Zone eu-west-1b"):
            with Cluster("Private Subnet 1b"):
                ec2_2 = EC2("EC2-2\nFlask + Docker\nt2.micro")
        
        with Cluster("Database Layer"):
            db = RDS("RDS PostgreSQL 15\nMulti-AZ\ndb.t3.micro")
    
    monitoring = Cloudwatch("CloudWatch\nLogs & Metrics")
    
    users >> Edge(label="HTTPS") >> igw >> alb
    alb >> Edge(label="HTTP:5000") >> ec2_1
    alb >> Edge(label="HTTP:5000") >> ec2_2
    ec2_1 >> Edge(label="PostgreSQL:5432") >> db
    ec2_2 >> Edge(label="PostgreSQL:5432") >> db
    
    ec2_1 >> Edge(label="logs", style="dashed", color="orange") >> monitoring
    ec2_2 >> Edge(label="logs", style="dashed", color="orange") >> monitoring
    db >> Edge(label="metrics", style="dashed", color="orange") >> monitoring

print("✅ Diagrama creado en: docs/diagramas/arquitectura-aws.png")
