import os 
import subprocess
import time 


# conf 1 zone at a time
class BindSetup():

    DB_REVERSE_RECORD=[]

    def __init__(self, zone = "a10.networks.com", ip = "30.30.30.10", record = ["www    IN  A   127.0.0.1"]) -> None:

        self.zone= zone
        self.IP_ADDRESS=ip
        self.prefix = "www"
        self.DB_RECORDS = record

    def init(self, fw_record = [], rev_record = []):
        try:
            subprocess.run(["sudo", "apt", "install", "bind9"])
            time.sleep(10)
            os.chdir("etc/bind9")
            print(os.getcwd())
        except FileNotFoundError:
            print(f"Error : FileNotFound ")
        except Exception as e:
            print(f"Error: {str(e)}")
        print("/etc/bind9" in os.getcwd())
        if(True or "/etc/bind9" in os.getcwd() ):
            print("copying original files")
            subprocess.run(["sudo", "cp", "named.conf.options", "named.conf.options.orig"])
            subprocess.run(["sudo", "cp", "named.conf.local", "named.conf.local.orig"])

            with open("db.ip", "w") as file:
                file.write(self.Forward_Db_File())

        #     with open("db.domain", "w") as file:
        #         self.dbRecord(ip="40.40.40.100")
        #         self.dbRecord(ip="40.40.40.101")
        #         file.write(createDBLocal())
          
    def Forward_Db_File(self):

        return f"$TTL    604800 \n \
            @       IN      SOA     ns1.{self.zone}. root.{self.zone}. (\n \
                                    2         ; Serial\n \
                                604800         ; Refresh\n \
                                86400         ; Retry\n \
                                2419200         ; Expire\n \
                                604800 )       ; Negative Cache TTL\n \
        ;\n \
        @       IN      NS      ns1.{self.zone}.\n \
        {'\n'.join(self.DB_RECORDS)} \n\
        @       IN      AAAA    ::1\n "
    
    def Resverse_Db_File(self):
        
        return f";\n \
        ; BIND reverse data file for local loopback interface\n \
        ;\n \
        $TTL    604800\n \
        @       IN      SOA     {self.domain}. root.{self.domain}. (\n \
                                    1         ; Serial\n \
                                604800         ; Refresh\n \
                                86400         ; Retry\n \
                                2419200         ; Expire\n \
                                604800 )       ; Negative Cache TTL\n \
        ;\n \
        @       IN      NS      {self.domain}.\n \
        {'\n'.join(self.DB_REVERSE_RECORD)} \
        1.0.0   IN      PTR     localhost.\n"

    def Forward_Zone_file(self):
        return "//forward lookup zone \n\
                zone \"a10.networks.com\" IN { \n\
                type master; \n\
                file \"/etc/bind/db.networks.com\"; \n\
        };\n"
    
    def dbRecord(self, ip, prefix ="www", ns = "A"):
        self.DB_RECORDS.append(f"{prefix}     IN      {ns}       {ip}")

    def reverseDbRecord(self, ip, prefix ="www", ns = "A"):
        self.DB_RECORDS.append(f"{prefix}     IN      {ns}       {ip}")







