import ControlMenu from './components/ControlMenu/ControlMenu';
import ResourcesList from './components/ResourcesList/ResourcesList';

import logo from '/logo.png';
import './App.css';

function App() {
  return (
    <>
      <header>
        <img src={logo} className="logo" alt="GCP Scanner logo" />
        <p>Scanner</p>
      </header>
      <div className="pages-nav">
        <a className="active" href="">
          Resources
        </a>
        <a href="">IAM Policy</a>
      </div>
      <main>
        <ControlMenu />
        <ResourcesList />
      </main>
    </>
  );
}

export default App;
