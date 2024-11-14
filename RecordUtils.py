def createRecords(args):
    filterArgs(args)
    return [ f"{args.domain[x]}\tIN\t{args.ns[x]}\t{args.ipaddress[x]}" for x in range(0, len(args.domain))]


def filterArgs(args):
    if len(args.ns)< len(args.domain):
        for x in range(len(args.ns), len(args.domain)):
            args.ns.append("A")

    if len(args.ipaddress)< len(args.domain):
        l = len(args.ipaddress)
        for x in range(l, len(args.domain)):
            args.ipaddress.append(args.ipaddress[l-1])

def createRevRecords(args):
    filterArgs(args)
    return[ f"{args.ipaddress[x].split(".")[-1]}\tIN\tPTR\t{args.domain[x]+args.zone}" for x in range(0, len(args.domain))]


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--domain', type=str, nargs='+', help="Domain")
    parser.add_argument('-ip', '--ipaddress', type=str, nargs='+', help="IP Address")
    parser.add_argument('-ns', '--ns', type=str, nargs='*', help="IP Address")
    parser.add_argument('-z', '--zone', type=str, help="zone")

    args = parser.parse_args() 
    
    