import {Resource} from '../../types/resources';
import GCE from '../../assets/resources/GCE.png';
import GCS from '../../assets/resources/GCS.png';

const typeToImage = (resource: Resource) => {
  switch (resource.type) {
    case 'GCE':
      return GCE;
    case 'GCS':
      return GCS;
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
