import {useState} from 'react';
import {Resource, availableResourceTypes} from './types/resources';

import Navbar from './components/Navbar/Navbar';
import ControlMenu from './components/ControlMenu/ControlMenu';
import ResourcesList from './components/ResourcesList/ResourcesList';

function App() {
  const [resources, setResources] = useState<Resource[]>([]);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [sortAttribute, setSortAttribute] = useState<string>('date');
  const [allowedTypes, setAllowedTypes] = useState<string[]>(
    availableResourceTypes
  );
  return (
    <>
      <Navbar searchQuery={searchQuery} setSearchQuery={setSearchQuery} />
      <main>
        <ControlMenu
          setResources={setResources}
          setSortAttribute={setSortAttribute}
          setAllowedTypes={setAllowedTypes}
        />
        <ResourcesList
          resources={resources}
          searchQuery={searchQuery}
          sortAttribute={sortAttribute}
          allowedTypes={allowedTypes}
        />
      </main>
    </>
  );
}

export default App;
