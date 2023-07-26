type ResourceType = 'Compute Instance' | 'Compute Disk';
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

type ComputeInstance = Resource & {
  type: 'Compute Instance';
  zone: string;
  machineType: string;
};

type ComputeDisk = Resource & {
  type: 'Compute Disk';
  storageType: string;
  sizeGb: number;
};

type Project = {
  project_info: {
    projectNumber: string;
    projectId: string;
  };
  compute_instances: ComputeInstance[];
  compute_disks: ComputeDisk[];
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
  ComputeInstance,
  ComputeDisk,
  Project,
  OutputFile,
};
