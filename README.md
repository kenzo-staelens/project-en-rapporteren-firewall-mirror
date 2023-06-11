[[_TOC_]]

# Kwaadaardig internetverkeer onderscheppen: een firewall ontwikkeld in Python
Voor dit project wordt er eerst een theoretisch onderzoek gedaan als voorstudie voor het ontwikkelen van een softwarefirewall. De software wordt ontwikkeld in Python. Het project is bedoeld om een beter inzicht te verkrijgen in de werking van malware en een firewall. 

## Werking
De werking van de firewall wordt hieronder geïllustreerd met een block diagram. Wanneer een pakket binnenkomt zal die in een loop terecht komen. Deze loop zal alle modules die tot een bepaalde laag behoren uitvoeren. Binnen een module wordt de relevante data vergeleken met de regels binnen de module. Hier volgt uit of het aan de regels van de module voldoet. Als de regel voldoet kan de firewall het pakket laten vallen of doorlaten. Belangrijk is dat de data tegenover alle regels binnen een module zal getest worden. Als de data volgens de regels niet geblokkeerd hoeft te worden zal het naar de volgende module gestuurd worden om daar hetzelfde proces te doorlopen. Dit tot alle modules doorlopen zijn. Vervolgens zal naar de volgende laag gekeken worden en begint alles weer van in het begin. Pas wanneer alle lagen doorlopen zijn zal het pakket geaccepteerd worden.

![Block Diagram Image](/Documents/Images/Blokdiagram.png)

## Userinterface
De userinterface wordt zodanig ontwikkeld dat deze toegankelijk is voor iedereen. Op de homepagina wordt gekozen voor grote duidelijke knoppen met de meest frequente en belangrijkste gebruikte functionaliteiten. De status van de firewall wordt hier ook getoond. Het geeft aan of er dreigingen gevonden werd en er pakketten werden geblokkeerd. Wanneer er gekozen wordt om hierop te drukken, dan gaat de gebruiker naar de dashboard pagina. Deze kan ook bereikt worden via de dashboard knop zelf. Hier wordt een gedetailleerde weergave van de meldingen getoond. Wanneer men het netwerkverkeer wil bekijken, kan men kiezen om op de traffic knop te drukken. Als de instellingen moeten worden aangepast kan er gekozen worden om op de instellingen knop te drukken. Het Figma ontwerp kan [hier](https://www.figma.com/proto/9cMeBzz5Z4thiJRbWzHK5Y/Firewall?node-id=2-6&starting-point-node-id=2%3A6) teruggevonden worden.

![Userinterface Image](/Documents/Images/Homepagina.png)

## Infrastructuur
### Virtuele machines
De software loopt op een paar virtuele machines. Zo zijn de verschillende machines ook in een netwerk worden geplaatst waar de nodige configuraties in toegepast zijn. Dit wordt hieronder besproken. De besturingssystemen werden als volgt gekozen. Voor de jump host is dat Windows 10. Voor de firewall CentOS 8 en voor de clients Fedora.

### Netwerk
Voor dit project wordt er gekozen voor een gesloten omgeving, zodat er geen gevaar ontstaat voor zelfbesmetting bij het testen met bestaande malware. In de figuur hieronder wordt de opstelling afgebeeld. De virtuele machines met als prefix “Linux” behoren tot de testomgeving. De “jumphost” is nodig om via SSH (secure shell) verbinding te maken met de firewall server. Het verkeer van de twee computers in het netwerk wordt gerouteerd door de firewall server zelf. Zo werkt deze ook als een eenvoudige router. Alle toestellen binnen dit afgesloten netwerk zijn via SSH-gateway bereikbaar vanop de jump-host. 

![Userinterface Image](/Documents/Images/Netwerk.png)

# Handleiding
## dependencies installeren
```bash
apt install build-essential python-dev-is-python3 libnetfilter-queue-dev
pip install netfilterqueue
pip install scapy
```

## forwarding aanzetten op linux machine
```bash
echo 1 >/proc/sys/net/ipv4/ip_forward
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

# Credits
## Auteurs
- Kenzo Staelens
- Jonathan van Caloen
- Jonas Van den Berghe
- Michaël Vasseur

## Mentors
- Tom Cordemans
- Sabine Martens