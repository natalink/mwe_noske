## VMWE corpus to NoSkE

This repository includes scripts and other files (registry) to convert corpora with verbal multiword expression annotation [PARSEME data](https://lindat.mff.cuni.cz/repository/xmlui/handle/11372/LRT-2282) into vertical format, so that to make them available via NoSke and KonText interfaces. 
The PARSEME data can be thus viewed on two different platforms:

- KonText, moderated by Ansa: http://lindat.mff.cuni.cz/services/kontext/corpora/corplist , alternative [github page](https://github.com/ufal/lindat-corpora-conversions/tree/master/data/vertical/parseme) for KonText-related scripts
- NoSke installation by Behrang: http://corpora.phil.hhu.de/parseme

The manual pages for CQL queries:

- [Manual](https://ufal.mff.cuni.cz/lindat-kontext/parseme-mwe) especially devoted to PARSEME data in KonText, to be filled with new examples
- [CQL for Sketch Engine](https://www.sketchengine.co.uk/documentation/corpus-querying/)
- KonText [query manual](https://wiki.korpus.cz/doku.php/en:kurz:uvod), [interface manual](https://wiki.korpus.cz/doku.php/en:manualy:kontext:index) (both by the Czech National Corpus team)
- For those not familiar with KonText/NoSke interface - quick intro, [some screenshots](https://ufal.mff.cuni.cz/lindat-kontext)




#### Vertical representation 
We decided to experiment first with VMWE represented as attributes. In the previous work by Behrang, MWEs were presented as structures (wrapped in xml tag), yet for the present data this may not be sufficient because of many discontinuous VMWEs. (this option is not excluded though).
The last attributes represent MWE:

- mwe (MWE type, e.g. LVC, ID)
- mwe_order. First we opted for head/child option, but since it does not reflect the dependency, just the order, we decided to mark it first/cont, see [#7](https://github.com/natalink/mwe_noske/issues/7) for discussion
- mwe_id (id of MWE in a sentence)
- mwe lemma - concatenation of lemmas, see also [#6](https://github.com/natalink/mwe_noske/issues/6) why this attribute



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
After a long discussion (see issues) we came up with this (not already final) format
Output: 
```
<s>
Nous    il      1       CL      CLS     n=p|p=1|s=suj|sentid=Europar.550_00191  2       suj     _       _       _       _       _       _
voulons vouloir 2       V       V       m=ind|n=p|p=1|t=pst     0       root    _       _       _       _       _       _
protéger        protéger        3       V       VINF    m=inf   2       obj     _       _       _       _       _       _
notre   son     4       D       DET     n=s|s=poss      5       det     _       _       _       _       _       _
droit   droit   5       N       NC      g=m|n=s|s=c     3       obj     _       _       _       _       _       _
à       à       6       P       P       _       5       dep     _       _       _       _       _       _
avoir   avoir   7       V       VINF    m=inf   6       obj.p   _       _       LVC;LVC;LVC     head;head;head  1;3;4   avoir idée;avoir sentiment;avoir émotion
des     un      8       D       DET     n=p|s=ind       9       det     _       _       _       _       _       _
idées   idée    9       N       NC      g=f|n=p|s=c     7       obj     _       _       LVC     child   1       avoir idée
,       ,       10      PONCT   PONCT   s=w     7       ponct   _       _       _       _       _       _
des     un      11      D       DET     n=p|s=ind       12      det     _       _       _       _       _       _
sentiments      sentiment       12      N       NC      g=m|n=p|s=c     7       obj     _       _       LVC     child   3       avoir sentiment
,       ,       13      PONCT   PONCT   s=w     7       ponct   _       _       _       _       _       _
des     un      14      D       DET     n=p|s=ind       15      det     _       _       _       _       _       _
émotions        émotion 15      N       NC      g=f|n=p|s=c     7       obj     _       _       LVC     child   4       avoir émotion
,       ,       16      PONCT   PONCT   s=w     7       ponct   _       _       _       _       _       _
contre  contre  17      P       P       _       7       mod     _       _       _       _       _       _
l'      le      18      D       DET     n=s|s=def       19      det     _       _       _       _       _       _
invasion        invasion        19      N       NC      g=f|n=s|s=c     17      obj.p   _       _       _       _       _       _
technologique   technologique   20      A       ADJ     n=s|s=qual      19      mod     _       _       _       _       _       _
des     _       21-22   _       _       _       _       _       _       _       _       _       _       _
de      de      21      P       P       _       19      dep     _       _       _       _       _       _
les     le      22      D       DET     g=m|n=p|s=def   24      det     _       _       _       _       _       _
grands  grand   23      A       ADJ     g=m|n=p|s=qual  24      mod     _       _       _       _       _       _
frères  frère   24      N       NC      g=m|n=p|s=c     21      obj.p   _       _       _       _       _       _
,       ,       25      PONCT   PONCT   s=w     2       ponct   _       _       _       _       _       _
comme   comme   26      C       CS      s=s     2       mod     _       _       _       _       _       _
nous    le/lui  27      CL      CLO     n=p|p=1|s=obj   29      a_obj   _       _       _       _       _       _
le      le      28      CL      CLO     g=m|n=s|p=3|s=obj       29      obj     _       _       _       _       _       _
laisse  laisser 29      V       V       m=ind|n=s|p=3|t=pst     26      obj.cpl _       _       ID      head    2       laisser à penser
à       à       30      P       P       _       29      a_obj   _       _       ID      child   2       laisser à penser
penser  penser  31      V       VINF    m=inf   30      obj.p   _       _       ID      child   2       laisser à penser
le      le      32      D       DET     g=m|n=s|s=def   33      det     _       _       _       _       _       _
cas     cas     33      N       NC      g=m|s=c 29      suj     _       _       _       _       _       _
récent  récent  34      A       ADJ     g=m|n=s|s=qual  33      mod     _       _       _       _       _       _
d'      de      35      P       P       _       33      dep     _       _       _       _       _       _
Échelon Échelon 36      N       NPP     s=p     35      obj.p   _       _       _       _       _       _
,       ,       37      PONCT   PONCT   s=w     33      ponct   _       _       _       _       _       _
sur     sur     38      P       P       _       43      p_obj   _       _       _       _       _       _
lequel  lequel  39      PRO     PROREL  g=m|n=s|s=rel   38      obj.p   _       _       _       _       _       _
cette   ce      40      D       DET     g=f|n=s|s=dem   41      det     _       _       _       _       _       _
Assemblée       assemblée       41      N       NC      g=f|n=s|s=c     43      suj     _       _       _       _       _       _
se      le/lui  42      CL      CLR     p=3|s=refl      43      aff     _       _       IReflV  head    5       le/lui pencher
penchera        pencher 43      V       V       m=ind|n=s|p=3|t=fut     33      mod.rel _       _       IReflV  child   5       le/lui pencher
sous    sous    44      P       P       _       43      mod     _       _       _       _       _       _
peu     peu     45      ADV     ADV     _       44      obj.p   _       _       _       _       _       _
.       .       46      PONCT   PONCT   s=s     2       ponct   _       _       _       _       _       _
</s>



```



