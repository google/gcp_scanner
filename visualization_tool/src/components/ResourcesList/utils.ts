import {Resource} from '../../types/resources';
import ComputeInstance from '../../assets/resources/Compute Instance.png';
import ComputeDisk from '../../assets/resources/Compute Disk.png';
import ManagedZone from '../../assets/resources/Managed Zone.png';
import SQLInstance from '../../assets/resources/SQL Instance.png';
import CloudFunction from '../../assets/resources/Cloud Function.png';
import defaultLogo from '../../assets/resources/resource.png';

const typeToImage = (resource: Resource) => {
  switch (resource.type) {
    case 'Compute Instance':
    case 'Compute Image':
    case 'Machine Image':
    case 'Compute Snapshot':
      return ComputeInstance;
    case 'Compute Disk':
      return ComputeDisk;
    case 'Managed Zone':
      return ManagedZone;
    case 'Sql Instance':
      return SQLInstance;
    case 'Cloud Function':
      return CloudFunction;
    default:
      return defaultLogo;
  }
};

const statusToColor = (status: string) => {
  switch (status) {
    case 'RUNNING':
      return 'green';
    case 'READY':
      return 'blue';
    case 'TERMINATED':
      return 'red';
    default:
      return 'grey';
  }
};

export {typeToImage, statusToColor};
