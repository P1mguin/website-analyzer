from typing import Set

import requests
from bs4 import BeautifulSoup


def get_children(root_url, url):
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    children = set()
    for child in soup.find_all('a'):
        child_url = child.get('href')
        if not child_url:
            continue

        if child_url.startswith(root_url):
            children.add(child_url)
        elif child_url.startswith('/'):
            children.add(f"{root_url}{child_url[1:]}")

    # Now remove the link itself from the children
    if url in children:
        children.remove(url)
    return list(children)


def get_link_table(root_url: str, this_url="", explored_links=set()):
    if not this_url:
        this_url = root_url
    print(this_url)

    # Maintain a map of the urls and which children they have
    link_map = {
        this_url: []
    }

    # The recursion is over when all links in the link_map have been explored
    if all([link in explored_links for link in link_map.keys()]):
        return link_map, explored_links

    # Set this link as explored in the set
    explored_links.add(this_url)

    # Get the children of the current_link and get the link table for those children
    children = get_children(root_url, this_url)
    link_map[this_url] = children
    for child in children:
        child_link_map, child_explored_links = get_link_table(root_url, child, explored_links)

        # Merge the link_map and the explored links
        explored_links = explored_links.union(child_explored_links)
        link_map.update(child_link_map)

    return link_map, explored_links


def get_all_children(url):
    children_table, _ = get_link_table(url)
    all_children = set()
    for children in children_table.values():
        for child in children:
            all_children.add(child)

    return list(all_children)


def get_keywords(url):
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    text = soup.text
    words = text.split()
    word_occurrence = {}
    for word in words:
        term = word.capitalize()
        if term not in word_occurrence:
            word_occurrence[term] = 0
        word_occurrence[term] += 1
    return word_occurrence


def get_website_keywords(root_url):
    # children = get_all_children(root_url)
    children = ['https://connectium.nl/cloud/spamfilter', 'https://connectium.nl/klantcases/haase-bouw', 'https://connectium.nl/', 'https://connectium.nl/glasvezelactie-enter#prijzenglasvezel', 'https://connectium.nl/inloggen', 'https://connectium.nl/blog/oorzaken-dataverlies', 'https://connectium.nl/blog/cloud-vs-on-premise-kosten', 'https://connectium.nl/cloud/hosting-domeinen', 'https://connectium.nl/blog/voordelen-voip-telefonie', 'https://connectium.nl/blog/voordelen-microsoft-365#productief', 'https://connectium.nl/klantcases/cantique', 'https://connectium.nl/cloud/werkplek-in-de-cloud', 'https://connectium.nl/klantcases/de-sterkerij', 'https://connectium.nl/uncategorised/klantcases', 'https://connectium.nl/klantcases', 'https://connectium.nl/it-beheer/werkplekbeheer', 'https://connectium.nl/blog/hoe-veilig-is-werken-in-de-cloud', 'https://connectium.nl/4g-back-up-internet', 'https://connectium.nl/klantcases/mensink-schoonmaak', 'https://connectium.nl/klantcases/de-jong-betonvloeren', 'https://connectium.nl/ict-oplossingen-voor-het-mkb', 'https://connectium.nl/blog/de-gratis-klassieke-teams-versie-verdwijnt-wat-te-doen', 'https://connectium.nl/klantcases/klanten-in-het-centrum-van-rijssen', 'https://connectium.nl/demo-cloud', 'https://connectium.nl/blog/voordelen-microsoft-365#teams', 'https://connectium.nl/blog/voordelen-microsoft-365#functionaliteiten', 'https://connectium.nl/blog/waarom-ict-beheer-uitbesteden', 'https://connectium.nl/blog/waarom-is-een-online-back-up-zakelijk-nodig', 'https://connectium.nl/blog/voordelen-microsoft-365#apparaat', 'https://connectium.nl/blog/voordelen-microsoft-365', 'https://connectium.nl/factsheet-security-awareness', 'https://connectium.nl/blog/waarom-microsoft365-back-up-maken', 'https://connectium.nl/blog/flexibiliteit-is-key-in-een-hybride-werkomgeving', 'https://connectium.nl/blog/zo-wordt-digitaal-werken-een-succes', 'https://connectium.nl/blog/ict-trends-en-ontwikkelingen', 'https://connectium.nl/cloud', 'https://connectium.nl/klantcases/kippers-rijssen', 'https://connectium.nl/camerabeveiliging/indoorbeveiliging', 'https://connectium.nl/blog/in-6-stappen-migreren-naar-de-cloud', 'https://connectium.nl/contact/over-connectium', 'https://connectium.nl/blog/voordelen-microsoft-365#vertrouwd', 'https://connectium.nl/camerabeveiliging', 'https://connectium.nl/ict-bedrijf-almelo#reviews', 'https://connectium.nl/klantcases/povag', 'https://connectium.nl/it-beheer/monitoring', 'https://connectium.nl/klantcases/van-buuren-groep', 'https://connectium.nl/klantcases/akor', 'https://connectium.nl/cloud/microsoft-365', 'https://connectium.nl/zakelijk-glasvezel-aanleggen', 'https://connectium.nl/blog/hybride-werken-faciliteren', 'https://connectium.nl/klantcases/owk-ramen-deuren', 'https://connectium.nl/klantcases/ahorn-bouwsystemen', 'https://connectium.nl/blog/wat-is-werken-in-de-cloud', 'https://connectium.nl/glasvezelactie-enschede#prijzenglasvezel', 'https://connectium.nl/blog/it-infrastructuur-de-definitie-essentie-en-voorbeelden', 'https://connectium.nl/cloud/online-back-up', 'https://connectium.nl/blog/kan-ik-mijn-eigen-software-gebruiken-in-de-cloud', 'https://connectium.nl/klantcases/rijssens-museum', 'https://connectium.nl/blog/ict-redundantie-cruciaal-voor-het-bedrijfsleven', 'https://connectium.nl/contact', 'https://connectium.nl/camerabeveiliging/terreinbeveiliging', 'https://connectium.nl/klantcases/solitas', 'https://connectium.nl/cloud/voip-telefonie', 'https://connectium.nl/blog/zonder-gedoe-wisselen-van-it-partner', 'https://connectium.nl/blog/voordelen-microsoft-365#teamverband', 'https://connectium.nl/it-beheer', 'https://connectium.nl/privacy-verklaring', 'https://connectium.nl/images/2021-algemene-voorwaarden-connectium-bv-verwerkingpersoonsgegevens.pdf', 'https://connectium.nl/klantcases/autobedrijf-de-haar', 'https://connectium.nl/camerabeveiliging/bouwplaatsbeveiliging', 'https://connectium.nl/blog/voordelen-microsoft-365#goedkoper', 'https://connectium.nl/zakelijk-glasvezel-aanvragen', 'https://connectium.nl/it-beheer/security', 'https://connectium.nl/blog/voordelen-microsoft-365#gebruikers', 'https://connectium.nl/sitemap', 'https://connectium.nl/security-awareness', 'https://connectium.nl/online-werkplek', 'https://connectium.nl/blog/flexibiliteit-is-key-in-een-hybride-werkomgeving#handleiding', 'https://connectium.nl/blog/wat-digitalisering-voor-jouw-bedrijf-kan-betekenen', 'https://connectium.nl/zakelijk-internet', 'https://connectium.nl/blog/makkelijk-thuiswerken-met-een-cloud-thuiswerkplek', 'https://connectium.nl/klantcases/schulp-vruchtensappen', 'https://connectium.nl/ebook-werkplekindecloud', 'https://connectium.nl/klantcases/constructiebedrijf-htb', 'https://connectium.nl/blog/waarom-multifactorauthenticatie-zo-belangrijk-is-bedrijven', 'https://connectium.nl/blog/het-belang-van-it-voor-jouw-bedrijf', 'https://connectium.nl/blog/voordelen-microsoft-365#updates', 'https://connectium.nl/blog/werken-in-de-cloud-wat-zijn-de-voordelen', 'https://connectium.nl/blog/de-voordelen-van-kantoorautomatisering', 'https://connectium.nl/blog/waarom-preventief-it-onderhoud-zo-belangrijk-is', 'https://connectium.nl/it-beheer/hard-en-software', 'https://connectium.nl/blog', 'https://connectium.nl/blog/bescherm-je-organisatie-tegen-phishing-e-mails', 'https://connectium.nl/it-beheer/zakelijk-glasvezel', 'https://connectium.nl/blog/voordelen-microsoft-365#internet', 'https://connectium.nl/camerabeveiliging/winkelbeveiliging', 'https://connectium.nl/klantcases/troost-hoveniers', 'https://connectium.nl/it-beheer/netwerken', 'https://connectium.nl/cloud/hosted-exchange', 'https://connectium.nl/blog/digitale-werkplek-inrichten', 'https://connectium.nl/it-beheer/serverbeheer', 'https://connectium.nl/blog/voordelen-microsoft-365#samenwerken', 'https://connectium.nl/klantcases/synwood', 'https://connectium.nl/blog/de-moderne-werkplek-veilig-samen-werken-in-de-cloud', 'https://connectium.nl/blog/wat-is-voip-telefonie-en-hoe-werkt-het', 'https://connectium.nl/klantcases/weshold', 'https://connectium.nl/blog/bedrijfsnetwerk-aanleggen-hier-moet-je-op-letten', 'https://connectium.nl/cloud/colocatie', 'https://connectium.nl/blog/een-eigen-server-of-cloud', 'https://connectium.nl/it-beheer/narrowcasting', 'https://connectium.nl/blog/mobiel-werken-wat-is-het-en-wat-zijn-de-voordelen', 'https://connectium.nl/glasvezelactie-losser#prijzenglasvezel', 'https://connectium.nl/blog/wat-betekent-webhosting-en-domeinnaam', 'https://connectium.nl/blog/wereld-back-up-dag-bescherm-jouw-data', 'https://connectium.nl/klantcases/metalin-steel-creators', 'https://connectium.nl/demo-aanvragen-security-awareness-platform', 'https://connectium.nl/blog/voordelen-microsoft-365#veiligcloud']
    word_occurrence = {}
    for child in children:
        print(child)
        child_word_occurrence = get_keywords(child)
        for word, count in child_word_occurrence.items():
            if word not in word_occurrence:
                word_occurrence[word] = 0
            word_occurrence[word] += count

    # Sort the occurrence
    return sorted(word_occurrence.items(), key=lambda x: x[1])


if __name__ == '__main__':
    # url = input("What is the full url of the company?\n")
    url = "https://connectium.nl/"
    keywords = get_website_keywords(url)
    for keyword, occurrence in keywords:
        print(f"{keyword}\t{occurrence}")
