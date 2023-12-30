from trueskill import Rating, rate_1vs1
import json

class Entry:
    def __init__(self, code: str, name1: str, name2: str):
        self.code = code
        self.name1 = name1
        self.name2 = name2
        self.rating = Rating()
        self.ranking = 0.0
        self.round_count = 0

def findEntry(entries : list[Entry], name1 : str, name2 : str):
    matches = list(filter(lambda e: (e.name1 == name1 or e.name2 == name1) and (e.name1 == name2 or e.name2 == name2), entries))
    if (len(matches) > 0):
        return matches[0]
    else:
        return None

def getData(entries, filename):
    f = open(filename)
    tourn = json.load(f)

    for category in tourn["categories"]:
        for event in category["events"]:
            if event["name"] == "Open" or event["name"] == "Shirley" or event["name"] == "Round Robin" or event["name"] == "Varsity NDT/CEDA" or event["name"] == "Open Policy" or event["name"] == "Run for the Roses":
                for round in event["rounds"]:
                    try:
                        for section in round["sections"]:
                            entry1, entry2 = None, None
                            entry1win, entry2win = False, False

                            for ballot in section["ballots"]:
                                code = ballot["entry_code"]
                                names = ballot["entry_name"].split(" & ")

                                if entry1 == None:
                                    match = findEntry(entries, names[0], names[1]) 
                                    entry1 = match if match != None else Entry(code, names[0], names[1])
                                    if match == None:
                                        entries.append(entry1)
                                    
                                    try:
                                        for score in ballot["scores"]:
                                            if score["tag"] == "winloss":
                                                entry1win = score["value"] == 1
                                    except:
                                        continue
                                else:
                                    match = findEntry(entries, names[0], names[1]) 
                                    entry2 = match if match != None else Entry(code, names[0], names[1])
                                    if match == None:
                                        entries.append(entry2)
                                    
                                    try:
                                        for score in ballot["scores"]:
                                            if score["tag"] == "winloss":
                                                entry2win = score["value"] == 1
                                    except:
                                        continue
                                
                            if entry1 == None or entry2 == None:
                                continue

                            if entry1win:
                                entry1.rating, entry2.rating = rate_1vs1(entry1.rating, entry2.rating)
                            elif entry2win:
                                entry2.rating, entry1.rating = rate_1vs1(entry2.rating, entry1.rating)
                            
                            entry1.round_count += 1
                            entry2.round_count += 1
                    except:
                        continue
                
                print(f"Finished {filename}")

def main():
    entries = []
    tourns = [
        "NU 23.json", 
        "GMU 23.json", 
        "Missouri State 23.json",
        "Bing 23.json",
        "SWC 23.json",
        "UK 23.json", 
        "Weber RR 23.json",
        "Weber 23.json",
        "Houston 23.json",
        "West Point 23.json",
        "Wayne 23.json",
        "CSUN 23.json",
        "Harvard 23.json", 
        "UCO 23.json",
        "Wake 23.json",
        "Monmouth 23.json",
        "BTO 23.json"
    ]

    for tourn in tourns:
        getData(entries, tourn)
    
    for entry in entries:
        if entry.round_count < 20:
            continue

        entry.ranking = entry.rating.mu - (3 * entry.rating.sigma)
    
    entries.sort(key=lambda e: e.ranking, reverse=True)

    num = 1
    for entry in entries:
        print(f"{num}\t{entry.name1} & {entry.name2} : {round(entry.ranking, 2)} : {round(entry.rating.mu, 2)} : {round(entry.rating.sigma, 2)}")
        num += 1
                        
if __name__ == "__main__":
    main()   