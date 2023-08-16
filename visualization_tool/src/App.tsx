import {useState} from 'react';

import {Routes, Route} from 'react-router-dom';

import {Resource, availableResourceTypes} from './types/resources';
import ControlMenuLayout from './layouts/ControlMenuLayout';
import ControlMenu from './components/ControlMenu/ControlMenu';
import ResourcesPage from './pages/ResourcesPage';
import IAMPolicyPage from './pages/IAMPolicyPage';
import Navbar from './components/Navbar/Navbar';

function App() {
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [sortAttribute, setSortAttribute] = useState<string>('date');
  const [resources, setResources] = useState<Resource[]>([]);
  const [allowedTypes, setAllowedTypes] = useState<string[]>(
    availableResourceTypes
  );
  return (
    <>
      <Navbar searchQuery={searchQuery} setSearchQuery={setSearchQuery} />
      <ControlMenuLayout>
        <ControlMenu
          setResources={setResources}
          setSortAttribute={setSortAttribute}
          setAllowedTypes={setAllowedTypes}
        />
      </ControlMenuLayout>
      <Routes>
        <Route
          path="/static/"
          element={
            <ResourcesPage
              resources={resources}
              searchQuery={searchQuery}
              sortAttribute={sortAttribute}
              allowedTypes={allowedTypes}
            />
          }
        />
        <Route path="/static/iam-policy" element={<IAMPolicyPage />} />
      </Routes>
    </>
  );
}

export default App;
