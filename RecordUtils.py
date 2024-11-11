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

   
if __name__ == "__main__": 

    # print(args.domain)
    # print(args.ipaddress)
    # print(args.ns) 
    # print(createRecords(args=None))
    pass
    