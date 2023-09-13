import {Resource} from '../types/resources';
import ResourcesList from '../components/ResourcesList/ResourcesList';

type ResourcesPageProps = {
  resources: Resource[];
  sortAttribute: string;
  allowedTypes: string[];
  allowedProjects: string[];
  searchQuery: string;
};

const ResourcesPage = ({
  resources,
  searchQuery,
  sortAttribute,
  allowedTypes,
  allowedProjects,
}: ResourcesPageProps) => {
  return (
    <>
      <ResourcesList
        resources={resources}
        searchQuery={searchQuery}
        sortAttribute={sortAttribute}
        allowedTypes={allowedTypes}
        allowedProjects={allowedProjects}
      />
    </>
  );
};

export default ResourcesPage;
