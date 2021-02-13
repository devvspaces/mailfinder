import dnspython as dns
import dns.resolver

result = dns.resolver.resolve('tutorialspoint.com', 'A')
for ipval in result:
    print('IP', ipval.to_text())

result = dns.resolver.resolve('mail.google.com', 'CNAME')
for cnameval in result:
    print (' cname target address:', cnameval.target)

result = dns.resolver.resolve('mail.blevins.org', 'MX')
for exdata in result:
    print (' MX Record:', exdata.exchange.text())