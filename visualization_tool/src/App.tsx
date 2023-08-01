import {useState} from 'react';
import {Resource} from './types/resources';

import Navbar from './components/Navbar/Navbar';
import ControlMenu from './components/ControlMenu/ControlMenu';
import ResourcesList from './components/ResourcesList/ResourcesList';

function App() {
  const [resources, setResources] = useState<Resource[]>([]);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [sortAttribute, setSortAttribute] = useState<string>('date');
  return (
    <>
      <Navbar searchQuery={searchQuery} setSearchQuery={setSearchQuery} />
      <main>
        <ControlMenu
          setResources={setResources}
          setSortAttribute={setSortAttribute}
        />
        <ResourcesList
          resources={resources}
          searchQuery={searchQuery}
          sortAttribute={sortAttribute}
        />
      </main>
    </>
  );
}

export default App;
