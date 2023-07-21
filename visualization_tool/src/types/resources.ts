type ResourceType = 'GCE' | 'GCS' | 'GKE' | 'App Engine';
type ResourceStatus = 'READY' | 'RUNNING' | 'STOPPED' | 'DELETED';

type Resource = {
  projectId: string;
  file: string;
  id: string;
  name: string;
  type: ResourceType;
  creationTimestamp: string;
  status: ResourceStatus;
};

type ComputeEngine = Resource & {
  type: 'GCE';
  zone: string;
  machineType: string;
};

type CloudStorage = Resource & {
  type: 'GCS';
  storageType: string;
  sizeGb: number;
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
  ResourceType,
  ResourceStatus,
  Resource,
  ComputeEngine,
  CloudStorage,
  KubernetesEngine,
  AppEngine,
  Project,
  OutputFile,
};
