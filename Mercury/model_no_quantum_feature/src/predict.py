
import pickle
import dgl
import torch
import pysmiles
import numpy as np
from model import MyModel
import argparse
from data_processing import networkx_to_dgl
from dgl.dataloading import GraphDataLoader
import warnings

warnings.filterwarnings("ignore")


class GraphDataset(dgl.data.DGLDataset):
    def __init__(self, path_to_model, rxn_smiles, gpu):
        self.path = path_to_model
        self.rxn_smiles = rxn_smiles
        self.reactant_graphs = []
        self.product_graphs = []
        self.parsed = []
        self.gpu = gpu
        super().__init__(name='graph_dataset')

    def process(self):
        with open(self.path + '/feature_enc.pkl', 'rb') as f:
            self.feature_encoder = pickle.load(f)
        f.close()

        for i, rxn in enumerate(self.rxn_smiles):
            try: 
                rxn = rxn.strip()
                reactant_smiles, product_smiles = rxn.split('>>')[0], rxn.split('>>')[1]
                if 'se' in reactant_smiles:
                    reactant_smiles = reactant_smiles.replace('se', 'Se')
                if 'se' in product_smiles:
                    product_smiles = product_smiles.replace('se', 'Se')

                reactant_graph = pysmiles.read_smiles(reactant_smiles, zero_order_bonds=False)
                product_graph = pysmiles.read_smiles(product_smiles, zero_order_bonds=False)
               
                reactant_graph = networkx_to_dgl(reactant_graph, self.feature_encoder)
                product_graph = networkx_to_dgl(product_graph, self.feature_encoder)
                self.reactant_graphs.append(reactant_graph)
                self.product_graphs.append(product_graph)
                self.parsed.append(i)
            except:
                print('ERROR: No. %d smiles is not parsed successfully' % i)
        print('the number of smiles successfully parsed: %d' % len(self.parsed))
        print('the number of smiles failed to be parsed: %d' % (len(self.rxn_smiles) - len(self.parsed)))
        if torch.cuda.is_available() and self.gpu is not None:
            self.reactant_graphs = [graph.to('cuda:' + str(self.gpu)) for graph in self.reactant_graphs]
            self.product_graphs = [graph.to('cuda:' + str(self.gpu)) for graph in self.product_graphs]

    def __getitem__(self, i):
        return self.reactant_graphs[i], self.product_graphs[i]

    def __len__(self):
        return len(self.reactant_graphs)



class MolEFeaturizer(object):
    def __init__(self, path_to_model, gpu=0):
        self.path_to_model = path_to_model
        self.gpu = gpu
        with open(path_to_model + '/hparams.pkl', 'rb') as f:
            hparams = pickle.load(f)
        self.mole = MyModel(hparams['gnn'], hparams['layer'], hparams['feature_len'], hparams['dim'])
        self.dim = hparams['dim']
        if torch.cuda.is_available() and gpu is not None:
            self.mole.load_state_dict(torch.load(path_to_model + '/model.pt'))
            self.mole = self.mole.cuda(gpu)
        else:
            self.mole.load_state_dict(torch.load(path_to_model + '/model.pt', map_location=torch.device('cpu')))

    def transform(self, rxn_smiles, batch_size=None):
        data = GraphDataset(self.path_to_model, rxn_smiles, self.gpu)
        dataloader = GraphDataLoader(data, batch_size=batch_size if batch_size is not None else len(rxn_smiles))
        all_preds = np.zeros((len(rxn_smiles)))
        flags = np.zeros(len(rxn_smiles), dtype=bool)
        res = []
        with torch.no_grad():
            self.mole.eval()
            for reactant_graphs, product_graphs in dataloader:
                preds = self.mole(reactant_graphs, product_graphs)
                res.extend(preds.cpu())
        
        all_preds[data.parsed] = res
        flags[data.parsed] = True
        print('done\n')
        return all_preds, flags


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--csv_file', type=str, default='', help='the path of csv file')

    args = parser.parse_args()

    f = open(args.csv_file, 'r')
    rxn_smiles = f.readlines()

    model = MolEFeaturizer(path_to_model='saved_model/')

    out_file_name = args.csv_file.split('.')[0] + '_result.csv'
    outfile = open(out_file_name, 'w') 
    all_preds, flags = model.transform(rxn_smiles)
    print('rxn_smiles', 'feasible_probability', 'successfully_predict', sep=',', file=outfile)
    for i,j,k in zip(rxn_smiles, all_preds.tolist(), flags):
        print(i.strip(),j,k, sep=',', file=outfile)

    print(f'Finally result file is {out_file_name}')
    


if __name__ == '__main__':
    main()
