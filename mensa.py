import sys
import requests
import click
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from datetime import datetime

@click.command()
@click.option("--date", default=datetime.now().strftime("%Y-%m-%d"), help="Date in ISO format")
@click.option("--mensa", default="hsma", help="The mensa you want to look at")
def menu(date, mensa):
    """Gets the Mensa Menu from a specified day"""
    console = Console()

    match mensa:
        case "hsma":
            URL =  "https://www.stw-ma.de/Essen+_+Trinken/Speisepl%C3%A4ne/Hochschule+Mannheim.html"
        case "schloss":
            URL = "https://www.stw-ma.de/men%C3%BCplan_schlossmensa.html"
        case "greenes":
            URL = "https://www.stw-ma.de/Essen+_+Trinken/Speisepl%C3%A4ne/greenes%C2%B2.html"
        case "mensawagon":
            URL = "https://www.stw-ma.de/Essen+_+Trinken/Speisepl%C3%A4ne/MensaWagon.html"
        case "musik":
            URL = "https://www.stw-ma.de/Essen+_+Trinken/Speisepl%C3%A4ne/Cafeteria+Musikhochschule.html"
        case "metropol":
            URL = "https://www.stw-ma.de/Essen+_+Trinken/Speisepl%C3%A4ne/Mensaria+Metropol.html"
        case "wohlgelegen":
            URL = "https://www.stw-ma.de/Essen+_+Trinken/Speisepl%C3%A4ne/Mensaria+Wohlgelegen.html"
        case "dhbw":
            URL = "https://www.stw-ma.de/Essen+_+Trinken/Speisepl%C3%A4ne/Speisenausgabe+DHBW+Eppelheim.html"
        case _:
            URL = "https://www.stw-ma.de/Essen+_+Trinken/Speisepl%C3%A4ne/Hochschule+Mannheim.html"
            

    data = {"day":date}
    page = requests.post(URL, data)
    if page.status_code != 200:
        console.print(Panel("[bold red]:warning: Something went wrong trying to fetch the website[/bold red]"))
        sys.exit()
        
    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find("h1", class_="maintitle").text.strip()

    console.print(Markdown("# Speiseplan " + title))
    
    menu = soup.find_all("table", class_="speiseplan-table")

    if len(menu) == 0:
        console.print(Panel("[bold dark_orange]:warning: Heute gibt es nichts.[/bold dark_orange]"))
        sys.exit()

    
    table = Table(show_header=True, show_lines=True, header_style="dark_orange")

    table.add_column("Kategorie")
    table.add_column("Gericht")
    table.add_column("Preis")

    for t in menu:
        rows = t.find_all("tr")
        for row in rows:
            kategorie = row.find("td", class_="speiseplan-table-menu-headline").text.strip()
            inhalt = row.find("td", class_="speiseplan-table-menu-content").text.strip().replace("(","[dim]").replace(")","[/dim]")
            preis = row.find("i", class_="price").text.strip()
            einheit = row.find("i", class_="customSelection").text.strip()
            table.add_row(
                "[bold]" + kategorie + "[/bold]",
                inhalt,
                preis + " [dim]" + einheit + "[/dim]",
            )
    console.print(table)
    console.print(f"[dim]{URL}[/dim]")

if __name__ == "__main__":
    menu()