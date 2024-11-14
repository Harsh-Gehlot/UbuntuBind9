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
            os.chdir("../etc/bind")
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

            with open("db."+self.zone, "w") as file:
                file.write(self.Forward_Db_File())

            with open("named.conf.local", "a") as file:
                file.write(self.Forward_Zone_file())

            with open("named.conf.options", "a+") as file:
                content = file.readlines()
                print(content)
               print( "\n \n \n", self.NamedOptions())
        #     with open("db.domain", "w") as file:
        #         self.dbRecord(ip="40.40.40.100")
        #         self.dbRecord(ip="40.40.40.101")
        #         file.write(createDBLocal())
          
    # def Forward_Db_File(self):

    #     return f"$TTL    604800 \n \
    #         @       IN      SOA     ns1.{self.zone}. root.{self.zone}. (\n \
    #                                 2         ; Serial\n \
    #                             604800         ; Refresh\n \
    #                             86400         ; Retry\n \
    #                             2419200         ; Expire\n \
    #                             604800 )       ; Negative Cache TTL\n \
    #     ;\n \
    #     @       IN      NS      ns1.{self.zone}.\n \
    #     {'\n'.join(self.DB_RECORDS)} \n\
    #     @       IN      AAAA    ::1\n "

    def Forward_Db_File(self):
        return '''$TTL    604800
            @       IN      SOA     ns1.{zone}. root.{zone}. (
                                        2         ; Serial
                                    604800         ; Refresh
                                    86400         ; Retry
                                    2419200         ; Expire
                                    604800 )       ; Negative Cache TTL
            ;
            @       IN      NS      ns1.{zone}.
            {records}
            @       IN      AAAA    ::1
            '''.format(zone=self.zone, records='\n'.join(self.DB_RECORDS))

    
    def Resverse_Db_File(self):

        return '''; \n
        ; BIND reverse data file for local loopback interface \n
        ;\n
        $TTL    604800\n 
        @       IN      SOA     {zone}. root.{zone}. (\n 
                                    1         ; Serial\n 
                                604800         ; Refresh\n 
                                86400         ; Retry\n 
                                2419200         ; Expire\n 
                                604800 )       ; Negative Cache TTL\n 
        ;\n \
        @       IN      NS      {zone}.\n 
        {records} \
        1.0.0   IN      PTR     localhost.\n
        '''.format(zone=self.zone, records='\n'.join(self.DB_REVERSE_RECORD))

    def Forward_Zone_file(self):
        return '''//forward lookup zone \n
                zone \"{zone}\" IN { \n
                type master; \n
                file \"/etc/bind/db.ip\"; \n\
        };\n'''.format(zone=self.zone)
    
    def NamedOptions(self):
        return '''recursion yes;
        listen-on {''' + self.IP_ADDRESS + '''; };
        allow-transfer { none; };
        forwarders {
        8.8.8.8;
        };'''

    def dbRecord(self, ip, prefix ="www", ns = "A"):
        self.DB_RECORDS.append(f"{prefix}     IN      {ns}       {ip}")

    def reverseDbRecord(self, ip, prefix ="www", ns = "A"):
        self.DB_RECORDS.append(f"{prefix}     IN      {ns}       {ip}")







