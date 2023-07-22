import {useState} from 'react';
import {Resource} from './types/resources';

import Navbar from './components/Navbar/Navbar';
import ControlMenu from './components/ControlMenu/ControlMenu';
import ResourcesList from './components/ResourcesList/ResourcesList';

import './App.css';

function App() {
  const [resources, setResources] = useState<Resource[]>([]);
  return (
    <>
      <Navbar />
      <main>
        <ControlMenu setResources={setResources} />
        <ResourcesList resources={resources} />
      </main>
    </>
  );
}

export default App;
