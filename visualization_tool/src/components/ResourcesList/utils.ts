import {Resource} from '../../types/resources';
import ComputeInstance from '../../assets/resources/Compute Instance.png';
import ComputeDisk from '../../assets/resources/Compute Disk.png';

const typeToImage = (resource: Resource) => {
  switch (resource.type) {
    case 'Compute Instance':
      return ComputeInstance;
    case 'Compute Disk':
      return ComputeDisk;
    default:
      return '';
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
