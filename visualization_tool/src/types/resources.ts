type ResourceType =
  | 'Compute Instance'
  | 'Compute Disk'
  | 'Compute Image'
  | 'Machine Image'
  | 'Compute Snapshot'
  | 'Managed Zone'
  | 'Sql Instance'
  | 'Cloud Function'
  | 'Dns Policy'
  | 'Pubsub Sub';

const availableResourceTypes: ResourceType[] = [
  'Compute Instance',
  'Compute Disk',
  'Compute Image',
  'Machine Image',
  'Compute Snapshot',
  'Managed Zone',
  'Sql Instance',
  'Cloud Function',
  'Dns Policy',
  'Pubsub Sub',
];

type ResourceStatus = 'READY' | 'ACTIVE' | 'RUNNING' | 'STOPPED' | 'DELETED';

type Resource = {
  projectId: string;
  file: string;
  id: string;
  name: string;
  type: ResourceType;
  creationTimestamp: string;
  status: ResourceStatus;
};

type Project = {
  [key: string]: Resource[];
};

type OutputFile = {
  projects: {
    [key: string]: Project;
  };
};

export type {ResourceType, ResourceStatus, Resource, Project, OutputFile};

export {availableResourceTypes};
