import {Resource} from '../types/resources';
import ResourcesList from '../components/ResourcesList/ResourcesList';

type ResourcesPageProps = {
  resources: Resource[];
  sortAttribute: string;
  allowedTypes: string[];
  searchQuery: string;
};

const ResourcesPage = ({
  resources,
  searchQuery,
  sortAttribute,
  allowedTypes,
}: ResourcesPageProps) => {
  return (
    <>
      <ResourcesList
        resources={resources}
        searchQuery={searchQuery}
        sortAttribute={sortAttribute}
        allowedTypes={allowedTypes}
      />
    </>
  );
};

export default ResourcesPage;
