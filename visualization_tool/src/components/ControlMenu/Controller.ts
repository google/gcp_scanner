import {OutputFile, Resource} from '../../types/resources';

const getResourceData = (
  resource: Resource,
  projectId: string,
  fileName: string
) => {
  return {
    projectId,
    file: fileName,
    id: resource.id,
    name: resource.name,
    creationTimestamp: resource.creationTimestamp,
    status: resource?.status || 'READY',
  };
};

const parseData = (data: OutputFile, fileName: string) => {
  const resources = [];
  for (const [projectId, projectData] of Object.entries(data.projects)) {
    const computeEngines = projectData.compute_instances?.map(computeEngine => {
      return {
        ...getResourceData(computeEngine, projectId, fileName),
        type: 'GCE' as const,
        zone: computeEngine.zone.split('/').at(-1) as string,
        machineType: computeEngine.machineType.split('/').at(-1) as string,
      };
    });
    resources.push(...computeEngines);

    const cloudStorages = projectData.compute_disks.map(cloudStorage => {
      return {
        ...getResourceData(cloudStorage, projectId, fileName),
        type: 'GCS' as const,
        storageType: cloudStorage.type.split('/').at(-1) as string,
        sizeGb: cloudStorage.sizeGb,
      };
    });

    resources.push(...cloudStorages);
  }

  return resources;
};

export {parseData};
