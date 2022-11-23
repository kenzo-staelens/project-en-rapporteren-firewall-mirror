## dependencies installeren
```bash
apt install build-essential python-dev-is-python3 libnetfilter-queue-dev
pip install netfilterqueue
pip install scapy
```

## Config
configs moeten moenteel aangepast worden in config.json, als nieuwe config parameters woren toegevoegd
moeten deze in de eerste sectie (aangeduid met #import config) worden toegevoegd en default waarden ingesteld
als config.json niet gevonden wordt

default values
| key | value |
| --- | --- |
|logging | `False` |
|logfile | `None` |

## Logging
logging naar file of print moet ingesteld worden via config.json
| logging | locatie |
| --- | --- |
| True | ingestelde logfile |
| False | print |

momenteel worden logs opgeslaan met pakketstructuur

in/out/fwd source_ip -> destination_ip: L3_protocol L4_Protocol packet_type

( format string: `"{: >3} {: >15} -> {: >15}: {} {} {}` )


## How to run
### opstellen iptables
`sudo ./setiptables`[^1]

stuurt alle opgevangen pakketten door naar nfqueue 1, 2 en 3 respectievelijk voor
de INPUT, OUTPUT en FORWARD chains

[^1]: herstellen van iptables kan met het commando `sudo iptables -F`

### opstarten programma
| Syntax | Achtergrond | Logging types |
| --- | --- | --- |
| `sudo ./firewall.py` | False | print/logfile |
| `sudo ./run` | True | logfile |
| `sudo ./fullreset`[^2] | True | logfile |

**Note**: sudo verplicht bij gebruik van deze commandos

[^2]: stopt automatisch vorige sessie (via uitvoeren killall, zie hierna), reset iptables naar nodige instellingen en voert opnieuw uit in achtergrond

### afsluiten programma
| start commando | kill commando|
| --- | --- |
| firewall.py | ctrl+C |
| run | `sudo ./killall`[^3] |
| fullreset | `sudo ./killall`[^3] |

**Note**: net als bij opstarten is sudo verplicht

[^3]: let op bij uitvoeren killall bij firewall.py implementatie, hierbij kan mogelijks de console waarin je werkt raar doen
