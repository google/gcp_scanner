import Drawer from '@mui/material/Drawer';
import {capitalize} from '@mui/material';

import {Resource} from '../../../types/resources';

type DetailsProps = {
  selectedResource: Resource | null;
  openDetails: boolean;
  setOpenDetails: React.Dispatch<React.SetStateAction<boolean>>;
};

const Details = ({
  selectedResource,
  openDetails,
  setOpenDetails,
}: DetailsProps) => {
  return (
    <Drawer
      anchor="right"
      open={openDetails}
      onClose={() => setOpenDetails(false)}
    >
      <div className="resource-details">
        <h2>Resource Details</h2>
        {selectedResource &&
          Object.keys(selectedResource).map(key => {
            return (
              <div className="resource-details__item" key={key}>
                <p className="resource-details__item__key">
                  {capitalize(key)}:
                </p>
                <p className="resource-details__item__value">
                  {selectedResource[key as keyof Resource]}
                </p>
              </div>
            );
          })}
      </div>
    </Drawer>
  );
};

export default Details;
