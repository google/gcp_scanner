import {useState} from 'react';

import {Routes, Route} from 'react-router-dom';

import {Resource, availableResourceTypes} from './types/resources';
import {IAMRole} from './types/IAMPolicy';
import ControlMenu from './components/ControlMenu/ControlMenu';
import ResourcesPage from './pages/ResourcesPage';
import IAMPolicyPage from './pages/IAMPolicyPage';
import Navbar from './components/Navbar/Navbar';

function App() {
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [sortAttribute, setSortAttribute] = useState<string>('date');
  const [resources, setResources] = useState<Resource[]>([]);
  const [projects, setProjects] = useState<string[]>([]);
  const [allowedProjects, setAllowedProjects] = useState<string[]>(projects);
  const [allowedTypes, setAllowedTypes] = useState<string[]>(
    availableResourceTypes
  );
  const [roles, setRoles] = useState<IAMRole[]>([]);
  return (
    <>
      <Navbar searchQuery={searchQuery} setSearchQuery={setSearchQuery} />
      <ControlMenu
        setResources={setResources}
        setProjects={setProjects}
        setSortAttribute={setSortAttribute}
        setAllowedTypes={setAllowedTypes}
        setRoles={setRoles}
        projects={projects}
        setAllowedProjects={setAllowedProjects}
      />
      <Routes>
        <Route
          path="/static/"
          element={
            <ResourcesPage
              resources={resources}
              searchQuery={searchQuery}
              sortAttribute={sortAttribute}
              allowedTypes={allowedTypes}
              allowedProjects={allowedProjects}
            />
          }
        />
        <Route
          path="/static/iam-policy"
          element={
            <IAMPolicyPage
              roles={roles}
              emailQuery={searchQuery}
              allowedProjects={allowedProjects}
            />
          }
        />
      </Routes>
    </>
  );
}

export default App;
