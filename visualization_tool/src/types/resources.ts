type ResourceType = 'GCE' | 'GCS' | 'GKE' | 'App Engine';

type Resource = {
  id: string;
  name: string;
  type: ResourceType;
  creationTimestamp: string;
  status: 'RUNNING' | 'STOPPED' | 'DELETED';
};

type ComputeEngine = Resource & {
  type: 'GCE';
  zone: string;
  machineType: string;
  cpu: number;
  memory: number;
};

type CloudStorage = Resource & {
  type: 'GCS';
  bucket: string;
  location: string;
  size: number;
};

type KubernetesEngine = Resource & {
  type: 'GKE';
  cluster: string;
  location: string;
  nodePools: string[];
};

type AppEngine = Resource & {
  type: 'App Engine';
  location: string;
  services: string[];
};

type Project = {
  project_info: {
    projectNumber: string;
    projectId: string;
  };
  compute_instances: ComputeEngine[];
  compute_disks: CloudStorage[];
  gke_clusters: KubernetesEngine[];
  app_engine_services: AppEngine[];
};

type OutputFile = {
  projects: {
    [key: string]: Project;
  };
};

export type {
  Resource,
  ComputeEngine,
  CloudStorage,
  KubernetesEngine,
  AppEngine,
  Project,
  OutputFile,
};
