import pywikibot
import re

class functions: 
    def search(self,input):
        aux = input.split(":")
        aux2 = aux[1].replace("]", "")

        site = pywikibot.Site("wikidata", "wikidata")
        repo = site.data_repository()
        item = pywikibot.ItemPage(repo, aux2)

        item_dict = item.get()  # Get the item dictionary
        output = str(item_dict["labels"]["en"])
        return output