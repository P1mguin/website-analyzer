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
    children = get_all_children(root_url)
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
    url = input("What is the full url of the company?\n")
    keywords = get_website_keywords(url)
    for keyword, occurrence in keywords:
        print(f"{keyword}\t{occurrence}")
