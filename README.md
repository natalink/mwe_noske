## VMWE corpus to NoSkE

This repository includes scripts and other files (registry) to convert corpora with verbal multiword expression annotation [PARSEME data](https://lindat.mff.cuni.cz/repository/xmlui/handle/11372/LRT-2282) into vertical format, so that to make them available via NoSke interface. 


#### Vertical representation 
We decided to experiment first with VMWE represented as attributes. In the previous work by Behrang, MWEs were presented as structures (wrapped in xml tag), yet for the present data this may not be sufficient because of many discontinuous VMWEs. (this option is not excluded though).
The last attributes will be : VMWEtype:head/childtype, e.g. LVC:head, or ID:child. Another attribute is VMWE lemma collected from all components of VMWE separated by underscore:

Input - parsemetsv + respective conllu:

```
# sentence-text: Nous voulons protéger notre droit à avoir des idées, des sentiments, des émotions, contre l'invasion technologique des grands frères, comme nous le lais
se à penser le cas récent d'Échelon, sur lequel cette Assemblée se penchera sous peu.
1       Nous    _       _
2       voulons _       _
3       protéger        _       _
4       notre   _       _
5       droit   _       _
6       à       _       _
7       avoir   _       1:LVC;3:LVC;4:LVC
8       des     _       _
9       idées   nsp     1
10      ,       _       _
11      des     _       _
12      sentiments      nsp     3
13      ,       _       _
14      des     _       _
15      émotions        nsp     4
16      ,       _       _
17      contre  _       _
18      l'      nsp     _
19      invasion        _       _
20      technologique   _       _
21-22   des     _       _
21      de      _       _
22      les     _       _
23      grands  _       _
24      frères  nsp     _
25      ,       _       _
26      comme   _       _
27      nous    _       _
28      le      _       _
29      laisse  _       2:ID
30      à       _       2
31      penser  _       2
32      le      _       _
33      cas     _       _
34      récent  _       _
35      d'      nsp     _
36      Échelon nsp     _
37      ,       _       _
38      sur     _       _
39      lequel  _       _
40      cette   _       _
41      Assemblée       _       _
42      se      _       5:IReflV
43      penchera        _       5
44      sous    _       _
45      peu     nsp     _
46      .       _       _

```

Output: 
```
<s>
Nous    1       il      CL      CLS     n=p|p=1|s=suj|sentid=Europar.550_00191  2       suj     _       _       _       _
voulons 2       vouloir V       V       m=ind|n=p|p=1|t=pst     0       root    _       _       _       _
protéger        3       protéger        V       VINF    m=inf   2       obj     _       _       _       _
notre   4       son     D       DET     n=s|s=poss      5       det     _       _       _       _
droit   5       droit   N       NC      g=m|n=s|s=c     3       obj     _       _       _       _
à       6       à       P       P       _       5       dep     _       _       _       _
avoir   7       avoir   V       VINF    m=inf   6       obj.p   _       _       LVC:head;LVC:head;LVC:head      avoir_idée;avoir_sentiment;avoir_émotion
des     8       un      D       DET     n=p|s=ind       9       det     _       _       _       _
idées   9       idée    N       NC      g=f|n=p|s=c     7       obj     _       _       LVC:child       avoir_idée
,       10      ,       PONCT   PONCT   s=w     7       ponct   _       _       _       _
des     11      un      D       DET     n=p|s=ind       12      det     _       _       _       _
sentiments      12      sentiment       N       NC      g=m|n=p|s=c     7       obj     _       _       LVC:child       avoir_sentiment
,       13      ,       PONCT   PONCT   s=w     7       ponct   _       _       _       _
des     14      un      D       DET     n=p|s=ind       15      det     _       _       _       _
émotions        15      émotion N       NC      g=f|n=p|s=c     7       obj     _       _       LVC:child       avoir_émotion
,       16      ,       PONCT   PONCT   s=w     7       ponct   _       _       _       _
contre  17      contre  P       P       _       7       mod     _       _       _       _
l'      18      le      D       DET     n=s|s=def       19      det     _       _       _       _
invasion        19      invasion        N       NC      g=f|n=s|s=c     17      obj.p   _       _       _       _
technologique   20      technologique   A       ADJ     n=s|s=qual      19      mod     _       _       _       _
des     21-22   _       _       _       _       _       _       _       _       _       _
de      21      de      P       P       _       19      dep     _       _       _       _
les     22      le      D       DET     g=m|n=p|s=def   24      det     _       _       _       _
grands  23      grand   A       ADJ     g=m|n=p|s=qual  24      mod     _       _       _       _
frères  24      frère   N       NC      g=m|n=p|s=c     21      obj.p   _       _       _       _
,       25      ,       PONCT   PONCT   s=w     2       ponct   _       _       _       _
comme   26      comme   C       CS      s=s     2       mod     _       _       _       _
nous    27      le/lui  CL      CLO     n=p|p=1|s=obj   29      a_obj   _       _       _       _
le      28      le      CL      CLO     g=m|n=s|p=3|s=obj       29      obj     _       _       _       _
laisse  29      laisser V       V       m=ind|n=s|p=3|t=pst     26      obj.cpl _       _       ID:head laisser_à_penser
à       30      à       P       P       _       29      a_obj   _       _       ID:child        laisser_à_penser
penser  31      penser  V       VINF    m=inf   30      obj.p   _       _       ID:child        laisser_à_penser
le      32      le      D       DET     g=m|n=s|s=def   33      det     _       _       _       _
cas     33      cas     N       NC      g=m|s=c 29      suj     _       _       _       _
récent  34      récent  A       ADJ     g=m|n=s|s=qual  33      mod     _       _       _       _
d'      35      de      P       P       _       33      dep     _       _       _       _
Échelon 36      Échelon N       NPP     s=p     35      obj.p   _       _       _       _
,       37      ,       PONCT   PONCT   s=w     33      ponct   _       _       _       _
sur     38      sur     P       P       _       43      p_obj   _       _       _       _
lequel  39      lequel  PRO     PROREL  g=m|n=s|s=rel   38      obj.p   _       _       _       _
cette   40      ce      D       DET     g=f|n=s|s=dem   41      det     _       _       _       _
Assemblée       41      assemblée       N       NC      g=f|n=s|s=c     43      suj     _       _       _       _
se      42      le/lui  CL      CLR     p=3|s=refl      43      aff     _       _       IReflV:head     le/lui_pencher
penchera        43      pencher V       V       m=ind|n=s|p=3|t=fut     33      mod.rel _       _       IReflV:child    le/lui_pencher
sous    44      sous    P       P       _       43      mod     _       _       _       _
peu     45      peu     ADV     ADV     _       44      obj.p   _       _       _       _
.       46      .       PONCT   PONCT   s=s     2       ponct   _       _       _       _
</s>

```



