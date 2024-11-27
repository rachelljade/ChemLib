# (c) 2024 Rachell Jade Jatulan
# This program is an interactive Chemical and Gene search engine in command prompt.

import json
import time
import random

import requests
from rich import print
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import track
from rich.console import Console


OPTIONS = ["1", "2", "3"]
SKIPLIST = ["_license","undefined_chiral_atom_count","undefined_chiral_bond_count"]

def progress_bar(description, sleep=0.03):
    Console().clear() # this will clear the screen
    for _ in track(range(20), description=description):
        time.sleep(sleep)
    Console().clear()

def main_menu():
    message = "[b][blue]ChemLib[/blue]: Chemical and GeneSet search engine.[/b]"
    print(Panel(message, expand=False))
    
    print("\n[b]MAIN MENU[/b]")
    print("[1] Search Chemical Compound")
    print("[2] Search Human Genes")
    print("[3] Exit")

def search_chemical():
    print("\nChemical Compound Finder")
    cid = input("Enter a PubChem CID (e.g. 962): ").strip()
    URL = f"https://mychem.info/v1/chem/{cid}"

    try:
        response = requests.get(URL)
        dataset = json.loads(response.text)
    except Exception as e:
        print(f"[red]Error:[/red][white]: {e}[/white]")
        return input("\nHit ENTER to return to main menu...")

    results = dataset.get("pubchem", [])
    if len(results) < 1:
        print(f"No results found.")
        return input("\nHit ENTER to return to main menu...")

    selection = results
    if isinstance(results, list):
        selection = results[0]

    for key, value in selection.items():
        if key in SKIPLIST:
            continue
            
        formatted_name = key.replace("_", " ").title()
        if not isinstance(value, dict):
            print(f"{formatted_name}:\t{value}")
            continue

        iupac = list(set(value.values()))
        print(f"{formatted_name}:\t", ", ".join(iupac))

    input("\nHit ENTER to return to main menu...")

def search_human_gene():
    print("\nHuman Gene Finder")
    keyword = input("Enter a keyword (e.g. hair): ").strip()
    
    fields = "taxid,genes.name"
    URL = f" https://mygeneset.info/v1/query/?q={keyword}&fields={fields}&size=5"

    try:
        response = requests.get(URL)
        dataset = json.loads(response.text)
    except Exception as e:
        print(f"[red]Error:[/red][white]: {e}[/white]")
        return input("\nHit ENTER to return to main menu...")

    results = dataset.get("hits", [])

    count = len(results)
    print(f"\nfound {count} results.")
    for result in results:
        trait = result.get("_id")
        print(f"\n{trait}")

        genes = result.get("genes")
        for gene in genes:
            gene_name = gene.get("name", "")
            print(f" - {gene_name}")
        input("\nView next item...")
        
    input("\nHit ENTER to return to main menu...")

def main():
    progress_bar("Loading...")
    while True:
        main_menu()
        selected = Prompt.ask("Select", choices=OPTIONS, show_choices=False)

        if selected == "1":
            search_chemical()
        elif selected == "2":
            search_human_gene()
        elif selected == "3":
            Console().clear()
            print("[red]\nClosing the program... Goodbye!")
            break

        Console().clear()
        
if __name__ == "__main__":
    main()
