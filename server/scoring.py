from nullload import NullLoader
from torch.utils.data import Dataset, DataLoader
import numpy as np
import torch
from sklearn.cluster import KMeans
import random
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# Ensure the API key is set
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the .env file")

client = OpenAI(api_key=OPENAI_API_KEY)

class EssaysDataset(Dataset):
  def __init__(self, data):
    self.data, self.index_dict = get_embeddings(data)

  def __len__(self):
    return len(self.data)

  def __getitem__(self, idx):

    return self.data[idx], [0,0]


def get_nullloder_scores(essays):
    BATCH = 32
    essays_dataset = EssaysDataset(essays)
    control_loader = torch.utils.data.DataLoader(essays_dataset, batch_size=BATCH)
    def norm(x):
        vnorm = torch.linalg.vector_norm(x.view(x.shape[0], -1), dim=1)
        return x.transpose(0, -1).div(vnorm).transpose(0, -1)
    PROTOBATCH = 16
    RITERS = 8
    MEM = 256
    proto_loader = torch.utils.data.DataLoader(essays_dataset, batch_size=PROTOBATCH)
    print("loader", proto_loader.batch_size)
    exp_loader = NullLoader(control_loader, BATCH, RITERS, MEM, (256,), (256,), norm, device="cuda")
    candidates, lablels, weights, asort = next(iter(exp_loader))
    print(candidates.shape)
    print(weights.shape)
    print(asort.shape)
    
    weights = weights.cpu().numpy()
    weights /= weights.max()
    weights *= 100
    scores = {}
    for name in essays_dataset.index_dict:
        scores[name] = weights[essays_dataset.index_dict[name]]
    return scores


def get_k_means_scores(essays):
    n_clusters = 6  # Set the number of clusters as needed

    # Extract features from the dataset
    features_list, index_dict = get_embeddings(essays)
    dataset_length = len(features_list)

    X = np.array(features_list)

    # Perform K-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(X)

    # Get cluster labels for each data point
    cluster_labels = kmeans.labels_


    # Organize data points by clusters
    cluster_sizes = {}
    for i in cluster_labels:
       if i in cluster_sizes:
            cluster_sizes[i] += 1
       else:
           cluster_sizes[i] = 1
    # Initialize a dictionary to store scores
    scores = {}

    for name in index_dict:
        print("cluster_sizes",cluster_sizes)
        print("cluster_labels",cluster_labels)
        cluster_size = cluster_sizes[cluster_labels[index_dict[name]]]
        print("cluster_size",cluster_size)
        scores[name] = (1 - (cluster_size / dataset_length)) * 100

    return scores

def get_embeddings(essays):
    index_dict = {}
    features_list = []
    for i, essay in enumerate(essays):
        embedding = client.embeddings.create(input=essay[1], model="text-embedding-3-small", dimensions=256).data[0].embedding
        features_list.append(np.array(embedding))
        index_dict[essay[0]] = i

    return features_list, index_dict

def get_scores(essays):
    if len(essays) > 256:
        return get_nullloder_scores(essays)
    else:
        return get_k_means_scores(essays)

