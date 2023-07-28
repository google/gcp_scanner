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
    const computeInstances = projectData.compute_instances?.map(
      computeInstance => {
        return {
          ...getResourceData(computeInstance, projectId, fileName),
          type: 'Compute Instance' as const,
          zone: computeInstance.zone.split('/').at(-1) as string,
          machineType: computeInstance.machineType.split('/').at(-1) as string,
        };
      }
    );
    resources.push(...computeInstances);

    const computeDisks = projectData.compute_disks.map(computeDisk => {
      return {
        ...getResourceData(computeDisk, projectId, fileName),
        type: 'Compute Disk' as const,
        storageType: computeDisk.type.split('/').at(-1) as string,
        sizeGb: computeDisk.sizeGb,
      };
    });

    resources.push(...computeDisks);
  }

  return resources;
};

export {parseData};
