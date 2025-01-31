## A package to compute the Reactivity-Related bond/atom-wise Descriptors (RRD).

### Usage
```python
from rrd import RRDCalculator
RRDC = RRDCalculator(scale=True)
smiles = 'CCCC'

## one smiles
dfa, dfb = RRDC.transform(smiles)

## many smiles: compute in parallel
smiles_list = [smiles for i in range(20)]
res = RRDC.batch_transform(smiles_list, n_jobs=-1)
```

### TODO list
- [x] Buried Volume
- [ ] Frontier orbital energy


### List of descriptors in our RRD package

| Descriptor | Description                    | Atom/Bond | Ref.  | Package                                              |
| ---------- | ------------------------------ | --------- | ----- | ---------------------------------------------------- |
| PC         | Hirshfeld partial charge       | Atom      | \[1\] | [qmdesc](https://github.com/yanfeiguan/qmdesc)   |
| FN         | Neucleuphilic Fukui indices    | Atom      | \[1\] | [qmdesc](https://github.com/yanfeiguan/qmdesc)    |
| FE         | Electrophilic Fukui indices    | Atom      | \[1\] | [qmdesc](https://github.com/yanfeiguan/qmdesc)    |
| NSC        | NMR shielding constants        | Atom      | \[1\] | [qmdesc](https://github.com/yanfeiguan/qmdesc)   |
| GC         | GasteigerCharge                | Atom      | \[2\] | [Rdkit](https://www.rdkit.org/docs/Cookbook.html) |
| MR         | Molar refractivity             | Atom      | \[3\] | [Rdkit](https://www.rdkit.org/docs/Cookbook.html) |
| Apol       | Atomic polarizability          | Atom      | \[4\] | [Rdkit](https://www.rdkit.org/docs/Cookbook.html) |
| SHI        | Steric hindrance index         | Atom      | \[5\] | \-                                                   |
| TSEI       | Toplogical steric effect index | Atom      | \[5\] | \-                                                   |
| OV       | Occupied volume | Atom      | \[7\] | [DBSTEP](https://github.com/patonlab/DBSTEP/tree/325e24224e523014c61263bef357c9fa55316f32/dbstep) |
| PBV       | Percent buried volume | Atom      | \[7\] | [DBSTEP](https://github.com/patonlab/DBSTEP/tree/325e24224e523014c61263bef357c9fa55316f32/dbstep) |           
| PSV       | Percent shell volume | Atom      | \[7\] |[DBSTEP](https://github.com/patonlab/DBSTEP/tree/325e24224e523014c61263bef357c9fa55316f32/dbstep)  |
| SB         | Single bond                    | Bond      | \-    | \-                                                   |
| DB         | Double bond                    | Bond      | \-    | \-                                                   |
| TB         | Triple bond                    | Bond      | \-    | \-                                                   |
| AB         | Aromatic bond                  | Bond      | \-    | \-                                                   |
| CB         | Conjugation bond               | Bond      | \-    | \-                                                   |
| RB         | Ring bond                      | Bond      | \-    | \-                                                   |
| SN         | Stereo-None                    | Bond      | \-    | \-                                                   |
| SA         | Stereo-Any                     | Bond      | \-    | \-                                                   |
| SS         | Stereo-S                       | Bond      | \-    | \-                                                   |
| SR         | Stereo-R                       | Bond      | \-    | \-                                                   |
| BO         | Bond order                     | Bond      | \[1\] | [qmdesc](https://github.com/yanfeiguan/qmdesc)   |
| BL         | Bond length                    | Bond      | \[1\] | [qmdesc](https://github.com/yanfeiguan/qmdesc)   |
| BDE        | Bond dissociation enthalpies   | Bond      | \[6\] | [alfabet](https://github.com/NREL/alfabet)        |
| BDFE       | Bond dissociation free energies   | Bond      | \[6\] |[alfabet](https://github.com/NREL/alfabet)        |


**Refernces**
- [1]. Guan, Yanfei, et al. "Regio-selectivity prediction with a machine-learned reaction representation and on-the-fly quantum mechanical descriptors." Chemical science 12.6 (2021): 2198-2208.
- [2]. J.Gasteiger, M. Marseli, Iterative Equalization of Oribital Electronegatiity A Rapid Access to Atomic Charges, Tetrahedron Vol 36 p3219 1980
- [3]. Wildman, Scott A., and Gordon M. Crippen. "Prediction of physicochemical parameters by atomic contributions." Journal of chemical information and computer sciences 39.5 (1999): 868-873.
- [4]. Miller and Savchik, JACS 101(24) 7206-7213, 1979.
- [5]. Cao, Chenzhong, and Li Liu. "Topological steric effect index and its application." Journal of chemical information and computer sciences 44.2 (2004): 678-687.
- [6]. St John, Peter C., et al. "Prediction of organic homolytic bond dissociation enthalpies at near chemical accuracy with sub-second computational cost." Nature communications 11.1 (2020): 1-12.
- [7]. A. Poater, F. Ragone, R. Mariz, R. Dorta and L. Cavallo, Chem. Eur. J. 2010, 16, 14348–14353.
