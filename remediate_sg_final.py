
import boto.ec2
conn = boto.ec2.connect_to_region("us-east-1")
groups = conn.get_all_security_groups()

for group in groups:
        ip_protocol='tcp'
        from_rdp_port='3389'
        to_rdp_port='3389'
        cidr_ip='0.0.0.0/0'
        your_ip='x.x.x.x/32' #place your ip
        from_ssh_port='22'
        to_ssh_port='22'

            for rule in group.rules:
                if rule.ip_protocol == ip_protocol:
                    if rule.from_port == from_rdp_port:
                        if rule.to_port == to_rdp_port:
                            for grant in rule.grants:
                                if grant.cidr_ip == cidr_ip:
                                    print (group.name, rule, grant.cidr_ip, group.id, grant.owner_id, 'allows RDP access from the entire internet! Correcting...' )
                                        try:
                                            group.authorize(ip_protocol, from_rdp_port, to_rdp_port, brm_ip)
                                            group.revoke(ip_protocol, from_rdp_port, to_rdp_port, your_ip)
                                        except:
                                            print ("Failed on", group.name)
                else:
                    if rule.from_port == from_ssh_port:
                        if rule.to_port == to_ssh_port:
                            for grant in rule.grants:
                                if grant.cidr_ip == cidr_ip:
                                    print (group.name, rule, grant.cidr_ip, group.id, grant.owner_id, 'allows SSH access from the entire internet! Correcting...' )
                                        try:
                                            group.authorize(ip_protocol, from_ssh_port, to_ssh_port, your_ip)
                                            group.revoke(ip_protocol, from_ssh_port, to_ssh_port, cidr_ip)
                                        except:
                                            print ("Failed on", group.name)
            