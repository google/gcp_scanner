import {Resource} from '../../types/resources';
import GCE from '../../assets/resources/GCE.png';
import GCS from '../../assets/resources/GCS.png';

const imageToURL = (resource: Resource) => {
  switch (resource.type) {
    case 'GCE':
      return GCE;
    case 'GCS':
      return GCS;
    default:
      return '';
  }
};

export {imageToURL};
