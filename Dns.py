import os 
import subprocess
import time 


# conf 1 zone at a time
class BindSetup():

    def __init__(self, zone = "a10.networks.com", ip = "30.30.20.10", record = ["www    IN  A   127.0.0.1"], revRecord = []) -> None:

        self.zone= zone
        self.IP_ADDRESS=ip
        self.prefix = "www"
        self.DB_RECORDS = record
        self.DB_REVERSE_RECORD = revRecord

    def init(self, fw_record = [], rev_record = []):
        try:
            subprocess.run(["sudo", "apt", "install", "bind9"])
            time.sleep(10)
            os.chdir("../")
            os.chdir("/etc/bind")
            print(os.getcwd())
        except FileNotFoundError:
            print(f"Error : FileNotFound ")
        except Exception as e:
            print(f"Error: {str(e)}")

        if(True or "/etc/bind" in os.getcwd() ):
            print(">copying original files...")
            # subprocess.run(["sudo", "cp", "named.conf.options", "named.conf.options.orig"])
            # subprocess.run(["sudo", "cp", "named.conf.local", "named.conf.local.orig"])

            with open("db."+self.zone, "w") as file:
                file.write(self.Forward_Db_File())

            with open("named.conf.local", "a") as file:
                file.write(self.Forward_Zone_file())

            # fetch content of named.config.options
            content =[]
            with open("named.conf.options", "r") as file:
                lines = file.readlines()
                for x in range(len(lines)-1, 0, -1):
                    content = lines[0:x]
                    if "recursion" in lines[x]:
                        break
            # named.config.options        
            with open("named.conf.options", "w") as file:
                file.write(' '.join(content) + self.NamedOptions()+"\n }")
            
            # revers query
            with open("db."+self.IP_ADDRESS, "w") as file:
                file.write(self.Resverse_Db_File())

            self.checkConfig()

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

        return ''';
        ; BIND reverse data file for local loopback interface
        ;
        $TTL    604800
        @       IN      SOA     {zone}. root.{zone}. (
                                    1         ; Serial
                                604800         ; Refresh
                                86400         ; Retry
                                2419200         ; Expire
                                604800 )       ; Negative Cache TTL
        ;
        @       IN      NS      {zone}.
        {records} 
        1.0.0   IN      PTR     localhost.
        '''.format(zone='.'.join(self.zone.split('.')[:-1]), records='\n'.join(self.DB_REVERSE_RECORD))

    def Forward_Zone_file(self):
        return '''//forward lookup zone
                zone \\"''' + self.zone +''' \\ IN {
                type master; 
                file \\"/etc/bind/db.ip\\";
        };\n'''
    
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

    def checkConfig(self):

        subprocess.run(["named-checkconf"])
        subprocess.run(["named-checkzone", f"{self.zone}",  f"db.{self.zone}"])
        #named-checkzone 40.40.40.in-addr.arpa db.40.40.40
