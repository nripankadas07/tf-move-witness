"""Offline bounded tf-move-witness analyzer. No operational writes."""

import re,json
NAME=r'[A-Za-z_][A-Za-z0-9_-]*'
INDEX=r'(?:\[(?:0|[1-9][0-9]*|"(?:[^"\\\x00-\x1f]|\\["\\/bfnrt]|\\u[0-9a-fA-F]{4})*")\])?'
ADDR=re.compile(r'(?P<modules>(?:module\.'+NAME+INDEX+r'\.)*)(?P<type>'+NAME+r')\.(?P<name>'+NAME+r')(?P<index>'+INDEX+r')\Z')

def address(s):
    if not isinstance(s,str) or len(s)>1024:raise ValueError('invalid address')
    m=ADDR.fullmatch(s)
    if not m or m['type'] in ('module','data'):raise ValueError('only managed resource addresses; explicit instances required')
    for key in re.findall(r'\[("(?:[^"\\]|\\.)*")\]',s):
        if json.dumps(json.loads(key),ensure_ascii=False)!=key:raise ValueError('instance key must use canonical JSON quoting')
    return s,m['type'],s[:len(s)-len(m['index'])] if m['index'] else s,bool(m['index'])

def analyze(d):
    if not isinstance(d,dict) or set(d)!={'state','moves'}:raise ValueError('expected state address list and moves')
    state=d['state'];moves=d['moves']
    if not isinstance(state,list) or len(state)>1000 or not isinstance(moves,list) or len(moves)>256:raise ValueError('state <=1000; moves <=256')
    if any(not isinstance(x,str) for x in state) or len(set(state))!=len(state):raise ValueError('state must contain unique address strings')
    states={address(x)[0]:address(x) for x in state};mapping={};types={}
    for item in moves:
        if not isinstance(item,dict) or set(item)!={'from','to'}:raise ValueError('expected from/to')
        a=address(item['from']);b=address(item['to'])
        if a[1]!=b[1]:raise ValueError('cross-type moves require provider validation and are unsupported')
        if a[0] in mapping or a[0]==b[0]:raise ValueError('duplicate source or self move')
        if not a[3] and any(s[2]==a[2] and s[3] for s in states.values()):raise ValueError('whole-resource move over indexed state unsupported; enumerate instances')
        mapping[a[0]]=b[0];types[a[0]]=a
    chains={}
    for a in mapping:
        chain=[a];seen={a}
        while chain[-1] in mapping:
            nxt=mapping[chain[-1]]
            if nxt in seen:raise ValueError('cyclic moved declarations')
            seen.add(nxt);chain.append(nxt)
        chains[a]=chain
    proposed=[];destinations={}
    for original in sorted(states):
        chain=chains.get(original,[original]);dest=chain[-1]
        if dest in destinations:raise ValueError('destination collision: '+dest)
        # Occupied intermediate addresses represent distinct objects, not a single chain.
        if any(x in states for x in chain[1:]):raise ValueError('move chain intersects occupied state: '+original)
        destinations[dest]=original
        proposed.append({'from':original,'to':dest,'chain':chain,'changed':len(chain)>1})
    return {'proposed':proposed,'unused_sources':sorted(set(mapping)-set(states)),
            'result_addresses':sorted(destinations),'state_written':False,'provider_validated':False}

def _pairs(pairs):
    result={}
    for key,val in pairs:
        if key in result:raise ValueError('duplicate JSON key: '+key)
        result[key]=val
    return result

def main():
    import argparse,json,sys
    from pathlib import Path
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',help='JSON input path; - for stdin')
    args=parser.parse_args()
    try:
        raw=sys.stdin.buffer.read(1048577) if args.input=='-' else Path(args.input).open('rb').read(1048577)
        if len(raw)>1048576:raise ValueError('input exceeds 1 MiB')
        data=json.loads(raw,object_pairs_hook=_pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite JSON number')))
        print(json.dumps(analyze(data),ensure_ascii=True,indent=2));return 0
    except (ValueError,TypeError,KeyError,OverflowError,RecursionError,OSError) as exc:
        print(json.dumps({'error':str(exc)}),file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
