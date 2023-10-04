from IntegerizedStack import *
from Utility import *
from Node import *

def from_int(nt, n, cfg):
    # provide the n'th expansion of nonterminal nt

    # count up the number of terminals
    nterminals = sum([is_terminal_rule(rhs, cfg) for rhs in cfg[nt]])

    # check if n is coding a terminal
    if n < nterminals:
        return Node(nt, cfg[nt][n])
    else:
        # n-nterminals should be an IntegerizedStack where we
        # uppop the children
        i = IntegerizedStack(n - nterminals)

        # how many nonterminal rules
        nnonterminals = len(cfg[nt]) - nterminals

        # i first encodoes which *non*-terminal
        which = i.modpop(nnonterminals)
        #print("#", nt, n, nterminals, nnonterminals, which, cfg[nt])
        rhs = cfg[nt][nterminals+which]

        # count up how many on the rhs are nonterminals
        # and divide i into that many integers
        t = i.split(sum( is_nonterminal(r,cfg) for r in rhs))

        # now we can expand all of the children
        children = []
        for r in rhs:
            if is_nonterminal(r,cfg):
                children.append(from_int(r,t.pop(0), cfg))
            else:
                children.append(Node(r))
        return Node(nt, children)

if __name__ == "__main__":

    ## NOTE: that in cfg, the terminal rules must be ordered first
    # cfg = {
    #     "S": [("o"), ("S", "S")]
    # }
    # cfg = {
    #     "S": [("NP", "VP")],
    #     "NP": [("n",), ("d", "n"), ("d", "AP", "n"), ("NP", "PP")],
    #     "AP": [("a",), ("a", "AP")],
    #     "PP": [("p", "NP"), ],
    #     "VP": [("v",), ("v", "NP"), ("v", "S"), ("VP", "PP")]
    # }
    # cfg = {
    #     "BOOL":   [("<", "NUMBER", "NUMBER"), ("=", "NUMBER", "NUMBER"), ("FORALL", "VAR", "BOOL"), ("NOT", "BOOL"), ("OR", "BOOL", "BOOL")],
    #     "NUMBER": [("0",), ("VAR",), ("S", "NUMBER"), ("+", "NUMBER", "NUMBER"), ("*", "NUMBER", "NUMBER")],
    #     "VAR":    [("x",), ("VAR", "*")]
    # }
    # cfg = {
    #     "S": [("a", "b"), ("a", "S", "b")]
    # }

    cfg = {
        "[4,O,4]": [("[4,O,4]", "ε+"), ("ε+", "[4,O,4]")],
        "[1,L,4]": [("[1,O,3]", "[3,N,4]"), ("ε+", "[1,L,4]"), ("[1,O,4]", "[4,N,4]"), ("[1,O,1]", "[1,N,4]"), ("[1,L,4]", "ε+")],
        "[1,N,1]": [("[1,a,1]", "ε+"), ("[1,N,1]", "[1,N,1]"), ("[1,N,4]", "[4,N,1]"), ("[1,N,1]", "ε+"), ("ε+", "[1,N,1]"), ("ε+", "[1,a,1]"), ("[1,N,3]", "[3,N,1]"), ("a")],
        "START": [("START", "F.ε"), ("[3,N,1]", "[1,L,4]"), ("[1,N,3]", "[3,L,4]"), ("[1,N,4]", "[4,L,4]"), ("[3,N,3]", "[3,L,4]"), ("[1,N,1]", "[1,L,4]"), ("[3,N,4]", "[4,L,4]")],
        "[1,O,3]": [("ε+", "[1,+,3]"), ("[1,+,3]", "ε+"), ("[1,O,3]", "ε+"), ("+"), ("*"), ("ε+", "[1,O,3]")],
        "[3,N,3]": [("[3,N,3]", "[3,N,3]"), ("[3,N,3]", "ε+"), ("ε+", "[3,N,3]"), ("[3,N,4]", "[4,N,3]"), ("[3,N,1]", "[1,N,3]")],
        "[4,N,1]": [("[4,N,3]", "[3,N,1]"), ("ε+", "[4,N,1]"), ("[4,N,1]", "ε+"), ("[4,N,1]", "[1,N,1]"), ("[4,N,4]", "[4,N,1]")],
        "[3,N,4]": [("ε+", "[3,N,4]"), ("[3,N,3]", "[3,N,4]"), ("b"), ("[3,N,1]", "[1,N,4]"), ("[3,N,4]", "ε+"), ("[3,N,4]", "[4,N,4]"), ("ε+", "[3,b,4]"), ("[3,b,4]", "ε+")],
        "[4,+,1]": [("ε+", "[4,+,1]"), ("+"), ("*"), ("[4,+,1]", "ε+")],
        "[4,N,4]": [("[4,b,4]", "ε+"), ("b"), ("[4,N,4]", "ε+"), ("[4,N,1]", "[1,N,4]"), ("[4,N,4]", "[4,N,4]"), ("ε+", "[4,b,4]"), ("[4,N,3]", "[3,N,4]"), ("ε+", "[4,N,4]")],
        "[3,N,1]": [("[3,N,4]", "[4,N,1]"), ("[3,N,1]", "ε+"), ("[3,N,3]", "[3,N,1]"), ("[3,N,1]", "[1,N,1]"), ("ε+", "[3,N,1]")],
        "[1,+,3]": [("[1,+,3]", "ε+"), ("ε+", "[1,+,3]"), ("*"), ("+")],
        "[1,O,4]": [("[1,O,4]", "ε+"), ("ε+", "[1,O,4]")],
        "[3,O,3]": [("ε+", "[3,O,3]"), ("[3,O,3]", "ε+")],
        "[4,b,4]": [("b"), ("[4,b,4]", "ε+"), ("ε+", "[4,b,4]")],
        "[1,N,4]": [("[1,N,4]", "[4,N,4]"), ("[1,N,4]", "ε+"), ("[1,N,1]", "[1,N,4]"), ("[1,N,3]", "[3,N,4]"), ("ε+", "[1,N,4]")],
        "[4,O,3]": [("ε+", "[4,O,3]"), ("[4,O,3]", "ε+")],
        "[3,L,4]": [("[3,O,4]", "[4,N,4]"), ("[3,O,1]", "[1,N,4]"), ("[3,O,3]", "[3,N,4]"), ("[3,L,4]", "ε+"), ("ε+", "[3,L,4]")],
        "ε+": [("ε+", "ε+"), ("ε")],
        "[4,L,4]": [("[4,O,1]", "[1,N,4]"), ("ε+", "[4,L,4]"), ("[4,L,4]", "ε+"), ("[4,O,3]", "[3,N,4]"), ("[4,O,4]", "[4,N,4]")],
        "[4,O,1]": [("+"), ("*"), ("[4,+,1]", "ε+"), ("ε+", "[4,O,1]"), ("[4,O,1]", "ε+"), ("ε+", "[4,+,1]")],
        "[3,O,4]": [("ε+", "[3,O,4]"), ("[3,O,4]", "ε+")],
        "[3,O,1]": [("[3,O,1]", "ε+"), ("ε+", "[3,O,1]")],
        "[1,N,3]": [("[1,N,1]", "[1,N,3]"), ("ε+", "[1,N,3]"), ("[1,N,3]", "[3,N,3]"), ("[1,N,3]", "ε+"), ("[1,N,4]", "[4,N,3]")],
        "F.ε": [("ε")],
        "[3,b,4]": [("b"), ("ε+", "[3,b,4]"), ("[3,b,4]", "ε+")],
        "[4,N,3]": [("[4,N,3]", "[3,N,3]"), ("[4,N,1]", "[1,N,3]"), ("[4,N,3]", "ε+"), ("[4,N,4]", "[4,N,3]"), ("ε+", "[4,N,3]")],
        "[1,a,1]": [("a"), ("[1,a,1]", "ε+"), ("ε+", "[1,a,1]")],
        "[1,O,1]": [("[1,O,1]", "ε+"), ("ε+", "[1,O,1]")],
    }

    unq = set()
    for i in range(10):
        t = from_int("START", i, cfg)

        tstr = str(t)
        assert(tstr not in unq)
        unq.add(tstr)

        print(i, "&", t.terminals(), "\\\\")
        # print(i, t.as_scheme())

